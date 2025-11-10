#!/usr/bin/env python3
"""
Decision Unit FSM (ROS 2 + transitions.GraphMachine + visualizer)

Implements and visualizes the shuttle’s autonomous state machine.
Publishes each /vehicle_state only once per real transition.
"""

import rclpy
import time
from transitions.extensions import GraphMachine
from std_msgs.msg import Bool, Int8
from rclpy.node import Node
import threading

# Define STATE_CODES at the top
STATE_CODES = {
    'IDLE': 0,
    'DRIVING_TO_PICKUP': 1,
    'BOARDING': 2,
    'DRIVING_TO_DROPOFF': 3,
    'DEBOARDING': 4,
    'PARKING': 5
}

# Optional visualization support
try:
    import pygraphviz
    HAS_PYGRAPHVIZ = True
except ImportError:
    HAS_PYGRAPHVIZ = False


class DecisionUnit:
    """Finite State Machine logic for the Decision Unit."""

    states = list(STATE_CODES.keys())

    def __init__(self, node: Node):
        self.node = node
        self.finished = False  # flag to stop FSM after final IDLE

        # Blackboard flags
        self.booking_request = None
        self.goal_reached_for_pickup = None
        self.goal_reached_for_dropoff = None
        self.goal_reached_for_parking = None
        self.door_open = None

        # Initialize FSM
        self.machine = GraphMachine(  # Change here
            model=self,
            states=DecisionUnit.states,
            initial='IDLE',
            ignore_invalid_triggers=True
        )

        # ------------------- Transitions -------------------
        self.machine.add_transition('try_transition', 'IDLE', 'DRIVING_TO_PICKUP',
                                    conditions='is_booking_received', after='publish_state')
        self.machine.add_transition('try_transition', 'DRIVING_TO_PICKUP', 'BOARDING',
                                    conditions='is_goal_reached_for_pickup', after='publish_state')
        self.machine.add_transition('try_transition', 'BOARDING', 'DRIVING_TO_DROPOFF',
                                    conditions='is_door_closed_after_boarding', after='publish_state')
        self.machine.add_transition('try_transition', 'DRIVING_TO_DROPOFF', 'DEBOARDING',
                                    conditions='is_door_closed_after_dropoff', after='publish_state')  # Updated condition here
        self.machine.add_transition('try_transition', 'DEBOARDING', 'PARKING',
                                    conditions='is_door_closed_after_deboarding', after='publish_state')
        self.machine.add_transition('try_transition', 'PARKING', 'IDLE',
                                    conditions='is_goal_reached_for_parking', after='publish_and_stop')

        # Draw the FSM diagram once at startup
        if HAS_PYGRAPHVIZ:
            try:
                g = self.machine.get_graph()
                g.draw("/tmp/decision_fsm.png", prog="dot")
                self.node.get_logger().info("FSM diagram exported to /tmp/decision_fsm.png")
            except Exception as e:
                self.node.get_logger().error(f"Graph export failed: {e}")
        else:
            self.node.get_logger().warn(
                "pygraphviz not installed. Run: sudo apt install graphviz graphviz-dev && pip install pygraphviz"
            )

        # Publish initial IDLE state only once
        self.publish_state()

    # ------------------- Condition Functions -------------------
    def is_booking_received(self):
        return self.booking_request is True

    def is_goal_reached_for_pickup(self):
        """Goal reached for pickup."""
        return self.goal_reached_for_pickup

    def is_door_closed_after_boarding(self):
        """Door must be closed after boarding before transitioning to driving to dropoff."""
        if self.door_open is False:
            self.door_open = None  # Reset door status immediately after checking
            return True
        self.door_open = None  # Reset door status if condition is not met
        return False

    def is_door_closed_after_dropoff(self):
        """Door must be closed after dropoff before transitioning to deboarding."""
        if self.goal_reached_for_dropoff:
            self.goal_reached_for_dropoff = None  # Reset flag after usage
            self.door_open = None  # Reset door status immediately after checking
            return True
        self.door_open = None  # Reset door status if condition is not met
        return False

    def is_door_closed_after_deboarding(self):
        """Check if doors closed after deboarding."""
        if self.door_open is False:
            self.door_open = None  # Reset door status immediately after checking
            return True
        self.door_open = None  # Reset door status if condition is not met
        return False

    def is_goal_reached_for_parking(self):
        """Goal reached for parking."""
        if self.goal_reached_for_parking:
            self.goal_reached_for_parking = None  # Reset flag after usage
            return True
        return False

    # ------------------- Publisher -------------------
    def publish_state(self):
        """Publish /vehicle_state when transition actually occurs."""
        code = STATE_CODES[self.state]
        msg = Int8()
        msg.data = code
        self.node.vehicle_state_pub.publish(msg)
        self.node.get_logger().info(f"/vehicle_state = {code} ({self.state})")

        # Live update FSM visualization
        if HAS_PYGRAPHVIZ:
            try:
                g = self.machine.get_graph()
                g.draw("/tmp/decision_fsm.png", prog="dot")
            except Exception:
                pass

    def publish_and_stop(self):
        """Publish IDLE at final transition and stop FSM loop."""
        self.publish_state()
        self.finished = True
        self.node.get_logger().info("FSM reached final IDLE. Stopping state updates.")

    # ------------------- FSM Monitor -------------------
    def monitor(self):
        """Trigger transition periodically and stop the loop after a final IDLE state."""
        prev_state = self.state
        while rclpy.ok() and not self.finished:
            self.try_transition()  # Try transition based on current conditions
            if self.state != prev_state:
                self.publish_state()  # Publish state change only if transition occurs
                prev_state = self.state  # Update the previous state
            time.sleep(0.5)  # Check every 0.5 seconds


class DecisionUnitNode(Node):
    """ROS 2 Node wrapper for the Decision Unit FSM."""

    def __init__(self):
        super().__init__('decision_core_fsm')
        self.vehicle_state_pub = self.create_publisher(Int8, '/vehicle_state', 10)
        self.fsm = DecisionUnit(self)

        self.create_subscription(Bool, '/booking_request', self.booking_cb, 10)
        self.create_subscription(Bool, '/goal_reached', self.goal_cb, 10)
        self.create_subscription(Bool, '/door_open', self.door_cb, 10)

        self.get_logger().info("Decision Unit FSM (transitions-based) started.")

    # --------------- Callbacks ---------------
    def booking_cb(self, msg):
        self.fsm.booking_request = msg.data

    def goal_cb(self, msg):
        # Check goal_reached conditions based on the state
        if self.fsm.state == 'DRIVING_TO_PICKUP' and msg.data:
            self.fsm.goal_reached_for_pickup = True
        elif self.fsm.state == 'DRIVING_TO_DROPOFF' and msg.data:
            self.fsm.goal_reached_for_dropoff = True
        elif self.fsm.state == 'PARKING' and msg.data:
            self.fsm.goal_reached_for_parking = True
        self.fsm.goal_reached = msg.data

    def door_cb(self, msg):
        self.fsm.door_open = msg.data


# ------------------- Entry Point -------------------
def main():
    rclpy.init()
    node = DecisionUnitNode()

    # Start monitor in a separate thread to avoid blocking the ROS 2 event loop
    monitor_thread = threading.Thread(target=node.fsm.monitor)
    monitor_thread.start()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        monitor_thread.join()


if __name__ == '__main__':
    main()

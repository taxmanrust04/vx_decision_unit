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

# Define state codes
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
        self.finished = False  # Stop FSM after final IDLE

        # Blackboard flags
        self.booking_request = None
        self.goal_reached_for_pickup = None
        self.goal_reached_for_dropoff = None
        self.goal_reached_for_parking = None
        self.door_open = None

        # Initialize FSM
        self.machine = GraphMachine(
            model=self,
            states=DecisionUnit.states,
            initial='IDLE',
            ignore_invalid_triggers=True
        )

        # Define transitions
        self.machine.add_transition('try_transition', 'IDLE', 'DRIVING_TO_PICKUP',
                                    conditions='is_booking_received', after='publish_state')
        self.machine.add_transition('try_transition', 'DRIVING_TO_PICKUP', 'BOARDING',
                                    conditions='is_goal_reached_for_pickup', after='publish_state')
        self.machine.add_transition('try_transition', 'BOARDING', 'DRIVING_TO_DROPOFF',
                                    conditions='is_door_closed_after_boarding', after='publish_state')
        self.machine.add_transition('try_transition', 'DRIVING_TO_DROPOFF', 'DEBOARDING',
                                    conditions='is_door_closed_after_dropoff', after='publish_state')
        self.machine.add_transition('try_transition', 'DEBOARDING', 'PARKING',
                                    conditions='is_door_closed_after_deboarding', after='publish_state')
        self.machine.add_transition('try_transition', 'PARKING', 'IDLE',
                                    conditions='is_goal_reached_for_parking', after='publish_and_stop')

        # Draw FSM diagram
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

        # Publish initial state
        self.publish_state()

    def is_booking_received(self):
        # Check if booking request received
        return self.booking_request is True

    def is_goal_reached_for_pickup(self):
        # Check if reached pickup goal
        return self.goal_reached_for_pickup

    def is_door_closed_after_boarding(self):
        # Check if door closed after boarding
        if self.door_open is False:
            self.door_open = None
            return True
        self.door_open = None
        return False

    def is_door_closed_after_dropoff(self):
        # Check if reached dropoff and door closed
        if self.goal_reached_for_dropoff:
            self.goal_reached_for_dropoff = None
            self.door_open = None
            return True
        self.door_open = None
        return False

    def is_door_closed_after_deboarding(self):
        # Check if doors closed after deboarding
        if self.door_open is False:
            self.door_open = None
            return True
        self.door_open = None
        return False

    def is_goal_reached_for_parking(self):
        # Check if parking goal reached
        if self.goal_reached_for_parking:
            self.goal_reached_for_parking = None
            return True
        return False

    def publish_state(self):
        # Publish current FSM state
        code = STATE_CODES[self.state]
        msg = Int8()
        msg.data = code
        self.node.vehicle_state_pub.publish(msg)
        self.node.get_logger().info(f"/vehicle_state = {code} ({self.state})")

        # Update FSM visualization
        if HAS_PYGRAPHVIZ:
            try:
                g = self.machine.get_graph()
                g.draw("/tmp/decision_fsm.png", prog="dot")
            except Exception:
                pass

    def publish_and_stop(self):
        # Publish final IDLE and stop FSM
        self.publish_state()
        self.finished = True
        self.node.get_logger().info("FSM reached final IDLE. Stopping state updates.")

    def monitor(self):
        # Periodically check and trigger transitions
        prev_state = self.state
        while rclpy.ok() and not self.finished:
            self.try_transition()
            if self.state != prev_state:
                self.publish_state()
                prev_state = self.state
            time.sleep(0.5)


class DecisionUnitNode(Node):
    """ROS 2 Node wrapper for the Decision Unit FSM."""

    def __init__(self):
        super().__init__('decision_core_fsm')
        self.vehicle_state_pub = self.create_publisher(Int8, '/vehicle_state', 10)
        self.fsm = DecisionUnit(self)

        # Subscriptions
        self.create_subscription(Bool, '/booking_request', self.booking_cb, 10)
        self.create_subscription(Bool, '/goal_reached', self.goal_cb, 10)
        self.create_subscription(Bool, '/door_open', self.door_cb, 10)

        self.get_logger().info("Decision Unit FSM (transitions-based) started.")

    def booking_cb(self, msg):
        # Handle booking request
        self.fsm.booking_request = msg.data

    def goal_cb(self, msg):
        # Handle goal reached based on current state
        if self.fsm.state == 'DRIVING_TO_PICKUP' and msg.data:
            self.fsm.goal_reached_for_pickup = True
        elif self.fsm.state == 'DRIVING_TO_DROPOFF' and msg.data:
            self.fsm.goal_reached_for_dropoff = True
        elif self.fsm.state == 'PARKING' and msg.data:
            self.fsm.goal_reached_for_parking = True
        self.fsm.goal_reached = msg.data

    def door_cb(self, msg):
        # Handle door state updates
        self.fsm.door_open = msg.data


def main():
    # Entry point for ROS node
    rclpy.init()
    node = DecisionUnitNode()

    # Start FSM monitor thread
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

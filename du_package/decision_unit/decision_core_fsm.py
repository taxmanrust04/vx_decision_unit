#!/usr/bin/env python3
 
import rclpy
import time
import threading
from transitions.extensions import GraphMachine
from std_msgs.msg import Bool, Int8
from rclpy.node import Node
 
 
STATE_CODES = {
    'IDLE': 0,
    'DRIVING_TO_PICKUP': 1,
    'BOARDING': 2,
    'DRIVING_TO_DROPOFF': 3,
    'DEBOARDING': 4,
    'PARKING': 5
}
 
 
class DecisionUnit:
 
    states = list(STATE_CODES.keys())
 
    def __init__(self, node):
        self.node = node
 
        # booking event
        self.booking_request = False
        self.last_booking_msg = False
 
        # blackboard flags
        self.goal_reached_for_pickup = False
        self.goal_reached_for_dropoff = False
        self.goal_reached_for_parking = False
        self.door_open = None
 
        # deboarding tracking
        self.deboarding_door_opened = False
        self.deboarding_finished = False
 
        self.machine = GraphMachine(
            model=self,
            states=self.states,
            initial='IDLE',
            ignore_invalid_triggers=True
        )
 
        # ---------- TRANSITIONS ----------
 
        self.machine.add_transition(
            'try_transition',
            'IDLE',
            'DRIVING_TO_PICKUP',
            conditions='is_booking_received',
            after='consume_booking_and_publish'
        )
 
        self.machine.add_transition(
            'try_transition',
            'DRIVING_TO_PICKUP',
            'BOARDING',
            conditions='is_goal_reached_for_pickup',
            after='publish_state'
        )
 
        self.machine.add_transition(
            'try_transition',
            'BOARDING',
            'DRIVING_TO_DROPOFF',
            conditions='is_door_closed_after_boarding',
            after='publish_state'
        )
 
        self.machine.add_transition(
            'try_transition',
            'DRIVING_TO_DROPOFF',
            'DEBOARDING',
            conditions='is_goal_reached_for_dropoff',
            after='start_deboarding'
        )
 
        #  CANCEL TRANSITION (NEW)
        self.machine.add_transition(
            'cancel_ride',
            'DRIVING_TO_PICKUP',
            'PARKING',
            after='publish_state'
        )
 
        self.machine.add_transition(
            'try_transition',
            'DEBOARDING',
            'DRIVING_TO_PICKUP',
            conditions='should_drive_again',
            after='consume_booking_and_publish'
        )
 
        self.machine.add_transition(
            'try_transition',
            'DEBOARDING',
            'PARKING',
            conditions='should_park',
            after='publish_state'
        )
 
        self.machine.add_transition(
            'try_transition',
            'PARKING',
            'DRIVING_TO_PICKUP',
            conditions='is_booking_received',
            after='consume_booking_and_publish'
        )
 
        self.machine.add_transition(
            'try_transition',
            'PARKING',
            'IDLE',
            conditions='is_goal_reached_for_parking',
            after='reset_and_publish'
        )
 
        self.publish_state()
 
    # ---------- CONDITIONS ----------
 
    def is_booking_received(self):
        return self.booking_request
 
    def should_drive_again(self):
        return self.deboarding_finished and self.booking_request
 
    def should_park(self):
        return self.deboarding_finished and not self.booking_request
 
    def is_goal_reached_for_pickup(self):
        if self.goal_reached_for_pickup:
            self.goal_reached_for_pickup = False
            return True
        return False
 
    def is_goal_reached_for_dropoff(self):
        if self.goal_reached_for_dropoff:
            self.goal_reached_for_dropoff = False
            return True
        return False
 
    def is_door_closed_after_boarding(self):
        if self.door_open is False:
            self.door_open = None
            return True
        return False
 
    def is_goal_reached_for_parking(self):
        if self.goal_reached_for_parking:
            self.goal_reached_for_parking = False
            return True
        return False
 
    # ---------- ACTIONS ----------
 
    def start_deboarding(self):
        self.deboarding_door_opened = False
        self.deboarding_finished = False
        self.publish_state()
 
    def consume_booking_and_publish(self):
        self.booking_request = False
        self.goal_reached_for_pickup = False
        self.goal_reached_for_dropoff = False
        self.door_open = None
        self.deboarding_door_opened = False
        self.deboarding_finished = False
        self.publish_state()
 
    def publish_state(self):
        code = STATE_CODES[self.state]
        msg = Int8()
        msg.data = code
        self.node.vehicle_state_pub.publish(msg)
        self.node.get_logger().info(
            f"/vehicle_state = {code} ({self.state})"
        )
 
    def reset_and_publish(self):
        self.booking_request = False
        self.goal_reached_for_pickup = False
        self.goal_reached_for_dropoff = False
        self.goal_reached_for_parking = False
        self.door_open = None
        self.deboarding_finished = False
        self.publish_state()
 
    # ---------- MONITOR ----------
 
    def monitor(self):
        while rclpy.ok():
            if self.state == 'DEBOARDING':
                if self.door_open is True:
                    self.deboarding_door_opened = True
                if self.deboarding_door_opened and self.door_open is False:
                    self.deboarding_finished = True
 
            self.try_transition()
            time.sleep(0.5)
 
 
class DecisionUnitNode(Node):
 
    def __init__(self):
        super().__init__('decision_core_fsm')
 
        self.vehicle_state_pub = self.create_publisher(
            Int8, '/vehicle_state', 10)
 
        self.fsm = DecisionUnit(self)
 
        self.create_subscription(
            Bool, '/booking_request', self.booking_cb, 10)
 
        self.create_subscription(
            Bool, '/goal_reached', self.goal_cb, 10)
 
        self.create_subscription(
            Bool, '/door_open', self.door_cb, 10)
 
        # 🔴 CANCEL SUBSCRIBER (NEW)
        self.create_subscription(
            Bool, '/booking_cancelled', self.cancel_cb, 10)
 
    # ---------- CALLBACKS ----------
 
    def booking_cb(self, msg):
        if msg.data:
            self.fsm.booking_request = True
        self.fsm.last_booking_msg = msg.data
 
    def cancel_cb(self, msg):
        if msg.data and self.fsm.state == 'DRIVING_TO_PICKUP':
            self.get_logger().warn(
                "CANCEL RECEIVED → DRIVING_TO_PICKUP → PARKING"
            )
            self.fsm.booking_request = False
            self.fsm.cancel_ride()
 
    def goal_cb(self, msg):
        if self.fsm.state == 'DRIVING_TO_PICKUP' and msg.data:
            self.fsm.goal_reached_for_pickup = True
        elif self.fsm.state == 'DRIVING_TO_DROPOFF' and msg.data:
            self.fsm.goal_reached_for_dropoff = True
        elif self.fsm.state == 'PARKING' and msg.data:
            self.fsm.goal_reached_for_parking = True
 
    def door_cb(self, msg):
        self.fsm.door_open = msg.data
 
 
def main():
    rclpy.init()
    node = DecisionUnitNode()
 
    monitor_thread = threading.Thread(
        target=node.fsm.monitor, daemon=True)
    monitor_thread.start()
 
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
        monitor_thread.join()
 
 
if __name__ == '__main__':
    main()
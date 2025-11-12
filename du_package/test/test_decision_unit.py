# import pytest
# from unittest.mock import MagicMock, patch
# from std_msgs.msg import Bool, Int8
# from decision_unit.decision_core_fsm import DecisionUnit, DecisionUnitNode

# @pytest.fixture
# def mock_node():
#     node = MagicMock()
#     node.vehicle_state_pub = MagicMock()
#     node.get_logger = MagicMock()
#     return node


# def test_publish_and_stop_sets_finished(mock_node):
#     fsm = DecisionUnit(mock_node)
#     fsm.state = 'PARKING'
#     fsm.goal_reached_for_parking = True
#     fsm.publish_and_stop()
#     assert fsm.finished is True
#     mock_node.vehicle_state_pub.publish.assert_called()


# def test_monitor_stops_when_finished(mock_node):
#     fsm = DecisionUnit(mock_node)
#     fsm.finished = True
#     fsm.monitor()  # Should exit immediately
#     assert fsm.finished


# def test_monitor_changes_state_and_publishes(mock_node):
#     fsm = DecisionUnit(mock_node)
#     fsm.booking_request = True
#     with patch('time.sleep', return_value=None):
#         with patch('rclpy.ok', return_value=False):  # simulate shutdown
#             fsm.monitor()
#     mock_node.vehicle_state_pub.publish.assert_called()


# def test_decision_unit_node_initialization():
#     """Patch ROS2 init so node creation works without real rclpy context."""
#     with patch('rclpy.init', return_value=None), \
#          patch('rclpy.ok', return_value=True), \
#          patch.object(DecisionUnitNode, 'create_publisher', return_value=MagicMock()), \
#          patch.object(DecisionUnitNode, 'create_subscription', return_value=None):
#         node = DecisionUnitNode()
#         assert isinstance(node.fsm, DecisionUnit)
#         assert node.vehicle_state_pub is not None


# def test_booking_callback_sets_flag(mock_node):
#     node = DecisionUnitNode.__new__(DecisionUnitNode)
#     node.fsm = DecisionUnit(mock_node)
#     msg = Bool()
#     msg.data = True
#     DecisionUnitNode.booking_cb(node, msg)
#     assert node.fsm.booking_request is True


# def test_goal_callback_routes_flags_correctly(mock_node):
#     node = DecisionUnitNode.__new__(DecisionUnitNode)
#     node.fsm = DecisionUnit(mock_node)

#     # Pickup
#     node.fsm.state = 'DRIVING_TO_PICKUP'
#     msg = Bool(); msg.data = Trueimport pytest
# from unittest.mock import MagicMock, patch
# from std_msgs.msg import Bool, Int8
# from decision_unit.decision_core_fsm import DecisionUnit, DecisionUnitNode

# @pytest.fixture
# def mock_node():
#     node = MagicMock()
#     node.vehicle_state_pub = MagicMock()
#     node.get_logger = MagicMock()
#     return node


# def test_publish_and_stop_sets_finished(mock_node):
#     fsm = DecisionUnit(mock_node)
#     fsm.state = 'PARKING'
#     fsm.goal_reached_for_parking = True
#     fsm.publish_and_stop()
#     assert fsm.finished is True
#     mock_node.vehicle_state_pub.publish.assert_called()


# def test_monitor_stops_when_finished(mock_node):
#     fsm = DecisionUnit(mock_node)
#     fsm.finished = True
#     fsm.monitor()  # Should exit immediately
#     assert fsm.finished


# def test_monitor_changes_state_and_publishes(mock_node):
#     fsm = DecisionUnit(mock_node)
#     fsm.booking_request = True
#     with patch('time.sleep', return_value=None):
#         with patch('rclpy.ok', return_value=False):  # simulate shutdown
#             fsm.monitor()
#     mock_node.vehicle_state_pub.publish.assert_called()


# def test_decision_unit_node_initialization():
#     """Patch ROS2 init so node creation works without real rclpy context."""
#     with patch('rclpy.init', return_value=None), \
#          patch('rclpy.ok', return_value=True), \
#          patch.object(DecisionUnitNode, 'create_publisher', return_value=MagicMock()), \
#          patch.object(DecisionUnitNode, 'create_subscription', return_value=None):
#         node = DecisionUnitNode()
#         assert isinstance(node.fsm, DecisionUnit)
#         assert node.vehicle_state_pub is not None


# def test_booking_callback_sets_flag(mock_node):
#     node = DecisionUnitNode.__new__(DecisionUnitNode)
#     node.fsm = DecisionUnit(mock_node)
#     msg = Bool()
#     msg.data = True
#     DecisionUnitNode.booking_cb(node, msg)
#     assert node.fsm.booking_request is True


# def test_goal_callback_routes_flags_correctly(mock_node):
#     node = DecisionUnitNode.__new__(DecisionUnitNode)
#     node.fsm = DecisionUnit(mock_node)

#     # Pickup
#     node.fsm.state = 'DRIVING_TO_PICKUP'
#     msg = Bool(); msg.data = True
#     DecisionUnitNode.goal_cb(node, msg)
#     assert node.fsm.goal_reached_for_pickup

#     # Dropoff
#     node.fsm.state = 'DRIVING_TO_DROPOFF'
#     DecisionUnitNode.goal_cb(node, msg)
#     assert node.fsm.goal_reached_for_dropoff

#     # Parking
#     node.fsm.state = 'PARKING'
#     DecisionUnitNode.goal_cb(node, msg)
#     assert node.fsm.goal_reached_for_parking


# def test_door_callback_sets_flag(mock_node):
#     node = DecisionUnitNode.__new__(DecisionUnitNode)
#     node.fsm = DecisionUnit(mock_node)
#     msg = Bool(); msg.data = False
#     DecisionUnitNode.door_cb(node, msg)
#     assert node.fsm.door_open is False


# def test_main_runs_and_shuts_down_cleanly():
#     """Patch out full ROS stack and run main() to hit shutdown logic."""
#     with patch('rclpy.init', return_value=None), \
#          patch('rclpy.ok', return_value=False), \
#          patch('rclpy.spin', side_effect=KeyboardInterrupt), \
#          patch('rclpy.shutdown', return_value=None), \
#          patch('threading.Thread.start', return_value=None), \
#          patch.object(DecisionUnitNode, 'destroy_node', return_value=None), \
#          patch.object(DecisionUnitNode, '__init__', return_value=None):
#         # manually patch __init__ to avoid real ROS node creation
#         from decision_unit.decision_core_fsm import main
#         main()  # should not raise
#     DecisionUnitNode.goal_cb(node, msg)
#     assert node.fsm.goal_reached_for_pickup

#     # Dropoff
#     node.fsm.state = 'DRIVING_TO_DROPOFF'
#     DecisionUnitNode.goal_cb(node, msg)
#     assert node.fsm.goal_reached_for_dropoff

#     # Parking
#     node.fsm.state = 'PARKING'
#     DecisionUnitNode.goal_cb(node, msg)
#     assert node.fsm.goal_reached_for_parking


# def test_door_callback_sets_flag(mock_node):
#     node = DecisionUnitNode.__new__(DecisionUnitNode)
#     node.fsm = DecisionUnit(mock_node)
#     msg = Bool(); msg.data = False
#     DecisionUnitNode.door_cb(node, msg)
#     assert node.fsm.door_open is False


# def test_main_runs_and_shuts_down_cleanly():
#     """Patch out full ROS stack and run main() to hit shutdown logic."""
#     with patch('rclpy.init', return_value=None), \
#          patch('rclpy.ok', return_value=False), \
#          patch('rclpy.spin', side_effect=KeyboardInterrupt), \
#          patch('rclpy.shutdown', return_value=None), \
#          patch('threading.Thread.start', return_value=None), \
#          patch.object(DecisionUnitNode, 'destroy_node', return_value=None), \
#          patch.object(DecisionUnitNode, '__init__', return_value=None):
#         # manually patch __init__ to avoid real ROS node creation
#         from decision_unit.decision_core_fsm import main
#         main()  # should not raise    #6 passed 2 failed test main runs and initialization



# #!/usr/bin/env python3
# import pytest
# from unittest.mock import MagicMock, patch
# from std_msgs.msg import Bool, Int8
# from decision_unit.decision_core_fsm import DecisionUnit, DecisionUnitNode, STATE_CODES


# # ---------------- FIXTURE ----------------

# @pytest.fixture
# def fsm():
#     """Fixture for initializing DecisionUnit with mocked node."""
#     class MockNode:
#         def __init__(self):
#             self.vehicle_state_pub = MagicMock()
#             self.get_logger = MagicMock(return_value=MagicMock(info=print, warn=print, error=print))
#     node = MockNode()
#     return DecisionUnit(node)


# # ---------------- US 1.1 to 1.7 TESTS ----------------

# def test_state_machine_structure(fsm):
#     """FSM defines required states and transition triggers."""
#     required_states = ['IDLE', 'DRIVING_TO_PICKUP', 'BOARDING', 'DRIVING_TO_DROPOFF', 'DEBOARDING', 'PARKING']
#     assert set(required_states).issubset(fsm.states)
#     all_triggers = list(fsm.machine.events.keys())
#     assert 'try_transition' in all_triggers


# def test_idle_to_driving_transition(fsm):
#     """Test transition from IDLE to DRIVING_TO_PICKUP."""
#     fsm.state = 'IDLE'
#     fsm.booking_request = True
#     fsm.try_transition()
#     assert fsm.state == 'DRIVING_TO_PICKUP'
#     fsm.node.vehicle_state_pub.publish.assert_called()


# def test_driving_to_boarding_transition(fsm):
#     """Test transition from DRIVING_TO_PICKUP to BOARDING."""
#     fsm.state = 'DRIVING_TO_PICKUP'
#     fsm.goal_reached_for_pickup = True
#     fsm.try_transition()
#     assert fsm.state == 'BOARDING'
#     fsm.node.vehicle_state_pub.publish.assert_called()


# def test_boarding_to_driving_dropoff_transition(fsm):
#     """Test transition from BOARDING to DRIVING_TO_DROPOFF."""
#     fsm.state = 'BOARDING'
#     fsm.door_open = False
#     fsm.try_transition()
#     assert fsm.state == 'DRIVING_TO_DROPOFF'
#     fsm.node.vehicle_state_pub.publish.assert_called()


# def test_driving_to_deboarding_transition(fsm):
#     """Test transition from DRIVING_TO_DROPOFF to DEBOARDING."""
#     fsm.state = 'DRIVING_TO_DROPOFF'
#     fsm.goal_reached_for_dropoff = True
#     fsm.try_transition()
#     assert fsm.state == 'DEBOARDING'
#     fsm.node.vehicle_state_pub.publish.assert_called()


# def test_deboarding_to_parking_transition(fsm):
#     """Test transition from DEBOARDING to PARKING."""
#     fsm.state = 'DEBOARDING'
#     fsm.door_open = False
#     fsm.try_transition()
#     assert fsm.state == 'PARKING'
#     fsm.node.vehicle_state_pub.publish.assert_called()


# def test_parking_to_idle_transition(fsm):
#     """Test transition from PARKING to IDLE."""
#     fsm.state = 'PARKING'
#     fsm.goal_reached_for_parking = True
#     fsm.try_transition()
#     assert fsm.state == 'IDLE'
#     fsm.node.vehicle_state_pub.publish.assert_called()
#     assert fsm.finished is True


# def test_full_fsm_sequence(fsm):
#     """Test the entire FSM transition sequence."""
#     sequence = [
#         ('IDLE', 'booking_request', True, 'DRIVING_TO_PICKUP'),
#         ('DRIVING_TO_PICKUP', 'goal_reached_for_pickup', True, 'BOARDING'),
#         ('BOARDING', 'door_open', False, 'DRIVING_TO_DROPOFF'),
#         ('DRIVING_TO_DROPOFF', 'goal_reached_for_dropoff', True, 'DEBOARDING'),
#         ('DEBOARDING', 'door_open', False, 'PARKING'),
#         ('PARKING', 'goal_reached_for_parking', True, 'IDLE'),
#     ]
#     for state, flag, value, expected in sequence:
#         fsm.state = state
#         setattr(fsm, flag, value)
#         fsm.try_transition()
#         assert fsm.state == expected
#         fsm.node.vehicle_state_pub.publish.assert_called()
#         fsm.node.vehicle_state_pub.publish.reset_mock()


# def test_publish_state_sends_correct_code(fsm):
#     """Test if publish_state sends the correct Int8 message."""
#     fsm.state = 'BOARDING'
#     fsm.publish_state()
#     msg = fsm.node.vehicle_state_pub.publish.call_args[0][0]
#     assert isinstance(msg, Int8)
#     assert msg.data == STATE_CODES['BOARDING']


# # ---------------- EXTRA COVERAGE TESTS ----------------

# def test_publish_and_stop_sets_finished(fsm):
#     """Test that publish_and_stop sets the 'finished' flag."""
#     fsm.state = 'PARKING'
#     fsm.goal_reached_for_parking = True
#     fsm.publish_and_stop()
#     assert fsm.finished is True
#     fsm.node.vehicle_state_pub.publish.assert_called()


# def test_monitor_stops_when_finished(fsm):
#     """Test that monitor stops if finished is True."""
#     fsm.finished = True
#     fsm.monitor()  # should exit immediately
#     assert fsm.finished


# def test_monitor_changes_state_and_publishes(fsm):
#     """Test that monitor changes state when conditions are met."""
#     fsm.booking_request = True
#     with patch('time.sleep', return_value=None), patch('rclpy.ok', return_value=False):
#         fsm.monitor()
#     fsm.node.vehicle_state_pub.publish.assert_called()


# # ---------------- CALLBACK TESTS ----------------

# def test_booking_callback_sets_flag():
#     """Test if booking callback sets the correct flag."""
#     node = DecisionUnitNode.__new__(DecisionUnitNode)
#     node.fsm = DecisionUnit(MagicMock())
#     msg = Bool(); msg.data = True
#     DecisionUnitNode.booking_cb(node, msg)
#     assert node.fsm.booking_request is True


# def test_goal_callback_routes_flags_correctly():
#     """Test if goal callback routes flags correctly based on state."""
#     node = DecisionUnitNode.__new__(DecisionUnitNode)
#     node.fsm = DecisionUnit(MagicMock())
#     msg = Bool(); msg.data = True

#     node.fsm.state = 'DRIVING_TO_PICKUP'
#     DecisionUnitNode.goal_cb(node, msg)
#     assert node.fsm.goal_reached_for_pickup

#     node.fsm.state = 'DRIVING_TO_DROPOFF'
#     DecisionUnitNode.goal_cb(node, msg)
#     assert node.fsm.goal_reached_for_dropoff

#     node.fsm.state = 'PARKING'
#     DecisionUnitNode.goal_cb(node, msg)
#     assert node.fsm.goal_reached_for_parking


# def test_door_callback_sets_flag():
#     """Test if door callback correctly sets the flag."""
#     node = DecisionUnitNode.__new__(DecisionUnitNode)
#     node.fsm = DecisionUnit(MagicMock())
#     msg = Bool(); msg.data = False
#     DecisionUnitNode.door_cb(node, msg)
#     assert node.fsm.door_open is False


# # ---------------- FIXED TESTS (ROS2 INIT & MAIN) ----------------

# def test_decision_unit_node_initialization():
#     """Test node initialization with mocked logger."""
#     fake_logger = MagicMock()
#     with patch('rclpy.node.Node.__init__', return_value=None), \
#          patch.object(DecisionUnitNode, 'create_publisher', return_value=MagicMock()), \
#          patch.object(DecisionUnitNode, 'create_subscription', return_value=None):
#         node = DecisionUnitNode.__new__(DecisionUnitNode)
#         # Inject fake logger to avoid initialization issues
#         node._logger = fake_logger
#         node.get_logger = MagicMock(return_value=fake_logger)
#         DecisionUnitNode.__init__(node)
#         assert hasattr(node, 'fsm')
#         assert isinstance(node.fsm, DecisionUnit)
#         assert node.vehicle_state_pub is not None


# def test_main_runs_and_shuts_down_cleanly():
#     """Test that main runs and shuts down without ROS2 context."""
#     mock_node = MagicMock()
#     mock_node.fsm = MagicMock()
#     mock_thread = MagicMock()

#     with patch('rclpy.init', return_value=None), \
#          patch('rclpy.spin', side_effect=KeyboardInterrupt), \
#          patch('rclpy.shutdown', return_value=None), \
#          patch('threading.Thread', return_value=mock_thread), \
#          patch('decision_unit.decision_core_fsm.DecisionUnitNode', return_value=mock_node):
#         from decision_unit.decision_core_fsm import main
#         main()

#     mock_thread.start.assert_called_once()
#     mock_node.destroy_node.assert_called_once()


# # ---------------- GRAPHVIZ TESTS ----------------

# def test_graphviz_behavior(monkeypatch):
#     """Cover both success and failure paths of FSM graph export."""
#     import decision_unit.decision_core_fsm as fsm_mod
#     node = MagicMock()
#     fake_logger = MagicMock()
#     node.get_logger.return_value = fake_logger

#     fake_graph = MagicMock()
#     fake_graph.draw = MagicMock()
#     fake_machine = MagicMock(get_graph=MagicMock(return_value=fake_graph))

#     # Success path (Graphviz is available)
#     fsm_mod.HAS_PYGRAPHVIZ = True
#     with patch('decision_unit.decision_core_fsm.GraphMachine', return_value=fake_machine):
#         fsm_mod.DecisionUnit(node)
#         fake_graph.draw.assert_called_once()

#     # Failure path (graph export fails)
#     fake_graph.draw.side_effect = Exception("graph export failed")
#     with patch('decision_unit.decision_core_fsm.GraphMachine', return_value=fake_machine):
#         fsm_mod.DecisionUnit(node)
#         fake_logger.error.assert_called()

#     # Missing PyGraphviz (warning path)
#     fsm_mod.HAS_PYGRAPHVIZ = False
#     with patch('decision_unit.decision_core_fsm.GraphMachine', return_value=fake_machine):
#         fsm_mod.DecisionUnit(node)
#         fake_logger.warn.assert_called()


# # ---------------- FINAL COVERAGE TESTS ----------------

# def test_auth_callback_sets_flag():
#     """Ensure auth_cb sets FSM.auth_status correctly."""
#     node = DecisionUnitNode.__new__(DecisionUnitNode)
#     node.fsm = DecisionUnit(MagicMock())
#     msg = MagicMock()
#     msg.data = True
#     DecisionUnitNode.auth_cb(node, msg)
#     assert node.fsm.auth_status is True


# def test_monitor_exits_when_ros_not_ok():
#     """Ensure monitor exits immediately when rclpy.ok() is False."""
#     fsm = DecisionUnit(MagicMock())
#     with patch('rclpy.ok', return_value=False):
#         fsm.monitor()
#     assert not fsm.finished


# #!/usr/bin/env python3
# import pytest
# from unittest.mock import MagicMock, patch
# from std_msgs.msg import Bool, Int8
# from decision_unit.decision_core_fsm import DecisionUnit, DecisionUnitNode, STATE_CODES


# # ---------------- FIXTURE ----------------

# @pytest.fixture
# def fsm():
#     """Fixture for initializing DecisionUnit with mocked node."""
#     class MockNode:
#         def __init__(self):
#             self.vehicle_state_pub = MagicMock()
#             self.get_logger = MagicMock(return_value=MagicMock(info=print, warn=print, error=print))
#     node = MockNode()
#     return DecisionUnit(node)


# # ---------------- US 1.1 to 1.7 TESTS ----------------

# def test_fsm_transitions_and_publish(fsm):
#     """Test FSM structure, transitions and publish messages for all states."""
#     # State Machine structure and transition checks
#     required_states = ['IDLE', 'DRIVING_TO_PICKUP', 'BOARDING', 'DRIVING_TO_DROPOFF', 'DEBOARDING', 'PARKING']
#     assert set(required_states).issubset(fsm.states)
#     all_triggers = list(fsm.machine.events.keys())
#     assert 'try_transition' in all_triggers

#     # Full FSM sequence transitions (testing transitions and state publishing)
#     sequence = [
#         ('IDLE', 'booking_request', True, 'DRIVING_TO_PICKUP'),
#         ('DRIVING_TO_PICKUP', 'goal_reached_for_pickup', True, 'BOARDING'),
#         ('BOARDING', 'door_open', False, 'DRIVING_TO_DROPOFF'),
#         ('DRIVING_TO_DROPOFF', 'goal_reached_for_dropoff', True, 'DEBOARDING'),
#         ('DEBOARDING', 'door_open', False, 'PARKING'),
#         ('PARKING', 'goal_reached_for_parking', True, 'IDLE'),
#     ]
#     for state, flag, value, expected in sequence:
#         fsm.state = state
#         setattr(fsm, flag, value)
#         fsm.try_transition()
#         assert fsm.state == expected
#         fsm.node.vehicle_state_pub.publish.assert_called()
#         fsm.node.vehicle_state_pub.publish.reset_mock()

#     # Test publish state sends the correct message
#     fsm.state = 'BOARDING'
#     fsm.publish_state()
#     msg = fsm.node.vehicle_state_pub.publish.call_args[0][0]
#     assert isinstance(msg, Int8)
#     assert msg.data == STATE_CODES['BOARDING']


# def test_publish_and_stop_sets_finished(fsm):
#     """Test publish_and_stop sets finished flag and publishes message correctly."""
#     fsm.state = 'PARKING'
#     fsm.goal_reached_for_parking = True
#     fsm.publish_and_stop()
#     assert fsm.finished is True
#     fsm.node.vehicle_state_pub.publish.assert_called()


# def test_monitor_behavior(fsm):
#     """Test monitor function behavior, stopping when finished and triggering state changes."""
#     # Test that monitor stops if finished is True
#     fsm.finished = True
#     fsm.monitor()  # should exit immediately
#     assert fsm.finished

#     # Test that monitor changes state when conditions are met
#     fsm.booking_request = True
#     with patch('time.sleep', return_value=None), patch('rclpy.ok', return_value=False):
#         fsm.monitor()
#     fsm.node.vehicle_state_pub.publish.assert_called()


# # ---------------- CALLBACK TESTS ----------------

# def test_callbacks(fsm):
#     """Test booking_cb, goal_cb, and door_cb work together and correctly update FSM flags."""
#     node = DecisionUnitNode.__new__(DecisionUnitNode)
#     node.fsm = DecisionUnit(MagicMock())

#     # Test booking callback sets the correct flag
#     msg = Bool(); msg.data = True
#     DecisionUnitNode.booking_cb(node, msg)
#     assert node.fsm.booking_request is True

#     # Test goal callback updates flags based on state
#     msg.data = True
#     node.fsm.state = 'DRIVING_TO_PICKUP'
#     DecisionUnitNode.goal_cb(node, msg)
#     assert node.fsm.goal_reached_for_pickup

#     node.fsm.state = 'DRIVING_TO_DROPOFF'
#     DecisionUnitNode.goal_cb(node, msg)
#     assert node.fsm.goal_reached_for_dropoff

#     node.fsm.state = 'PARKING'
#     DecisionUnitNode.goal_cb(node, msg)
#     assert node.fsm.goal_reached_for_parking

#     # Test door callback correctly sets the flag
#     msg.data = False
#     DecisionUnitNode.door_cb(node, msg)
#     assert node.fsm.door_open is False


# # ---------------- FIXED TESTS (ROS2 INIT & MAIN) ----------------

# def test_decision_unit_node_initialization_and_monitoring():
#     """Test node initialization with mocked logger and monitor function."""
#     fake_logger = MagicMock()
#     with patch('rclpy.node.Node.__init__', return_value=None), \
#          patch.object(DecisionUnitNode, 'create_publisher', return_value=MagicMock()), \
#          patch.object(DecisionUnitNode, 'create_subscription', return_value=None):
#         node = DecisionUnitNode.__new__(DecisionUnitNode)
#         node._logger = fake_logger
#         node.get_logger = MagicMock(return_value=fake_logger)
#         DecisionUnitNode.__init__(node)
#         assert hasattr(node, 'fsm')
#         assert isinstance(node.fsm, DecisionUnit)
#         assert node.vehicle_state_pub is not None

#     # Simulate monitor exit with rclpy.ok()
#     fsm = node.fsm
#     with patch('rclpy.ok', return_value=False):
#         fsm.monitor()
#     assert not fsm.finished


# def test_main_runs_and_shuts_down_cleanly():
#     """Test that main runs and shuts down cleanly without real ROS2 context."""
#     mock_node = MagicMock()
#     mock_node.fsm = MagicMock()
#     mock_thread = MagicMock()

#     with patch('rclpy.init', return_value=None), \
#          patch('rclpy.spin', side_effect=KeyboardInterrupt), \
#          patch('rclpy.shutdown', return_value=None), \
#          patch('threading.Thread', return_value=mock_thread), \
#          patch('decision_unit.decision_core_fsm.DecisionUnitNode', return_value=mock_node):
#         from decision_unit.decision_core_fsm import main
#         main()

#     mock_thread.start.assert_called_once()
#     mock_node.destroy_node.assert_called_once()


# # ---------------- GRAPHVIZ TESTS ----------------

# def test_graphviz_behavior(monkeypatch):
#     """Cover both success and failure paths of FSM graph export."""
#     import decision_unit.decision_core_fsm as fsm_mod
#     node = MagicMock()
#     fake_logger = MagicMock()
#     node.get_logger.return_value = fake_logger

#     fake_graph = MagicMock()
#     fake_graph.draw = MagicMock()
#     fake_machine = MagicMock(get_graph=MagicMock(return_value=fake_graph))

#     # Initialize the mock state to a valid initial state
#     fsm_mod.DecisionUnit.state = 'IDLE'  # Ensure state is set

#     # Success path (Graphviz is available)
#     fsm_mod.HAS_PYGRAPHVIZ = True
#     with patch('decision_unit.decision_core_fsm.GraphMachine', return_value=fake_machine):
#         fsm_mod.DecisionUnit(node)  # Initialize DecisionUnit
#         fake_graph.draw.assert_called_once()

#     # Failure path (graph export fails)
#     fake_graph.draw.side_effect = Exception("graph export failed")
#     with patch('decision_unit.decision_core_fsm.GraphMachine', return_value=fake_machine):
#         fsm_mod.DecisionUnit(node)
#         fake_logger.error.assert_called()

#     # Missing PyGraphviz (warning path)
#     fsm_mod.HAS_PYGRAPHVIZ = False
#     with patch('decision_unit.decision_core_fsm.GraphMachine', return_value=fake_machine):
#         fsm_mod.DecisionUnit(node)
#         fake_logger.warn.assert_called()

#!/usr/bin/env python3
import pytest
from unittest.mock import MagicMock, patch
from std_msgs.msg import Bool, Int8
from decision_unit.decision_core_fsm import DecisionUnit, DecisionUnitNode, STATE_CODES


# ---------------- FIXTURE ----------------

@pytest.fixture
def fsm():
    """Fixture for initializing DecisionUnit with mocked node."""
    class MockNode:
        def __init__(self):
            self.vehicle_state_pub = MagicMock()
            self.get_logger = MagicMock(return_value=MagicMock(info=print, warn=print, error=print))
    node = MockNode()
    return DecisionUnit(node)


# ---------------- US 1.1 to 1.7 TESTS ----------------

def test_fsm_transitions_and_publish(fsm):
    """Test FSM structure, transitions and publish messages for all states."""
    # State Machine structure and transition checks
    required_states = ['IDLE', 'DRIVING_TO_PICKUP', 'BOARDING', 'DRIVING_TO_DROPOFF', 'DEBOARDING', 'PARKING']
    assert set(required_states).issubset(fsm.states)
    all_triggers = list(fsm.machine.events.keys())
    assert 'try_transition' in all_triggers

    # Full FSM sequence transitions (testing transitions and state publishing)
    sequence = [
        ('IDLE', 'booking_request', True, 'DRIVING_TO_PICKUP'),
        ('DRIVING_TO_PICKUP', 'goal_reached_for_pickup', True, 'BOARDING'),
        ('BOARDING', 'door_open', False, 'DRIVING_TO_DROPOFF'),
        ('DRIVING_TO_DROPOFF', 'goal_reached_for_dropoff', True, 'DEBOARDING'),
        ('DEBOARDING', 'door_open', False, 'PARKING'),
        ('PARKING', 'goal_reached_for_parking', True, 'IDLE'),
    ]
    for state, flag, value, expected in sequence:
        fsm.state = state
        setattr(fsm, flag, value)
        fsm.try_transition()
        assert fsm.state == expected
        fsm.node.vehicle_state_pub.publish.assert_called()
        fsm.node.vehicle_state_pub.publish.reset_mock()

    # Test publish state sends the correct message
    fsm.state = 'BOARDING'
    fsm.publish_state()
    msg = fsm.node.vehicle_state_pub.publish.call_args[0][0]
    assert isinstance(msg, Int8)
    assert msg.data == STATE_CODES['BOARDING']


def test_publish_and_stop_sets_finished(fsm):
    """Test publish_and_stop sets finished flag and publishes message correctly."""
    fsm.state = 'PARKING'
    fsm.goal_reached_for_parking = True
    fsm.publish_and_stop()
    assert fsm.finished is True
    fsm.node.vehicle_state_pub.publish.assert_called()


def test_monitor_behavior(fsm):
    """Test monitor function behavior, stopping when finished and triggering state changes."""
    # Test that monitor stops if finished is True
    fsm.finished = True
    fsm.monitor()  # should exit immediately
    assert fsm.finished

    # Test that monitor changes state when conditions are met
    fsm.booking_request = True
    with patch('time.sleep', return_value=None), patch('rclpy.ok', return_value=False):
        fsm.monitor()
    fsm.node.vehicle_state_pub.publish.assert_called()


# ---------------- CALLBACK TESTS ----------------

def test_callbacks(fsm):
    """Test booking_cb, goal_cb, and door_cb work together and correctly update FSM flags."""
    node = DecisionUnitNode.__new__(DecisionUnitNode)
    node.fsm = DecisionUnit(MagicMock())

    # Test booking callback sets the correct flag
    msg = Bool(); msg.data = True
    DecisionUnitNode.booking_cb(node, msg)
    assert node.fsm.booking_request is True

    # Test goal callback updates flags based on state
    msg.data = True
    node.fsm.state = 'DRIVING_TO_PICKUP'
    DecisionUnitNode.goal_cb(node, msg)
    assert node.fsm.goal_reached_for_pickup

    node.fsm.state = 'DRIVING_TO_DROPOFF'
    DecisionUnitNode.goal_cb(node, msg)
    assert node.fsm.goal_reached_for_dropoff

    node.fsm.state = 'PARKING'
    DecisionUnitNode.goal_cb(node, msg)
    assert node.fsm.goal_reached_for_parking

    # Test door callback correctly sets the flag
    msg.data = False
    DecisionUnitNode.door_cb(node, msg)
    assert node.fsm.door_open is False


# ---------------- FIXED TESTS (ROS2 INIT & MAIN) ----------------

def test_decision_unit_node_initialization_and_monitoring():
    """Test node initialization with mocked logger and monitor function."""
    fake_logger = MagicMock()
    with patch('rclpy.node.Node.__init__', return_value=None), \
         patch.object(DecisionUnitNode, 'create_publisher', return_value=MagicMock()), \
         patch.object(DecisionUnitNode, 'create_subscription', return_value=None):
        node = DecisionUnitNode.__new__(DecisionUnitNode)
        node._logger = fake_logger
        node.get_logger = MagicMock(return_value=fake_logger)
        DecisionUnitNode.__init__(node)
        assert hasattr(node, 'fsm')
        assert isinstance(node.fsm, DecisionUnit)
        assert node.vehicle_state_pub is not None

    # Simulate monitor exit with rclpy.ok()
    fsm = node.fsm
    with patch('rclpy.ok', return_value=False):
        fsm.monitor()
    assert not fsm.finished


def test_main_runs_and_shuts_down_cleanly():
    """Test that main runs and shuts down cleanly without real ROS2 context."""
    mock_node = MagicMock()
    mock_node.fsm = MagicMock()
    mock_thread = MagicMock()

    with patch('rclpy.init', return_value=None), \
         patch('rclpy.spin', side_effect=KeyboardInterrupt), \
         patch('rclpy.shutdown', return_value=None), \
         patch('threading.Thread', return_value=mock_thread), \
         patch('decision_unit.decision_core_fsm.DecisionUnitNode', return_value=mock_node):
        from decision_unit.decision_core_fsm import main
        main()

    mock_thread.start.assert_called_once()
    mock_node.destroy_node.assert_called_once()


# ---------------- GRAPHVIZ TESTS ----------------

def test_graphviz_behavior(monkeypatch):
    """Cover both success and failure paths of FSM graph export."""
    import decision_unit.decision_core_fsm as fsm_mod
    node = MagicMock()
    fake_logger = MagicMock()
    node.get_logger.return_value = fake_logger

    fake_graph = MagicMock()
    fake_graph.draw = MagicMock()  # Mock draw method
    fake_machine = MagicMock(get_graph=MagicMock(return_value=fake_graph))

    # Initialize state and pygraphviz behavior
    fsm_mod.HAS_PYGRAPHVIZ = True  # Mock that pygraphviz is available
    fsm_mod.DecisionUnit.state = 'IDLE'  # Initialize state to 'IDLE'

    # Success path (Graphviz is available)
    with patch('decision_unit.decision_core_fsm.GraphMachine', return_value=fake_machine):
        fsm_mod.DecisionUnit(node)  # Initialize DecisionUnit
        # Ensure draw is called only once
        assert fake_graph.draw.call_count == 1
        fake_graph.draw.assert_called_once_with('/tmp/decision_fsm.png', prog='dot')

    # Failure path (graph export fails)
    fake_graph.draw.side_effect = Exception("graph export failed")
    with patch('decision_unit.decision_core_fsm.GraphMachine', return_value=fake_machine):
        fsm_mod.DecisionUnit(node)
        fake_logger.error.assert_called_once()

    # Missing PyGraphviz (warning path)
    fsm_mod.HAS_PYGRAPHVIZ = False
    with patch('decision_unit.decision_core_fsm.GraphMachine', return_value=fake_machine):
        fsm_mod.DecisionUnit(node)
        fake_logger.warn.assert_called_once()


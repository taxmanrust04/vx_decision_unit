# Decision Unit 

## 📄 Overview

The Decision Unit Module consumes a fused view of the environment, proximity alerts, obstacle detection flags, and authentication status to make high‑level driving decisions. It publishes vehicle state commands, emergency stop signals, and access control commands for downstream planning and execution components.

---

## 📑 Table of Contents

- [Architecture](#architecture)
- [Component Functionalities](#component-functionalities)
- [Node Details](#node-details)
- [Installation, Usage & Testing](#installation-usage--testing)
- [License](#license)

---

## 🧱 Architecture

```mermaid
graph LR
  subgraph Inputs
    FS["Sensor Fusion<br/>(/fused_msgs/EnvironmentState)"]
    IR["IR Sensor<br/>(/ir/proximity_alert: sensor_msgs/Range)"]
    OB["Obstacle Detector<br/>(/obstacle_detected: std_msgs/Bool)"]
    AU["Auth Module<br/>(/auth_status: std_msgs/Bool)"]
  end

  DU["Decision Unit Module"]

  subgraph Outputs
    PP["Path Planning Component<br/>(/vehicle_state: std_msgs/Bool)"]
    PE["Path Execution Controller<br/>(/emergency_stop: std_msgs/Bool)"]
    AC["Access Controller<br/>(/access_command: std_msgs/UInt8)"]
  end

  FS --> DU
  IR --> DU
  OB --> DU
  AU --> DU

  DU --> PP
  DU --> PE
  DU --> AC

  class DU redRounded
  class FS,IR,OB,AU,PP,PE,AC graySquare

  classDef redRounded fill:#ff4d4d,stroke:#333,stroke-width:2px,rx:20,ry:20,color:#fff
  classDef graySquare fill:#dddddd,stroke:#222,stroke-width:1px,rx:5,ry:5,color:#000

  ```

## ⚙️ Component Functionalities

- **Evaluates Surroundings**  
  Analyzes incoming fused perception data from `/fused_msgs/EnvironmentState` to identify nearby dynamic and static obstacles for situational awareness.

- **Assesses Immediate Proximity**  
  Uses IR sensor input from `/ir/proximity_alert` to detect objects in close range and flag potential collision threats.

- **Processes Obstacle Alerts**  
  Interprets discrete alerts from `/obstacle_detected` (`std_msgs/Bool`) to trigger reactive behaviors like halting or re-evaluating movement intent.

- **Monitors Authentication Status**  
  Listens to `/auth_status` (`std_msgs/Bool`) to ensure vehicle commands are only executed if the user is authenticated.

- **Generates Vehicle Motion Commands**  
  Based on environmental, proximity, and authentication inputs, it determines and publishes `/vehicle_state` to guide the Path Planning module (drive/stop decision).

- **Issues Emergency Stop Signals**  
  Sends a high-priority `/emergency_stop` signal to the Path Execution Controller to halt motion instantly when conditions become unsafe.

- **Controls Access Mechanisms**  
  Publishes an `/access_command` (`std_msgs/UInt8`) to the Access Controller to lock/unlock doors or enable/disable system access based on decision logic.
  

## 🧩 Node Details

**Node**: `decision_unit_node`

| Topic                          | I/O    | Type                          | Description                                        |
|--------------------------------|--------|-------------------------------|----------------------------------------------------|
| `/fused_msgs/EnvironmentState` | Input  | `fused_msgs/EnvironmentState` | Fused perception from all sensors.                 |
| `/ir/proximity_alert`          | Input  | `sensor_msgs/Range`           | IR sensor proximity readings.                      |
| `/obstacle_detected`           | Input  | `std_msgs/Bool`               | Obstacle detector flag.                            |
| `/auth_status`                 | Input  | `std_msgs/Bool`               | Authentication status from security module.        |
| `/vehicle_state`               | Output | `std_msgs/Bool`               | Command to Path Planning (drive vs. idle).         |
| `/emergency_stop`              | Output | `std_msgs/Bool`               | Immediate stop signal to Path Execution Controller.|
| `/access_command`              | Output | `std_msgs/UInt8`              | Access control code (e.g., lock/unlock).           |


## 🧪 Installation, Usage & Testing

```bash
# Clone the repository
git clone https://git.hs-coburg.de/par8824s/decision_unit_module.git
cd decision_unit_module

# Build and source
colcon build --packages-select decision_unit_module
source install/setup.bash

# Run the node
ros2 run decision_unit_module decision_unit_node

# Monitor topics
ros2 topic echo /fused_msgs/EnvironmentState
ros2 topic echo /ir/proximity_alert
ros2 topic echo /obstacle_detected
ros2 topic echo /auth_status
ros2 topic echo /vehicle_state
ros2 topic echo /emergency_stop
ros2 topic echo /access_command

# Run unit tests
colcon test --packages-select decision_unit_module

## 📝 License
http://www.apache.org/licenses/LICENSE-2.0


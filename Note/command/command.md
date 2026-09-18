1. rosdep install -i --from-path src --rosdistro $ROS_DISTRO -y
   扫描我这个 ROS 2 工作空间 `src` 里的所有源码包，按照 Jazzy 的规则检查它们缺少的依赖，并自动安装，过程中不要再问我确认。

1. gz topic -l
2. ros2 control list_controllers
3. ros2 control list_controllers -v 

4. 控制夹抓关: ros2 action send_goal /gripper_action_controller/gripper_cmd control_msgs/action/GripperCommand "{command: {position: -0.7, max_effort: 5.0}}"

5. 控制夹抓开: ros2 action send_goal /gripper_action_controller/gripper_cmd control_msgs/action/GripperCommand "{command: {position: 0.0, max_effort: 5.0}}"

6. ros2 control set_controller_state gripper_action_controller inactive

7.列出所有已加载并准备好供 ROSS 2 控制控制器管理器使用的可用硬件组件: 
ros2 control list_hardware_components

8. ros2 topic list

9. ros2 action list

 
10. 机械臂运动到某个特定的位置
其中 "/arm_controller/follow_joint_trajectory" 是用来控制机械臂的
ros2 action send_goal /arm_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{
  trajectory: {
    joint_names: ['link1_to_link2', 'link2_to_link3', 'link3_to_link4', 'link4_to_link5', 'link5_to_link6', 'link6_to_link6_flange'],
    points: [{
      positions: [1.345, -1.23, 0.264, -0.296, 0.389, -1.5],
      velocities: [],
      accelerations: [],
      effort: [],
      time_from_start: {sec: 3, nanosec: 0}
    }]
  }
}"

11. 恢复原位
ros2 action send_goal /arm_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{
  trajectory: {
    joint_names: ['link1_to_link2', 'link2_to_link3', 'link3_to_link4', 'link4_to_link5', 'link5_to_link6', 'link6_to_link6_flange'],
    points: [{
      positions: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      velocities: [],
      accelerations: [],
      effort: [],
      time_from_start: {sec: 1, nanosec: 500000000}
    }]
  }
}"

11. ros2 action info /arm_controller/follow_joint_trajectory

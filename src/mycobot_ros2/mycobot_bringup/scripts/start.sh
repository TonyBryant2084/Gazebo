# 总启动脚本

# 定义一个 Bash 函数
cleanup() {
    # 命令1: 相关进程清除函数声明
    echo "Cleaning up..."
    # 命令2: 暂停 5s
    sleep 5.0
    # 遍历进程 → 查看每个进程的完整启动命令 → 如果命令中包含 ros2、gazebo、gz、nav2、rviz2、moveit、move_group、basic_navigator 等任意关键词 → 用 -9 强制杀掉该进程
    # -f: 匹配启动该进程时的完整命令行，只要命令行中包含关键词，就可能被匹配
    pkill -9 -f "ros2|gazebo|gz|nav2|amcl|bt_navigator|nav_to_pose|rviz2|assisted_teleop|cmd_vel_relay|robot_state_publisher|joint_state_publisher|move_to_free|mqtt|autodock|cliff_detection|moveit|move_group|basic_navigator"
}

# 设置cleanup()的触发条件
# 1. Ctrl+C → SIGINT → 执行 cleanup
# 2. pkill xxx（默认不带 -9）→ SIGTERM → 执行 cleanup
trap 'cleanup' SIGINT SIGTERM

# 启动 Gazebo 进行仿真
echo "Launching Gazebo simulation..."

# 1. use
# 2. condition
# 3. robot
# 注意：在只启动 robot_description.launch..py 时，由于没有启动 Gazebo，没有外部时间(topic: /clock)，所以不要使用 use_sim_time(use_sim_time = flase)， 让 rsp, jsp, rviz2 听系统时间
ros2 launch mycobot_gazebo gazebo.launch.py \
    use_sim_time:=true \
    use_rsp:=true \
    use_jsp:=true \
    use_rviz2:=true \
    condition_robot_description:=true \
    condition_ros2_controllers:=true \
    condition_gazebo:=true \
    condition_topic_bridge:=true \
    condition_image_bridge:=true \
    condition_spawner:=true \
    robot_name:="mycobot_280" \
    robot_x:=0.0 \
    robot_y:=0.0 \
    robot_z:=0.0 \
    robot_roll:=0.0 \
    robot_pitch:=0.0 \
    robot_yaw:=0.0 \
# ==================== Path：路径 ====================

# 查找 ROS 2 Package 的 share 文件夹路径
from launch_ros.substitutions import FindPackageShare

# 拼接路径
from launch.substitutions import PathJoinSubstitution


# ==================== Launch Argument：启动参数 ====================

# 声明 Launch 参数
from launch.actions import DeclareLaunchArgument

# 获取 Launch 参数的值
from launch.substitutions import LaunchConfiguration


# ==================== Substitution：替换 ====================

# 执行命令，并把命令输出作为一个值
from launch.substitutions import Command

# 指定参数值的数据类型
from launch_ros.parameter_descriptions import ParameterValue


# ==================== Action：动作 ====================

# LaunchDescription：管理整个 Launch 文件中的 Action
from launch import LaunchDescription

# Node：启动 ROS 2 节点
from launch_ros.actions import Node

# ExecuteProcess：启动外部进程
from launch.actions import ExecuteProcess

# IncludeLaunchDescription：包含并执行其他 Launch 文件
from launch.actions import IncludeLaunchDescription

# PythonLaunchDescriptionSource：
# 将 Python Launch 文件转换为 LaunchDescription 来源
from launch.launch_description_sources import PythonLaunchDescriptionSource

# TimerAction：延迟执行 Action
from launch.actions import TimerAction

# RegisterEventHandler：注册事件处理器
from launch.actions import RegisterEventHandler

# AppendEnvironmentVariable：向环境变量追加内容
from launch.actions import AppendEnvironmentVariable


# ==================== Condition：条件 ====================

# 根据条件决定 Action 是否执行
from launch.conditions import IfCondition


# ==================== Event Handler：事件处理 ====================

# OnProcessExit：进程退出时触发事件
from launch.event_handlers import OnProcessExit


# ==================== LaunchDescription ====================

# 启动生成函数
def generate_launch_description():

    # Path:

    # 1. Share Path
    #   1) mycobot_description/share
    share_path_mycobot_description = FindPackageShare(package="mycobot_description")

    #   2) mycobot_moveit2_config
    share_path_mycobot_moveit2_config = FindPackageShare(package="mycobot_moveit2_config")

    #   3) ros_gz_sim/share
    share_path_ros_gz_sim = FindPackageShare(package="ros_gz_sim")

    #   3) mycobot_gazebo/share
    share_path_mycobot_gazebo = FindPackageShare(package="mycobot_gazebo")

    # 2. File Path
    #   1) topic_bridge
    file_path_topic_bridge = PathJoinSubstitution([
        share_path_mycobot_gazebo,
        "config",
        "topic_bridge.yaml"
    ])
    #   2) world
    file_path_world = PathJoinSubstitution([
        share_path_mycobot_gazebo,
        "worlds",
        "pick_and_place.world"
    ])

    # Launch Arguments: 

    # 1. use
    #   1) use_sim_time
    argument_use_sim_time = DeclareLaunchArgument(
        name="use_sim_time",
        default_value="true"
    )
    use_sim_time = LaunchConfiguration("use_sim_time")

    #   2) use_rsp
    argument_use_rsp = DeclareLaunchArgument(
        name="use_rsp",
        default_value="true"
    )
    use_rsp = LaunchConfiguration("use_rsp")  

    #   3) use_jsp
    argument_use_jsp = DeclareLaunchArgument(
        name="use_jsp",
        default_value="true"
    )
    use_jsp = LaunchConfiguration("use_jsp") 

    #   4) use_rviz2
    argument_use_rviz2 = DeclareLaunchArgument(
        name="use_rviz2",
        default_value="true"
    )
    use_rviz2 = LaunchConfiguration("use_rviz2")    

    # 2. condition
    
    #   1) robot_description
    argument_condition_robot_description = DeclareLaunchArgument(
        name="condition_robot_description",
        default_value="true"
    )
    condition_robot_description = LaunchConfiguration("condition_robot_description")
    #   2) ros2_controllers
    argument_condition_ros2_controllers = DeclareLaunchArgument(
        name="condition_ros2_controllers",
        default_value="true"
    )
    condition_ros2_controllers = LaunchConfiguration("condition_ros2_controllers")
    #   3) gazebo
    argument_condition_gazebo = DeclareLaunchArgument(
        name="condition_gazebo",
        default_value="true"
    )
    condition_gazebo = LaunchConfiguration("condition_gazebo")
    #   4) topic_bridge
    argument_condition_topic_bridge = DeclareLaunchArgument(
        name="condition_topic_bridge",
        default_value="true"
    )
    condition_topic_bridge = LaunchConfiguration("condition_topic_bridge")
    #   5) image_bridge
    argument_condition_image_bridge = DeclareLaunchArgument(
        name="condition_image_bridge",
        default_value="true"
    )
    condition_image_bridge = LaunchConfiguration("condition_image_bridge")
    #   6) spawner
    argument_condition_spawner = DeclareLaunchArgument(
        name="condition_spawner",
        default_value="true"
    )
    condition_spawner = LaunchConfiguration("condition_spawner")

    # 3. robot
    #   1) robot_name
    argument_robot_name = DeclareLaunchArgument(
        name="robot_name",
        default_value="mycobot_280"
    )
    robot_name = LaunchConfiguration("robot_name")
    #   2) x
    argument_robot_x = DeclareLaunchArgument(
        name="robot_x",
        default_value="0.0"
    )
    robot_x = LaunchConfiguration("robot_x")
    #   3) y
    argument_robot_y = DeclareLaunchArgument(
        name="robot_y",
        default_value="0.0"
    )
    robot_y = LaunchConfiguration("robot_y")
    #   5) z
    argument_robot_z = DeclareLaunchArgument(
        name="robot_z",
        default_value="0.0"
    )
    robot_z = LaunchConfiguration("robot_z")
    #   6) roll
    argument_robot_roll = DeclareLaunchArgument(
        name="robot_roll",
        default_value="0.0"
    )
    robot_roll = LaunchConfiguration("robot_roll")
    #   7) pitch
    argument_robot_pitch = DeclareLaunchArgument(
        name="robot_pitch",
        default_value="0.0"
    )
    robot_pitch = LaunchConfiguration("robot_pitch")
    #   8) yaw
    argument_robot_yaw = DeclareLaunchArgument(
        name="robot_yaw",
        default_value="0.0"
    )
    robot_yaw = LaunchConfiguration("robot_yaw")

    # Actions:

    # 1. 机器人描述 (Launch)
    #   1) 机器人状态发布: robot_state_publisher
    #   2) 关节状态发布: joint_state_publisher
    #   3) 机器人模型可视化: rviz2
    #   4) ROS2_Control 的控制器配置文件: ros2_controllers.yaml
    action_robot_description = IncludeLaunchDescription(
        # 1. 启动文件
        # 将 python 文件 变成 ROS2 Launch 系统能够使用的 启动描述文件
        launch_description_source = PythonLaunchDescriptionSource(
            launch_file_path = PathJoinSubstitution(
                [
                    share_path_mycobot_description,
                    "launch",
                    "robot_description.launch.py"
                ]
            )
        ),
        # 2. 启动参数
        launch_arguments=[
            # 0) 使用仿真时间
            ("use_sim_time", use_sim_time),
            # 1) robot_state_publisher
            ("use_rsp", use_rsp),
            # 2) joint_state_publisher
            ("use_jsp", use_jsp),
            # 3) rviz2
            ("use_rviz2", use_rviz2)
        ],
        # 3. 启动条件
        condition=IfCondition(condition_robot_description)
    )

    # 2. 机器人控制器 (Launch)
    action_ros2_controllers = IncludeLaunchDescription(
        # 1. 启动文件
        # 将 python 文件 变成 ROS2 Launch 系统能够使用的 启动描述文件
        launch_description_source=PythonLaunchDescriptionSource(
            launch_file_path=PathJoinSubstitution(
                [
                    share_path_mycobot_moveit2_config,
                    "launch",
                    "ros2_controllers.launch.py"
                ]
            )
        ),
        # 2. 启动条件
        condition=IfCondition(condition_ros2_controllers)
    )

    action_append_environment_variable = AppendEnvironmentVariable(
        # 1. Gazebo Sim 的环境变量
        "GZ_SIM_RESOURCE_PATH",
        # 2. 追加的 Gazebo 模型目录
        PathJoinSubstitution([
            share_path_mycobot_gazebo,
            "world"
        ])
    )

    # 3. Gazebo (Launch)
    action_gazebo = IncludeLaunchDescription(
        # 1. 启动文件
        # 将 python 文件 变成 ROS2 Launch 系统能够使用的 启动描述文件
        launch_description_source=PythonLaunchDescriptionSource(
            launch_file_path=PathJoinSubstitution(
                [
                    share_path_ros_gz_sim,
                    "launch",
                    "gz_sim.launch.py"
                ]
            )
        ),
        # 2. 启动参数
        launch_arguments=[
            ("gz_args", [" -r -v 4 ", file_path_world])
        ],
        # 3. 启动条件
        condition=IfCondition(condition_gazebo)
    )

    # 4. 话题数据桥梁 (Node)
    action_parameter_bridge = Node(
        # 1. 包名
        package="ros_gz_bridge",
        # 2. 可执行程序
        executable="parameter_bridge",
        # 3. 参数
        parameters=[{
            "config_file": file_path_topic_bridge
        }],
        # 4. 输出
        output="screen",
        # 5. 启动条件
        condition=IfCondition(condition_topic_bridge)
    )

    # 5. 图像数据桥梁 (Node)
    action_image_bridge = Node(
        # 1. 包名
        package="ros_gz_image",
        # 2. 可执行程序
        executable="image_bridge",
        # 3. 命令
        arguments=[
            # Gazebo 内部话题:
            # 1. 深度图像: 每个像素存距离相机的米数
            "/camera_head/depth_image",
            # 2. RGB 彩色图像: 像素彩色画面
            "/camera_head/image"
        ],
        # 4. 话题重映射配置
        remappings=[
            # (Gazebo 内部话题名称, ROS2 内部话题名称)
            ("/camera_head/depth_image", "/camera_head/depth/image_rect_raw"),
            ('/camera_head/image', '/camera_head/color/image_raw')
        ],
        # 5. 输出
        output="screen",
        # 6. 启动条件
        condition=IfCondition(condition_image_bridge)
    )

    # 6. Gazebo 机器人生成器
    action_spawner = Node(
        # 1. 包名
        package="ros_gz_sim",
        # 2. 可执行程序
        executable="create",
        # 3. 命令
        arguments=[
            # 告诉 "create" 程序不要直接从文件读取机器人模型，而是从 robot_state_publisher 发布的 /robot_description 这个话题来读取
            '-topic', '/robot_description',
            # 把创建出来的机器人模型命名为什么
            '-name', robot_name,
            # 如果这个名字已经存在，允许 Gazebo 自动换一个名字
            '-allow_renaming', 'true',
            # 放在 Gazebo 世界坐标系的哪个位置
            '-x', robot_x,
            '-y', robot_y,
            '-z', robot_z,
            # 以什么样的位姿摆放
            '-R', robot_roll,
            '-P', robot_pitch,
            '-Y', robot_yaw
        ],
        # 4. 普通打印和报错信息, 全部实时打印到终端
        output="screen",
        # 5. 启动条件
        condition=IfCondition(condition_spawner)
    )

    # Action Container
    ld = LaunchDescription()

    # Launch Arguments

    # 1. use
    ld.add_action(argument_use_sim_time)
    ld.add_action(argument_use_rsp)
    ld.add_action(argument_use_jsp)
    ld.add_action(argument_use_rviz2)

    # 2. condition
    ld.add_action(argument_condition_robot_description)
    ld.add_action(argument_condition_ros2_controllers)
    ld.add_action(argument_condition_gazebo)
    ld.add_action(argument_condition_topic_bridge)
    ld.add_action(argument_condition_image_bridge)
    ld.add_action(argument_condition_spawner)

    # 3. robot
    ld.add_action(argument_robot_name)
    ld.add_action(argument_robot_x)
    ld.add_action(argument_robot_y)
    ld.add_action(argument_robot_z)
    ld.add_action(argument_robot_roll)
    ld.add_action(argument_robot_pitch)
    ld.add_action(argument_robot_yaw)

    # Actions
    # ① action_robot_description  ← 已经搞懂
    # ② action_gazebo             ← 下一步
    # ③ action_parameter_bridge       ← 再下一步
    # ④ action_spawner             ← 再下一步
    # ⑤ action_ros2_controllers    ← 最后
    # ⑥ action_image_bridge        ← 暂时不加

    # 1. Launch File
    ld.add_action(action_robot_description)
    # ld.add_action(action_ros2_controllers)
    # ld.add_action(action_append_environment_variable)
    ld.add_action(action_gazebo)

    # 2. Node
    ld.add_action(action_parameter_bridge)
    # ld.add_action(action_image_bridge)
    ld.add_action(action_spawner)

    # 返回完整的 LaunchDescription
    return ld

    


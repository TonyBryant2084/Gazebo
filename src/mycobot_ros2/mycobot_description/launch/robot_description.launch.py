# ==================== Path：路径 ====================

# 1. 查找 ROS 2 Package 的 share 文件夹路径
from launch_ros.substitutions import FindPackageShare

# 2. 拼接路径
from launch.substitutions import PathJoinSubstitution


# ==================== Arguments：Launch 参数 ====================

# 1. 声明 Launch 参数
from launch.actions import DeclareLaunchArgument

# 2. 获取 Launch 参数的值
from launch.substitutions import LaunchConfiguration


# ==================== Command：命令 ====================

# 1. 执行命令，并把命令的输出结果作为一个值使用
from launch.substitutions import Command

# 2. 指定参数值的类型
from launch_ros.parameter_descriptions import ParameterValue

# 3. 执行命令并启动外部进程
from launch.actions import ExecuteProcess


# ==================== Action：动作 ====================

# 1. LaunchDescription：Action 容器
from launch import LaunchDescription

# 2. Node：启动 ROS 2 节点
from launch_ros.actions import Node

# 3. IncludeLaunchDescription：包含其他 Launch 文件
from launch.actions import IncludeLaunchDescription

# 4. PythonLaunchDescriptionSource：
#    将 Python Launch 文件转换为 LaunchDescription 来源
from launch.launch_description_sources import PythonLaunchDescriptionSource

# 5. DeclareLaunchArgument：声明 Launch 参数
from launch.actions import DeclareLaunchArgument

# 6. ExecuteProcess：启动外部进程
from launch.actions import ExecuteProcess


# ==================== Condition：条件 ====================

# 1. 根据条件决定 Action 是否执行
from launch.conditions import IfCondition

def generate_launch_description():

    # Path

    # 1. Share Path
    #   1) mycobot_description/share
    share_path_mycobot_description = FindPackageShare(package="mycobot_description")

    # 2. File Path
    #   1) file_path_xacro
    file_path_xacro = PathJoinSubstitution([
        share_path_mycobot_description,
        "urdf",
        "robots",
        "mycobot_280.urdf.xacro"        
    ])
    #   2) file_path_rviz
    file_path_rviz2 = PathJoinSubstitution([
        share_path_mycobot_description,
        "rviz",
        "mycobot_280_description.rviz"
    ])

    # Launch Arguments

    # 1. use
    #   1) use_sim_time
    argument_use_sim_time = DeclareLaunchArgument(
        name="use_sim_time",
        default_value="true"
    )
    use_sim_time = LaunchConfiguration("use_sim_time")

    # 2. condition
    #   1) robot_state_publisher
    argument_use_rsp = DeclareLaunchArgument(
        name="use_rsp",
        default_value="true"
    )
    use_rsp = LaunchConfiguration("use_rsp")
    #   2) joint_state_publisher
    argument_use_jsp = DeclareLaunchArgument(
        name="use_jsp",
        default_value="true"
    )
    use_jsp = LaunchConfiguration("use_jsp")
    #   3) rviz2
    argument_use_rviz2 = DeclareLaunchArgument(
        name="use_rviz2",
        default_value="true"
    )
    use_rviz2 = LaunchConfiguration("use_rviz2")
    


    # 3. robot
    #   1) name: 机器人名字
    argument_robot_name = DeclareLaunchArgument(
        name="robot_name",
        default_value="mycobot_280"
    )
    robot_name = LaunchConfiguration("robot_name")
    #   2) prefix: 前缀名称 (多机器人场景)
    argument_robot_prefix = DeclareLaunchArgument(
        name="robot_prefix",
        default_value=""
    )
    robot_prefix = LaunchConfiguration("robot_prefix")
    #   3) add_world: 添加 world 根 link
    argument_robot_add_world = DeclareLaunchArgument(
        name="robot_add_world",
        default_value="true"
    )
    robot_add_world = LaunchConfiguration("robot_add_world")
    #   4) base_link: 机器人底座名称
    argument_robot_base_link = DeclareLaunchArgument(
        name="robot_base_link",
        default_value="base_link"
    )
    robot_base_link = LaunchConfiguration("robot_base_link")
    #   5) base_type: 机器人底座形状 
    argument_robot_base_type = DeclareLaunchArgument(
        name="robot_base_type",
        default_value="g_shape"
    )
    robot_base_type = LaunchConfiguration("robot_base_type")
    #   6) flange_link: 安装末端装置(gripper, camera)的实体 link 
    argument_robot_flange_link = DeclareLaunchArgument(
        name="robot_flange_link",
        default_value="link6_flange"
    )
    robot_flange_link = LaunchConfiguration("robot_flange_link")
    #   7) gripper_type: 夹爪类型
    argument_robot_gripper_type = DeclareLaunchArgument(
        name="robot_gripper_type",
        default_value="adaptive_gripper"
    )
    robot_gripper_type = LaunchConfiguration("robot_gripper_type")
    #   8) use_camera: 是否使用相机 
    argument_robot_use_camera = DeclareLaunchArgument(
        name="robot_use_camera",
        default_value="false"
    )
    robot_use_camera = LaunchConfiguration("robot_use_camera")
    #   9) use_gazebo: 是否使用 Gazebo 仿真 
    argument_robot_use_gazebo = DeclareLaunchArgument(
        name="robot_use_gazebo",
        default_value="true"
    )
    robot_use_gazebo = LaunchConfiguration("robot_use_gazebo")
    #   9) use_gripper: 是否使用夹爪 
    argument_robot_use_gripper = DeclareLaunchArgument(
        name="robot_use_gripper",
        default_value="true"
    )
    robot_use_gripper = LaunchConfiguration("robot_use_gripper")

    # File 
    robot_description = ParameterValue(
        Command([
            # 1. xacro 命令
            "xacro", " ", 
            # 2. xacro 文件位置
            file_path_xacro, " ",
            # 3. 机器人名字
            " robot_name:=", robot_name,
            # 4. 名称前缀
            " prefix:=", robot_prefix,
            # 5. 是否添加 world 根 link
            " add_world:=", robot_add_world,
            # 6. 机器人底座 link 名称
            " base_link:=", robot_base_link,
            # 7. 底座类型
            " base_type:=", robot_base_type,
            # 8. 安装末端的实体link
            " flange_link:=", robot_flange_link,
            # 9. 夹爪类型
            " gripper_type:=", robot_gripper_type,
            # 10. 是否使用相机
            " use_camera:=", robot_use_camera,
            # 11. 是否使用 Gazebo 仿真
            " use_gazebo:=", robot_use_gazebo,
            # 12. 是否使用夹爪
            " use_gripper:=", robot_use_gripper
        ]),
        value_type=str
    )

    # Actions

    # 1. robot_state_publisher (Node)
    action_robot_state_publisher = Node(
        # 1. 包名
        package="robot_state_publisher",
        # 2. 可执行程序
        executable="robot_state_publisher",
        # 3. 参数
        parameters=[{
            "robot_description": robot_description,
            "use_sim_time": use_sim_time
        }],
        # 4. 普通打印和报错信息, 全部实时打印到终端
        output="screen",
        # 5. 启动条件
        condition=IfCondition(use_rsp)
    )
    # 2. joint_state_publisher
    action_joint_state_publisher = Node(
        # 1. 包名
        package="joint_state_publisher_gui",
        # 2. 可执行程序
        executable="joint_state_publisher_gui",
        # 3. 参数
        parameters=[{
            "use_sim_time": use_sim_time
        }],
        # 4. 普通打印和报错信息, 全部实时打印到终端
        output="screen",
        # 5. 启动条件
        condition=IfCondition(use_jsp)
    ) 
    # 3. rviz2
    action_rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", file_path_rviz2],
        parameters=[{"use_sim_time": use_sim_time}],
        output="screen",
        condition=IfCondition(use_rviz2)
    )

    # Action Container
    ld = LaunchDescription()

    # Launch Arguments

    # 1. use
    ld.add_action(argument_use_sim_time)

    # 2. condition
    ld.add_action(argument_use_rsp)
    ld.add_action(argument_use_jsp)
    ld.add_action(argument_use_rviz2)

    # 3. robot
    ld.add_action(argument_robot_name)
    ld.add_action(argument_robot_prefix)
    ld.add_action(argument_robot_add_world)
    ld.add_action(argument_robot_base_link)
    ld.add_action(argument_robot_base_type)
    ld.add_action(argument_robot_flange_link)
    ld.add_action(argument_robot_gripper_type)
    ld.add_action(argument_robot_use_camera)
    ld.add_action(argument_robot_use_gazebo)
    ld.add_action(argument_robot_use_gripper)

    # Actions
    # 1. Node
    ld.add_action(action_robot_state_publisher)
    ld.add_action(action_joint_state_publisher)
    ld.add_action(action_rviz2)

    return ld
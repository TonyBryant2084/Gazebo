# os
import os

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

# 7. OpaqueFunction：执行自定义 Python 函数
from launch.actions import OpaqueFunction


# ==================== Condition：条件 ====================

# 1. 根据条件决定 Action 是否执行
from launch.conditions import IfCondition

# Robot Arguments
ROBOT_ARGUMENTS = [
    # 3. robot
    #   1) name: 机器人名字
    DeclareLaunchArgument(
        name="robot_name",
        default_value="mycobot_280"
    ),

    #   2) prefix: 前缀名称 (多机器人场景)
    DeclareLaunchArgument(
        name="robot_prefix",
        default_value=""
    ),

    #   3) add_world: 添加 world 根 link
    DeclareLaunchArgument(
        name="robot_add_world",
        default_value="true"
    ),

    #   4) base_link: 机器人底座名称
    DeclareLaunchArgument(
        name="robot_base_link",
        default_value="base_link"
    ),

    #   5) base_type: 机器人底座形状 
    DeclareLaunchArgument(
        name="robot_base_type",
        default_value="g_shape"
    ),

    #   6) flange_link: 安装末端装置(gripper, camera)的实体 link 
    DeclareLaunchArgument(
        name="robot_flange_link",
        default_value="link6_flange"
    ),

    #   7) gripper_type: 夹爪类型
    DeclareLaunchArgument(
        name="robot_gripper_type",
        default_value="adaptive_gripper"
    ),

    #   8) use_camera: 是否使用相机 
    DeclareLaunchArgument(
        name="robot_use_camera",
        default_value="false"
    ),

    #   9) use_gazebo: 是否使用 Gazebo 仿真 
    DeclareLaunchArgument(
        name="robot_use_gazebo",
        default_value="true"
    ),

    #   9) use_gripper: 是否使用夹爪 
    DeclareLaunchArgument(
        name="robot_use_gripper",
        default_value="true"
    )
    
]

# 通过通过模板生成 ros2_controllers 的配置文件
# 其中: 原生 Python 函数（os.path.join、open、str.replace）完全不认识 Substitution 对象，因此必须手动调用 .perform(context) 把占位对象解析成普通字符串(Substitution的最终值)
def generate_ros2_controllers_config(context):

    # 1. prefix: 前缀名称 (多机器人场景)
    robot_prefix = LaunchConfiguration("robot_prefix").perform(context)
    
    # 2. flange_link: 安装末端装置(gripper, camera)的实体 link 
    robot_flange_link = LaunchConfiguration("robot_flange_link").perform(context)

    # 3. name: 机器人名称
    robot_name = LaunchConfiguration("robot_name").perform(context)

    # 4. mycobot_moveit2_config 包的 share 路径
    share_path_mycobot_moveit2_config = FindPackageShare("mycobot_moveit2_config").perform(context)

    # 5. controllers_config 文件夹路径
    dir_path_controllers_config = os.path.join(
        # 1) mycobot_moveit2_config 包的 share 路径
        share_path_mycobot_moveit2_config,
        "config",
        robot_name
    )

    # 6. controllers_config 的 模板路径
    file_path_controllers_config_template = os.path.join(
        # controllers_config 文件夹路径
        dir_path_controllers_config,
        "ros2_controllers_template.yaml"
    )

    # 7. 最终生成的 controllers_config.yaml 的 路径
    file_path_controllers_config = os.path.join(
        # controllers_config 文件夹路径
        dir_path_controllers_config,
        "ros2_controllers.yaml"
    )

    # 8. 读取模板(template_path -> content)
    with open(
        file=file_path_controllers_config_template,
        mode="r",
        encoding="utf-8"
    ) as file:
        content = file.read()

    # 9. 替换模板变量
    content = content.replace(
        "${prefix}",
        robot_prefix
    )
    content = content.replace(
        "${flange_link}",
        robot_flange_link
    )

    # 10. 写入最终的yaml文件
    with open(
        file=file_path_controllers_config,
        mode="w",
        encoding="utf-8"
    ) as file:
        file.write(content)

    # 没有要追加的Action，返回空列表 
    return []



# 生成启动描述
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
    
    

    # Actions

    # 0. OpaqueFunction：运行阶段执行自定义 Python 代码，借助 context 来确定 Substitution 最终的值(Action)
    # 当 "robot_use_gazebo" = true 时, 通过 xacro 命令解析 mycobot_280.urdf.xacro 文件时, 需要 controller_config.yaml 文件, 所以要先创建该文件
    action_controllers_config = OpaqueFunction(
        function=generate_ros2_controllers_config
    )

    # File (非 Action) 
    # 关键: 在 xacro 过程中 如果 "robot_use_gazebo" = true, 则 需要 ros2_controllers.yaml 文件
    robot_description = ParameterValue(
        Command([
            # 1. xacro 命令
            "xacro", " ", 
            # 2. xacro 文件位置
            file_path_xacro, " ",
            # 3. 机器人名字
            " robot_name:=", LaunchConfiguration("robot_name"),
            # 4. 名称前缀
            " prefix:=", LaunchConfiguration("robot_prefix"),
            # 5. 是否添加 world 根 link
            " add_world:=", LaunchConfiguration("robot_add_world"),
            # 6. 机器人底座 link 名称
            " base_link:=", LaunchConfiguration("robot_base_link"),
            # 7. 底座类型
            " base_type:=", LaunchConfiguration("robot_base_type"),
            # 8. 安装末端的实体link
            " flange_link:=", LaunchConfiguration("robot_flange_link"),
            # 9. 夹爪类型
            " gripper_type:=", LaunchConfiguration("robot_gripper_type"),
            # 10. 是否使用相机
            " use_camera:=", LaunchConfiguration("robot_use_camera"),
            # 11. 是否使用 Gazebo 仿真
            " use_gazebo:=", LaunchConfiguration("robot_use_gazebo"),
            # 12. 是否使用夹爪
            " use_gripper:=", LaunchConfiguration("robot_use_gripper")
        ]),
        value_type=str
    )

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
    ld = LaunchDescription(ROBOT_ARGUMENTS)

    # Launch Arguments

    # 1. use
    ld.add_action(argument_use_sim_time)

    # 2. condition
    ld.add_action(argument_use_rsp)
    ld.add_action(argument_use_jsp)
    ld.add_action(argument_use_rviz2)

    # Actions
    # 1. Self-defined python file
    ld.add_action(action_controllers_config)
    # 2. Node
    ld.add_action(action_robot_state_publisher)
    ld.add_action(action_joint_state_publisher)
    ld.add_action(action_rviz2)

    return ld
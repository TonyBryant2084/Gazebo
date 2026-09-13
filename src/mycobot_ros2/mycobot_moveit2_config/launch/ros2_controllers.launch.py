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


# ==================== Condition：条件 ====================

# 根据条件决定 Action 是否执行
from launch.conditions import IfCondition


# ==================== Event Handler：事件处理 ====================

# OnProcessExit：进程退出时触发事件
from launch.event_handlers import OnProcessExit


# ==================== Controller ====================

# controller_manager (Node)
#       │
#       │ 根据配置/YAML知道有哪些 Controller
#       ↓
# 加载 Controller 插件
#       │
#       ├── joint_state_broadcaster (Controller)
#       ├── arm_controller (Controller)
#       └── gripper_action_controller (Controller)
# Controller 不是 Node，所以不是“启动一个 Controller Node”；而是由 controller_manager 这个 Node 加载并激活 Controller 插件


# ==================== LaunchDescription ====================

# 启动生成函数
def generate_launch_description():

    # ==================== Action  ====================

    # 1. 启动机械臂控制器
    action_arm_controller = ExecuteProcess(
        cmd=[
            # ROS2 命令
            "ros2",
            # ROS2 Control 相关命令
            "control",
            # 加载指令控制器
            "load_controller",
            # 指定加载控制器后要设置的状态
            "--set-state",
            # 把控制器设置为 "active" 激活状态
            "active",
            # 要加载的控制器名称
            "arm_controller"
        ],
        output="screen"
    )

    # 2. 启动夹爪控制器
    action_gripper_controller = ExecuteProcess(
        cmd=[
            # ROS2 命令
            "ros2",
            # ROS2 Control 相关命令
            "control",
            # 加载指令控制器
            "load_controller",
            # 指定加载控制器后要设置的状态
            "--set-state",
            # 把控制器设置为 "active" 激活状态
            "active",
            # 要加载的控制器名称
            "gripper_action_controller"
        ],
        output="screen"
    )

    # 3. 启动关节状态广播器
    action_joint_state_broadcaster = ExecuteProcess(
        cmd=[
            # ROS2 命令
            "ros2",
            # ROS2 Control 相关命令
            "control",
            # 加载指令控制器
            "load_controller",
            # 指定加载控制器后要设置的状态
            "--set-state",
            # 把控制器设置为 "active" 激活状态
            "active",
            # 要加载的控制器名称
            "joint_state_broadcaster"
        ],
        output="screen"
    )

    # 4. 延迟启动关节状态广播器
    action_delayed_start = TimerAction(
        # In Seconds
        period=10.0,
        actions=[action_joint_state_broadcaster]
    )

    # 5. 注册用于控制器顺序的事件处理器
    #   1) 关节状态广播器的 Action 启动完成后，再启动机械臂控制器 Action
    action_load_joint_state_broadcaster = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=action_joint_state_broadcaster,
            on_exit=[
                action_arm_controller
            ]
        )
    )
    #   2) 机械臂控制器的 Action 启动完成后，再启动夹爪动作控制器的 Action
    action_load_arm_controller_cmd = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=action_arm_controller,
            on_exit=[
                action_gripper_controller
            ]
        )
    )

    # ==================== Action 容器 ====================

    # Action 容器
    ld = LaunchDescription()

    # Action 添加
    ld.add_action(action_delayed_start)
    ld.add_action(action_load_joint_state_broadcaster)
    ld.add_action(action_load_arm_controller_cmd)

    # 返回完整的 LaunchDescription
    return ld
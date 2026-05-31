import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QGridLayout
from control.state_machine import ControlModule
from control.get_position import get_current_tcp_joint_positions
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("夾娃娃機控制介面")
        self.control_module = ControlModule()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        grid = QGridLayout()
        grid.setSpacing(10)  # 增加元件間距
        grid.setContentsMargins(20, 20, 20, 20)  # 增加內邊距

        # 新增方向按鈕，排列成 3×3 格局：
        # 第一列：左前、前、右前
        self.btn_left_forward = QPushButton("左前")
        self.btn_forward = QPushButton("前")
        self.btn_right_forward = QPushButton("右前")
        # 第二列：左、右（中間留空）
        self.btn_left = QPushButton("左")
        self.btn_right = QPushButton("右")
        # 第三列：左後、後、右後
        self.btn_left_backward = QPushButton("左後")
        self.btn_backward = QPushButton("後")
        self.btn_right_backward = QPushButton("右後")
        
        # 抓取按鈕放置在第四列中間
        self.btn_grab = QPushButton("抓取")
        self.btn_grab.setObjectName("grabButton")

        grid.addWidget(self.btn_left_forward, 0, 0)
        grid.addWidget(self.btn_forward, 0, 1)
        grid.addWidget(self.btn_right_forward, 0, 2)
        grid.addWidget(self.btn_left, 1, 0)
        grid.addWidget(self.btn_right, 1, 2)
        grid.addWidget(self.btn_left_backward, 2, 0)
        grid.addWidget(self.btn_backward, 2, 1)
        grid.addWidget(self.btn_right_backward, 2, 2)
        grid.addWidget(self.btn_grab, 3, 1)

        # 狀態訊息顯示區放在最下方
        self.status_label = QLabel("系統初始化中...")
        self.status_label.setObjectName("statusLabel")
        self.control_module.handle_initial_command()
        grid.addWidget(self.status_label, 4, 0, 1, 3)

        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)
        self.setMinimumSize(400, 500) # 設定最小視窗大小

        # 套用 QSS 美化樣式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QWidget {
                font-family: "Microsoft JhengHei", "PingFang TC", sans-serif;
                font-size: 24px;
                color: #000000;
            }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #dcdfe6;
                border-radius: 10px;
                padding: 15px;
                min-width: 100px;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #ecf5ff;
                border: 1px solid #c6e2ff;
                color: #409eff;
            }
            QPushButton:pressed {
                background-color: #d9ecff;
            }
            QPushButton#grabButton {
                background-color: #67c23a;
                border: 1px solid #67c23a;
                color: #000000;
                font-weight: bold;
            }
            QPushButton#grabButton:hover {
                background-color: #85ce61;
                border: 1px solid #85ce61;
            }
            QPushButton#grabButton:pressed {
                background-color: #5daf34;
            }
            QLabel#statusLabel {
                background-color: #ffffff;
                border: 1px solid #ebeef5;
                border-radius: 8px;
                padding: 12px;
                color: #000000;
                margin-top: 10px;
            }
        """)

        # 各方向按鈕皆以單次點擊事件觸發對應指令
        self.btn_left_forward.clicked.connect(lambda: self.send_command("left_forward"))
        self.btn_forward.clicked.connect(lambda: self.send_command("forward"))
        self.btn_right_forward.clicked.connect(lambda: self.send_command("right_forward"))
        self.btn_left.clicked.connect(lambda: self.send_command("left"))
        self.btn_right.clicked.connect(lambda: self.send_command("right"))
        self.btn_left_backward.clicked.connect(lambda: self.send_command("left_backward"))
        self.btn_backward.clicked.connect(lambda: self.send_command("backward"))
        self.btn_right_backward.clicked.connect(lambda: self.send_command("right_backward"))

        # 抓取按鈕單次觸發
        self.btn_grab.clicked.connect(lambda: self.send_command("grab"))

    def send_command(self, cmd):
        # 方向命令使用 handle_move_command，其他命令則使用 handle_command
        if cmd in ["forward", "backward", "left", "right",
                   "left_forward", "right_forward", "left_backward", "right_backward"]:
            result = self.control_module.handle_move_command(cmd)

            # 取得當前手臂位置
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tcp_pose, joint_positions = get_current_tcp_joint_positions()
            print(f"Current Time: {current_time}\ntcp_pose={tcp_pose}\noint_positions={joint_positions}\n")
        else:
            result = self.control_module.handle_command(cmd)
        self.status_label.setText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

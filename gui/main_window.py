import tkinter as tk
from control.state_machine import ControlModule
from control.get_position import get_current_tcp_joint_positions
from datetime import datetime

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("夾娃娃機控制介面")
        self.control_module = ControlModule()

        # 初始化介面
        self.init_ui()

        # 定時更新機台狀態 (每 2 秒一次)
        self.update_robot_status()

    def init_ui(self):
        # 設定按鈕樣式
        btn_params = {"width": 10, "height": 2, "font": ("Arial", 12)}

        # 3x3 方向按鈕佈局
        self.btn_left_forward = tk.Button(self.root, text="左前", command=lambda: self.send_command("left_forward"), **btn_params)
        self.btn_forward = tk.Button(self.root, text="前", command=lambda: self.send_command("forward"), **btn_params)
        self.btn_right_forward = tk.Button(self.root, text="右前", command=lambda: self.send_command("right_forward"), **btn_params)
        
        self.btn_left = tk.Button(self.root, text="左", command=lambda: self.send_command("left"), **btn_params)
        self.btn_right = tk.Button(self.root, text="右", command=lambda: self.send_command("right"), **btn_params)
        
        self.btn_left_backward = tk.Button(self.root, text="左後", command=lambda: self.send_command("left_backward"), **btn_params)
        self.btn_backward = tk.Button(self.root, text="後", command=lambda: self.send_command("backward"), **btn_params)
        self.btn_right_backward = tk.Button(self.root, text="右後", command=lambda: self.send_command("right_backward"), **btn_params)
        
        self.btn_grab = tk.Button(self.root, text="抓取", command=lambda: self.send_command("grab"), bg="orange", **btn_params)

        # 放置按鈕
        self.btn_left_forward.grid(row=0, column=0, padx=5, pady=5)
        self.btn_forward.grid(row=0, column=1, padx=5, pady=5)
        self.btn_right_forward.grid(row=0, column=2, padx=5, pady=5)
        
        self.btn_left.grid(row=1, column=0, padx=5, pady=5)
        self.btn_right.grid(row=1, column=2, padx=5, pady=5)
        
        self.btn_left_backward.grid(row=2, column=0, padx=5, pady=5)
        self.btn_backward.grid(row=2, column=1, padx=5, pady=5)
        self.btn_right_backward.grid(row=2, column=2, padx=5, pady=5)
        
        self.btn_grab.grid(row=3, column=1, padx=5, pady=10)

        # 狀態訊息
        self.status_label = tk.Label(self.root, text="系統初始化中...", fg="blue", font=("Arial", 10))
        self.status_label.grid(row=4, column=0, columnspan=3, pady=5)

        # 運行模式
        self.mode_label = tk.Label(self.root, text="運行模式：讀取中...", font=("Arial", 10, "bold"))
        self.mode_label.grid(row=5, column=0, columnspan=3, pady=5)

    def send_command(self, cmd):
        # 方向命令使用 handle_move_command，其他命令則使用 handle_command
        if cmd in ["forward", "backward", "left", "right",
                   "left_forward", "right_forward", "left_backward", "right_backward"]:
            result = self.control_module.handle_move_command(cmd)

            # 取得當前手臂位置
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tcp_pose, joint_positions = get_current_tcp_joint_positions()
            print(f"Current Time: {current_time}\ntcp_pose={tcp_pose}\njoint_positions={joint_positions}\n")
        else:
            result = self.control_module.handle_command(cmd)
        self.status_label.config(text=result)

    def update_robot_status(self):
        # 更新狀態標籤與模式標籤
        state = self.control_module.state
        self.mode_label.config(text=f"運行模式：{state}")
        # 每 2 秒更新一次
        self.root.after(2000, self.update_robot_status)

if __name__ == "__main__":
    root = tk.Tk()
    window = MainWindow(root)
    root.mainloop()

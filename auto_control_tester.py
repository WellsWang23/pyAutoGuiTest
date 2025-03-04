import tkinter as tk
from tkinter import ttk, messagebox
from auto_control import click_button, input_text
import pyautogui # type: ignore
import sys
import io
import random
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class AutoControlTester(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("自动控制测试程序")
        self.geometry("800x600")  # 增加窗口宽度
        
        # 创建主框架
        main_frame = ttk.Frame(self, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 左侧操作区域
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=10)
        
        # 右侧显示区域
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=10)
        
        # 测试目标区域
        self.target_frame = ttk.LabelFrame(left_frame, text="测试目标区域", padding="10")
        self.target_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # 添加测试按钮
        self.target_button = ttk.Button(self.target_frame, 
                                      text="测试用按钮",
                                      command=self.show_random_text)
        self.target_button.grid(row=0, column=0, pady=10, padx=5)
        
        # 添加测试输入框
        self.target_entry = ttk.Entry(self.target_frame)
        self.target_entry.grid(row=1, column=0, pady=10, padx=5)
        
        # 状态显示区域
        self.status_label = ttk.Label(left_frame, text="当前状态: 等待操作", font=('Arial', 10))
        self.status_label.grid(row=1, column=0, pady=10)
        
        # 坐标显示区域
        self.position_frame = ttk.LabelFrame(left_frame, text="记录的位置", padding="10")
        self.position_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.button_pos_label = ttk.Label(self.position_frame, text="按钮位置: 未记录")
        self.button_pos_label.grid(row=0, column=0, pady=5)
        
        self.entry_pos_label = ttk.Label(self.position_frame, text="输入框位置: 未记录")
        self.entry_pos_label.grid(row=1, column=0, pady=5)
        
        # 操作按钮区域
        self.control_frame = ttk.LabelFrame(left_frame, text="操作区域", padding="10")
        self.control_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # 记录按钮位置按钮
        self.record_button = ttk.Button(self.control_frame, 
                                      text="第一步: 记录按钮位置(3秒后记录)", 
                                      command=self.prepare_capture_button)
        self.record_button.grid(row=0, column=0, pady=10, padx=5, sticky=(tk.W, tk.E))
        
        # 记录输入框位置按钮
        self.record_entry = ttk.Button(self.control_frame, 
                                     text="第二步: 记录输入框位置(3秒后记录)", 
                                     command=self.prepare_capture_entry)
        self.record_entry.grid(row=1, column=0, pady=10, padx=5, sticky=(tk.W, tk.E))
        
        # 执行测试按钮
        self.run_test = ttk.Button(self.control_frame, 
                                 text="第三步: 执行自动化测试", 
                                 command=self.run_auto_test)
        self.run_test.grid(row=2, column=0, pady=10, padx=5, sticky=(tk.W, tk.E))
        
        # 右侧文本显示区域
        self.text_display = tk.Text(right_frame, width=30, height=20)
        self.text_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 存储坐标
        self.button_pos = None
        self.entry_pos = None
        
        # 随机文本列表
        self.random_texts = [
            "Hello, Auto Test!",
            "Testing is fun!",
            "Automation works!",
            "Python is great!",
            "Click success!",
            "Everything works fine!",
            "Test completed!",
            "Great job!",
        ]
    
    def show_random_text(self):
        """显示随机文本"""
        random_text = random.choice(self.random_texts)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, random_text)
    
    def prepare_capture_button(self):
        """准备捕获按钮位置"""
        self.status_label.config(text="请在3秒内将鼠标移动到目标按钮位置...")
        self.after(3000, self.capture_button_pos)
    
    def prepare_capture_entry(self):
        """准备捕获输入框位置"""
        self.status_label.config(text="请在3秒内将鼠标移动到目标输入框位置...")
        self.after(3000, self.capture_entry_pos)
    
    def capture_button_pos(self):
        """捕获按钮位置"""
        self.button_pos = pyautogui.position()
        self.button_pos_label.config(text=f"按钮位置: X={self.button_pos[0]}, Y={self.button_pos[1]}")
        self.status_label.config(text="按钮位置已记录")
    
    def capture_entry_pos(self):
        """捕获输入框位置"""
        self.entry_pos = pyautogui.position()
        self.entry_pos_label.config(text=f"输入框位置: X={self.entry_pos[0]}, Y={self.entry_pos[1]}")
        self.status_label.config(text="输入框位置已记录")
    
    def run_auto_test(self):
        """执行自动化测试"""
        if not self.button_pos or not self.entry_pos:
            messagebox.showwarning("警告", "请先记录按钮和输入框的位置！")
            return
        
        self.status_label.config(text="正在执行自动化测试...")
        
        # 测试点击
        click_button(self.button_pos[0], self.button_pos[1])
        
        # 等待一下让随机文本显示
        self.after(1000, lambda: self._continue_test())

    def _continue_test(self):
        """继续执行测试的剩余部分"""
        # 测试输入
        input_text(self.entry_pos[0], self.entry_pos[1], "i can input auto")
        self.status_label.config(text="自动化测试完成！")

if __name__ == "__main__":
    app = AutoControlTester()
    app.mainloop() 
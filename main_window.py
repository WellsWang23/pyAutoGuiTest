import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("自助增值税发票打印终端")
        
        # 设置全屏
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        # 配置深绿色主题
        self.style = ttk.Style()
        self.style.configure("Header.TFrame", background="#1B5E20")
        self.style.configure("Header.TLabel", 
                           background="#1B5E20", 
                           foreground="white",
                           font=("Arial", 24, "bold"))
        
        self.setup_ui()
        
    def setup_ui(self):
        # 顶部标题栏
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.pack(fill="x", pady=0)
        
        # Logo (假设logo.png在同一目录下)
        try:
            logo_img = Image.open("logo.png")
            logo_img = logo_img.resize((50, 50))
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(header_frame, image=logo_photo, background="#1B5E20")
            logo_label.image = logo_photo
            logo_label.pack(side="left", padx=20, pady=10)
        except:
            # 如果找不到logo文件，使用文字代替
            logo_label = ttk.Label(header_frame, 
                                 text="国网", 
                                 style="Header.TLabel")
            logo_label.pack(side="left", padx=20, pady=10)
        
        # 标题
        title_label = ttk.Label(header_frame, 
                              text="自助增值税发票打印终端", 
                              style="Header.TLabel")
        title_label.pack(side="left", padx=20, pady=10)
        
        # 时间标签
        self.time_label = ttk.Label(header_frame, 
                                  text="", 
                                  style="Header.TLabel")
        self.time_label.pack(side="right", padx=20, pady=10)
        self.update_time()
        
        # 主要内容区域
        content_frame = ttk.Frame(self.root)
        content_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        # 创建两个按钮
        button_frame = ttk.Frame(content_frame)
        button_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # 发票打印按钮
        self.create_icon_button(button_frame, 
                              "print_icon.png",  # 假设有这个图标文件
                              "发票打印",
                              0,
                              self.on_print_click)
        
        # 信息维护按钮
        self.create_icon_button(button_frame,
                              "settings_icon.png",  # 假设有这个图标文件
                              "开票信息维护",
                              1,
                              self.on_settings_click)
        
    def create_icon_button(self, parent, icon_path, text, column, command):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=column, padx=50)
        
        # 尝试加载图标
        try:
            icon = Image.open(icon_path)
            icon = icon.resize((100, 100))
            icon_photo = ImageTk.PhotoImage(icon)
            icon_label = ttk.Label(frame, image=icon_photo)
            icon_label.image = icon_photo
        except:
            # 如果找不到图标文件，创建一个占位框
            icon_label = ttk.Label(frame, 
                                 text="图标",
                                 width=15,
                                 height=5,
                                 relief="solid")
        icon_label.pack(pady=10)
        
        # 按钮文字
        text_label = ttk.Label(frame, 
                             text=text,
                             font=("Arial", 12))
        text_label.pack()
        
        # 使整个框架可点击
        frame.bind("<Button-1>", lambda e: command())
        icon_label.bind("<Button-1>", lambda e: command())
        text_label.bind("<Button-1>", lambda e: command())
        
    def update_time(self):
        """更新时间显示"""
        from datetime import datetime
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.root.after(1000, self.update_time)
        
    def on_print_click(self):
        """处理打印按钮点击"""
        print("打印按钮被点击")
        # 在这里添加打印功能的实现
        
    def on_settings_click(self):
        """处理设置按钮点击"""
        print("设置按钮被点击")
        # 在这里添加设置功能的实现
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run() 
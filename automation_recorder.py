import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import keyboard
import time
import pyautogui # type: ignore
from auto_control import click_button, input_text, double_click_button, hide_cursor, show_cursor, perform_action_with_wait

class AutomationRecorder:
    def __init__(self):
        # 添加 X11 错误处理
        try:
            from Xlib import XLib
        except ImportError:
            pass
        
        self.root = tk.Tk()
        self.root.title("自动化操作录制器")
        self.root.geometry("400x500")
        
        self.actions = []  # 存储录制的操作
        self.is_recording = False
        self.is_playing = False  # 添加回放状态标志
        
        # 添加一个StringVar来存储列表内容
        self.list_var = tk.StringVar(value=[])
        
        self.setup_ui()
        
    def setup_ui(self):
        # 创建录制控制区域
        record_frame = ttk.LabelFrame(self.root, text="录制控制", padding="10")
        record_frame.pack(fill="x", padx=10, pady=5)
        
        self.record_btn = ttk.Button(record_frame, text="开始录制", command=self.toggle_recording)
        self.record_btn.pack(side="left", padx=5)
        
        ttk.Label(record_frame, text="按F8记录位置").pack(side="left", padx=5)
        
        # 创建操作列表显示区域
        list_frame = ttk.LabelFrame(self.root, text="已录制的操作", padding="10")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        # 创建列表框并配置
        self.action_list = tk.Listbox(
            list_frame,
            listvariable=self.list_var,  # 使用StringVar
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            height=10,
            font=("Arial", 10),
            activestyle='dotbox',
            bg='white',
            fg='black'
        )
        self.action_list.pack(fill="both", expand=True, padx=(0, 5))
        
        # 配置滚动条
        scrollbar.config(command=self.action_list.yview)
        
        # 绑定右键菜单
        self.action_list.bind("<Button-3>", self.show_context_menu)
        
        # 创建右键菜单
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="删除", command=self.delete_action)
        
        # 创建回放控制区域
        playback_frame = ttk.LabelFrame(self.root, text="回放控制", padding="10")
        playback_frame.pack(fill="x", padx=10, pady=5)
        
        # 第一行：配置文件操作
        config_frame = ttk.Frame(playback_frame)
        config_frame.pack(fill="x", pady=5)
        
        self.save_btn = ttk.Button(config_frame, text="保存配置", command=self.save_config)
        self.save_btn.pack(side="left", padx=5)
        
        self.load_btn = ttk.Button(config_frame, text="选择配置", command=self.choose_config)
        self.load_btn.pack(side="left", padx=5)
        
        # 第二行：回放控制
        control_frame = ttk.Frame(playback_frame)
        control_frame.pack(fill="x", pady=5)
        
        self.playback_btn = ttk.Button(control_frame, text="开始回放", command=self.toggle_playback)
        self.playback_btn.pack(side="left", padx=5)
        
        # 添加配置文件路径显示
        self.config_path_label = ttk.Label(playback_frame, text="当前配置文件: 未选择", wraplength=350)
        self.config_path_label.pack(fill="x", pady=5)
        
        # 添加当前配置文件路径存储
        self.current_config_path = None

    def toggle_recording(self):
        try:
            self.is_recording = not self.is_recording
            if self.is_recording:
                self.record_btn.configure(text="停止录制")
                keyboard.on_press_key("F8", self.record_position)
                # 禁用其他按钮
                self.disable_buttons()
            else:
                self.record_btn.configure(text="开始录制")
                keyboard.unhook_all()
                # 启用其他按钮
                self.enable_buttons()
        except PermissionError:
            messagebox.showerror("错误", "需要 root 权限才能录制键盘事件。请使用 sudo 运行程序。")
            self.is_recording = False
            self.record_btn.configure(text="开始录制")
            
    def record_position(self, _):
        if not self.is_recording:
            return
            
        # 获取当前鼠标位置
        x, y = pyautogui.position()
        
        # 创建操作类型选择窗口
        dialog = tk.Toplevel(self.root)
        dialog.title("选择操作类型")
        dialog.geometry("300x250")
        
        action_type = tk.StringVar(value="click")
        text_value = tk.StringVar()
        wait_for_change = tk.BooleanVar(value=False)
        
        ttk.Radiobutton(dialog, text="单击操作", variable=action_type, value="click").pack()
        ttk.Radiobutton(dialog, text="双击操作", variable=action_type, value="double_click").pack()
        ttk.Radiobutton(dialog, text="输入文本", variable=action_type, value="input").pack()
        ttk.Checkbutton(dialog, text="等待页面变化", variable=wait_for_change).pack(pady=5)
        
        input_frame = ttk.Frame(dialog)
        input_frame.pack(pady=5)
        ttk.Label(input_frame, text="输入文本:").pack(side="left")
        text_entry = ttk.Entry(input_frame, textvariable=text_value)
        text_entry.pack(side="left", padx=5)
        
        def save_action():
            action = {
                "type": action_type.get(),
                "x": x,
                "y": y,
                "text": text_value.get() if action_type.get() == "input" else "",
                "wait_for_change": wait_for_change.get()
            }
            self.actions.append(action)
            
            # 更新列表显示
            current_items = list(self.action_list.get(0, tk.END))
            action_type_str = {
                "click": "单击",
                "double_click": "双击",
                "input": "输入"
            }.get(action["type"], "未知操作")
            
            action_str = f"{len(self.actions)}. {action_type_str} at ({action['x']}, {action['y']})"
            if action["type"] == "input":
                action_str += f" 文本: {action['text']}"
            if action.get("wait_for_change", False):
                action_str += " [等待页面变化]"
            
            current_items.append(action_str)
            self.list_var.set(current_items)  # 使用StringVar更新
            
            dialog.destroy()
            
            # 确保选中并显示最新项
            self.root.after(100, lambda: (
                self.action_list.selection_clear(0, tk.END),
                self.action_list.selection_set(tk.END),
                self.action_list.see(tk.END),
                self.root.update()
            ))
        
        dialog.protocol("WM_DELETE_WINDOW", lambda: dialog.destroy())
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Button(dialog, text="确定", command=save_action).pack(pady=5)
        dialog.focus_set()
        
    def update_action_list(self):
        """更新操作列表显示"""
        self.action_list.delete(0, tk.END)
        for i, action in enumerate(self.actions):
            action_type_str = {
                "click": "单击",
                "double_click": "双击",
                "input": "输入"
            }.get(action["type"], "未知操作")
            
            action_str = f"{i+1}. {action_type_str} at ({action['x']}, {action['y']})"
            if action["type"] == "input":
                action_str += f" 文本: {action['text']}"
            if action.get("wait_for_change", False):
                action_str += " [等待页面变化]"
            
            self.action_list.insert(tk.END, action_str)
        self.root.update()
        
    def choose_config(self):
        """选择配置文件"""
        file_path = filedialog.askopenfilename(
            title="选择配置文件",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.current_config_path = file_path
            self.config_path_label.config(text=f"当前配置文件: {file_path}")
            self.load_config(file_path)
    
    def save_config(self):
        """保存配置文件"""
        file_path = filedialog.asksaveasfilename(
            title="保存配置文件",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.actions, f, ensure_ascii=False, indent=2)
            self.current_config_path = file_path
            self.config_path_label.config(text=f"当前配置文件: {file_path}")
            messagebox.showinfo("成功", "配置已保存")
            
    def load_config(self, file_path=None):
        """加载配置文件"""
        try:
            path = file_path or self.current_config_path
            if not path:
                messagebox.showwarning("警告", "请先选择配置文件")
                return
                
            with open(path, "r", encoding="utf-8") as f:
                self.actions = json.load(f)
                self.update_action_list()
                messagebox.showinfo("成功", "配置已加载")
        except FileNotFoundError:
            messagebox.showerror("错误", "配置文件不存在")
        except json.JSONDecodeError:
            messagebox.showerror("错误", "配置文件格式错误")
            
    def toggle_playback(self):
        """切换回放状态"""
        if not self.actions:
            messagebox.showwarning("警告", "没有可回放的操作")
            return
            
        if not self.is_playing:
            self.is_playing = True
            self.playback_btn.configure(text="停止回放")
            self.start_playback()
        else:
            self.is_playing = False
            self.playback_btn.configure(text="开始回放")
            
    def start_playback(self):
        """执行回放"""
        if not self.is_playing:
            return
            
        try:
            hide_cursor()
            
            for i, action in enumerate(self.actions):
                if not self.is_playing:
                    break
                    
                try:
                    wait_for_change = action.get("wait_for_change", False)
                    
                    if action["type"] == "click":
                        perform_action_with_wait(click_button, 
                                              action["x"], 
                                              action["y"], 
                                              wait_for_change=wait_for_change)
                    elif action["type"] == "double_click":
                        perform_action_with_wait(double_click_button, 
                                              action["x"], 
                                              action["y"], 
                                              wait_for_change=wait_for_change)
                    elif action["type"] == "input":
                        perform_action_with_wait(input_text, 
                                              action["x"], 
                                              action["y"], 
                                              action["text"], 
                                              wait_for_change=wait_for_change)
                    
                    self.action_list.selection_clear(0, tk.END)
                    self.action_list.selection_set(i)
                    self.action_list.see(i)
                    self.root.update()
                    
                    if self.is_playing:
                        time.sleep(1)
                except Exception as e:
                    messagebox.showerror("错误", f"执行操作失败: {str(e)}")
                    self.is_playing = False
                    self.playback_btn.configure(text="开始回放")
                    break
        finally:
            show_cursor()
            
        # 回放完成后重置状态
        if self.is_playing:
            self.is_playing = False
            self.playback_btn.configure(text="开始回放")
            messagebox.showinfo("完成", "回放已完成")

    def disable_buttons(self):
        """禁用除录制按钮外的所有按钮"""
        self.save_btn.configure(state="disabled")
        self.load_btn.configure(state="disabled")
        self.playback_btn.configure(state="disabled")
        self.action_list.configure(state="disabled")

    def enable_buttons(self):
        """启用所有按钮"""
        self.save_btn.configure(state="normal")
        self.load_btn.configure(state="normal")
        self.playback_btn.configure(state="normal")
        self.action_list.configure(state="normal")

    def show_context_menu(self, event):
        """显示右键菜单"""
        if not self.is_recording:  # 只在非录制状态下显示右键菜单
            try:
                # 获取点击位置对应的项目索引
                index = self.action_list.nearest(event.y)
                # 选中该项目
                self.action_list.selection_clear(0, tk.END)
                self.action_list.selection_set(index)
                # 显示菜单
                self.context_menu.post(event.x_root, event.y_root)
            except:
                pass

    def delete_action(self):
        """删除选中的操作"""
        try:
            # 获取选中项的索引
            selected = self.action_list.curselection()
            if selected:
                index = selected[0]
                # 从列表和操作记录中删除
                self.action_list.delete(index)
                self.actions.pop(index)
                # 更新显示
                self.update_action_list()
        except:
            pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    recorder = AutomationRecorder()
    recorder.run() 
import pyautogui # type: ignore
import time
from ctypes import *

# 设置pyautogui的失败安全模式为False（可选）
pyautogui.FAILSAFE = False

def hide_cursor():
    """隐藏鼠标光标"""
    try:
        # Linux系统
        import subprocess
        subprocess.run(['xdotool', 'mousemove_relative', '--sync', '--', '0', '0'])
        subprocess.run(['unclutter', '-idle', '0.01'])
    except:
        try:
            # Windows系统
            class CURSORINFO(Structure):
                _fields_ = [("cbSize", c_uint),
                          ("flags", c_uint),
                          ("hCursor", c_void_p),
                          ("ptScreenPos", c_void_p)]
            
            windll.user32.ShowCursor(False)
        except:
            pass

def show_cursor():
    """显示鼠标光标"""
    try:
        # Linux系统
        import subprocess
        subprocess.run(['killall', 'unclutter'])
    except:
        try:
            # Windows系统
            windll.user32.ShowCursor(True)
        except:
            pass

def move_mouse_invisible(x, y):
    """无痕迹移动鼠标到指定位置"""
    hide_cursor()
    pyautogui.moveTo(x, y, duration=0)  # duration=0 表示立即移动，不显示过程

def click_button(x: int, y: int) -> bool:
    """
    点击屏幕指定位置的按钮
    
    Args:
        x: 按钮的x坐标
        y: 按钮的y坐标
        
    Returns:
        bool: 点击操作是否成功
    """
    move_mouse_invisible(x, y)
    pyautogui.click()
    show_cursor()
    return True

def input_text(x: int, y: int, text: str) -> bool:
    """
    在指定位置的输入框中输入文本
    
    Args:
        x: 输入框的x坐标
        y: 输入框的y坐标
        text: 要输入的文本内容
        
    Returns:
        bool: 输入操作是否成功
    """
    move_mouse_invisible(x, y)
    pyautogui.click()
    time.sleep(0.1)  # 短暂延迟确保点击生效
    pyautogui.typewrite(text)
    show_cursor()
    return True

def double_click_button(x: int, y: int) -> bool:
    """
    在指定位置双击鼠标
    
    Args:
        x: 双击位置的x坐标
        y: 双击位置的y坐标
        
    Returns:
        bool: 双击操作是否成功
    """
    move_mouse_invisible(x, y)
    pyautogui.doubleClick()
    show_cursor()
    return True 
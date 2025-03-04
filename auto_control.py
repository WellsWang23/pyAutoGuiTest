import pyautogui # type: ignore
import time
from ctypes import *
import cv2
import numpy as np
from typing import Optional

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

def capture_screen() -> np.ndarray:
    """捕获当前屏幕"""
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def wait_for_page_change(original_image: np.ndarray, timeout: int = 10, threshold: float = 0.95) -> bool:
    """
    等待页面变化
    
    Args:
        original_image: 原始页面截图
        timeout: 超时时间（秒）
        threshold: 相似度阈值，低于此值认为页面已改变
        
    Returns:
        bool: 页面是否发生变化
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_image = capture_screen()
        
        # 确保图像大小相同
        if original_image.shape != current_image.shape:
            current_image = cv2.resize(current_image, (original_image.shape[1], original_image.shape[0]))
            
        # 计算图像相似度
        result = cv2.matchTemplate(current_image, original_image, cv2.TM_CCOEFF_NORMED)
        similarity = np.max(result)
        
        if similarity < threshold:
            return True
        time.sleep(0.5)
        
    return False

def perform_action_with_wait(action_func, *args, wait_for_change: bool = False, **kwargs) -> bool:
    """
    执行操作并可选等待页面变化
    
    Args:
        action_func: 要执行的操作函数
        wait_for_change: 是否等待页面变化
        *args, **kwargs: 传递给操作函数的参数
    """
    if wait_for_change:
        original_image = capture_screen()
        
    result = action_func(*args, **kwargs)
    
    if wait_for_change and result:
        return wait_for_page_change(original_image)
    return result 
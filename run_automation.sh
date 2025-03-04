#!/bin/bash

# 检查是否已经创建虚拟环境
if [ ! -d "$HOME/pyautogui_env" ]; then
    echo "正在创建虚拟环境..."
    python3 -m venv ~/pyautogui_env
fi

# 激活虚拟环境
source ~/pyautogui_env/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

# 设置 X11 权限
echo "设置 X11 权限..."
xhost +local:

# 设置 dconf 权限
echo "设置 dconf 权限..."
mkdir -p /tmp/runtime-root
export XDG_RUNTIME_DIR=/tmp/runtime-root
chmod 700 /tmp/runtime-root

# 运行程序
echo "启动自动化录制器..."
sudo -E DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY XDG_RUNTIME_DIR=/tmp/runtime-root ~/pyautogui_env/bin/python3 automation_recorder.py

# 恢复 X11 安全设置
xhost -local:

# 清理临时目录
rm -rf /tmp/runtime-root

# 提示完成
echo "程序已退出"

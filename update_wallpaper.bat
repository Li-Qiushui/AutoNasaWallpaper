@echo off
chcp 65001 >nul
echo ========================================
echo NASA自动壁纸更换程序
echo 开始时间: %date% %time%
echo ========================================

:: 切换到程序所在目录
cd /d "%~dp0"

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请确保Python已安装并添加到PATH环境变量
    pause
    exit /b 1
)

:: 检查依赖是否安装
echo 检查依赖包...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install requests
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
)

:: 运行壁纸更换程序
echo 正在获取NASA图片并更换壁纸...
python run.py

:: 检查程序运行结果
if errorlevel 1 (
    echo 壁纸更换失败，请查看日志文件
    echo 日志文件位置: %~dp0wallpaper.log
) else (
    echo 壁纸更换成功！
)

echo ========================================
echo 完成时间: %date% %time%
echo ========================================

:: 等待3秒后关闭窗口（如果是从任务计划程序启动）
timeout /t 3 >nul 
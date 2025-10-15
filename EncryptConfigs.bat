@echo off
setlocal enabledelayedexpansion

:: ==============================
:: 使用 UTF-8 编码，防止日志中文乱码
:: ==============================
chcp 65001 >nul

:: ==============================
:: Unity 路径（修改成你本地版本）
:: ==============================
set UNITY_EXE="F:\Unity\Unity2020.3.33f1\Unity2020.3.33f1\Editor\Unity.exe"

:: ==============================
:: Unity 工程路径
:: ==============================
set PROJECT_PATH=D:\Github\TaleOfXiaMod

:: ==============================
:: 配置输入目录（原始文本）
:: ==============================
set INPUT_DIR=E:\mod\XiakePreMod\Game\Mods\1.0.2.8

:: ==============================
:: 时间戳生成（保留原有本地方式）
:: ==============================
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do (
    set DATE=%%a-%%b-%%c
)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (
    set TIME=%%a-%%b
)
set TIME=!TIME::=-!

:: ==============================
:: 输出目录 & 日志文件
:: ==============================
set OUTPUT_DIR=E:\mod\XiakePreMod\Game\Mods\1.0.2.8\Config\Output_!DATE!_!TIME!
set LOG_FILE=%PROJECT_PATH%\encrypt_log_!DATE!_!TIME!.txt

:: ==============================
:: 确保输出目录存在
:: ==============================
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

:: ==============================
:: 显示信息
:: ==============================
echo ===========================================
echo 🔐 开始加密游戏配置文件
echo -------------------------------------------
echo 🏗️ 工程路径: %PROJECT_PATH%
echo 📂 输入目录: %INPUT_DIR%
echo 💾 输出目录: %OUTPUT_DIR%
echo 📜 日志文件: %LOG_FILE%
echo ===========================================
echo.

:: ==============================
:: 执行 Unity 命令行
:: ==============================
%UNITY_EXE% ^
 -batchmode ^
 -quit ^
 -projectPath "%PROJECT_PATH%" ^
 -executeMethod GameConfigEncryptor.EncryptFromCommandLine ^
 input="%INPUT_DIR%" ^
 output="%OUTPUT_DIR%" ^
 -logFile "%LOG_FILE%"

:: ==============================
:: 错误检查
:: ==============================
if %errorlevel% neq 0 (
    echo ❌ 加密过程中发生错误，请检查日志: %LOG_FILE%
    pause
    exit /b %errorlevel%
)

echo.
echo ===========================================
echo ✅ 加密完成！
echo 📦 输出文件夹: %OUTPUT_DIR%
echo 📜 日志文件: %LOG_FILE%
echo ===========================================

:: ==============================
:: 自动打开输出目录
:: ==============================
start "" "%OUTPUT_DIR%"

pause
endlocal

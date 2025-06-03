@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo =============================================
echo   ⚙️  开始批量双向同步（不删除任何文件）
echo =============================================

:: 每组目录一行，用 | 分隔，本地在前，GitHub 路径在后
:: 不要带引号，即使有空格也不要加
:: 可在此添加多组路径
set "SYNC_PAIRS_FILE=%~dp0sync_pairs.txt"

:: 检查配置文件
if not exist "%SYNC_PAIRS_FILE%" (
    echo ❌ 找不到配置文件：%SYNC_PAIRS_FILE%
    echo 请创建一个名为 sync_pairs.txt 的文件，每行写入：
    echo   本地路径|GitHub路径
    echo 例如：
    echo   F:\A Path\Local|E:\Repo\Target
    pause
    exit /b
)

:: 逐行读取并处理
for /f "usebackq tokens=1,2 delims=|" %%A in ("%SYNC_PAIRS_FILE%") do (
    set "localPath=%%A"
    set "githubPath=%%B"

    echo.
    echo 🔄 正在同步：
    echo    本地：!localPath!
    echo    GitHub：!githubPath!

    if exist "!localPath!" if exist "!githubPath!" (
        echo ➤ 本地 → GitHub
        robocopy "!localPath!" "!githubPath!" /E /XO /NFL /NDL /NJH /NJS /NS /NC

        echo ➤ GitHub → 本地
        robocopy "!githubPath!" "!localPath!" /E /XO /NFL /NDL /NJH /NJS /NS /NC
    ) else (
        echo ❌ 路径不存在，请检查：
        if not exist "!localPath!" echo   - 本地路径不存在：!localPath!
        if not exist "!githubPath!" echo   - GitHub路径不存在：!githubPath!
    )
)

echo.
echo ✅ 所有同步任务已完成。
pause
exit /b

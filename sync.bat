@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo =============================================
echo   ⚙️  开始批量双向同步（不删除任何文件）
echo =============================================

:: 保存路径组，每行一组，用 | 分隔。不要加引号！
:: 将下面每组路径改成你自己的即可。
set "syncListFile=%temp%\_sync_pairs.txt"
(
    echo F:\Program Files (x86)\FB_apps\2083\app_data\BepInEx\plugins|E:\mod\XiakePreMod\Game\BepInEx\plugins
    echo F:\Program Files (x86)\FB_apps\2083\app_data\Mods|E:\mod\XiakePreMod\Game\Mods
) > "%syncListFile%"

:: 遍历每组路径并同步
for /f "usebackq tokens=1,2 delims=|" %%A in ("%syncListFile%") do (
    set "localPath=%%A"
    set "githubPath=%%B"

    echo.
    echo 🔄 正在同步：
    echo    本地：!localPath!
    echo    GitHub：!githubPath!

    if exist "!localPath!" if exist "!githubPath!" (
        echo ➤ 本地 → GitHub
        robocopy "!localPath!" "!githubPath!" /E /XO /NFL /NDL /NJH /NJS /NS /NC >nul

        echo ➤ GitHub → 本地
        robocopy "!githubPath!" "!localPath!" /E /XO /NFL /NDL /NJH /NJS /NS /NC >nul
    ) else (
        echo ❌ 路径不存在，请检查：
        if not exist "!localPath!" echo   - 本地路径不存在：!localPath!
        if not exist "!githubPath!" echo   - GitHub路径不存在：!githubPath!
    )
)

del "%syncListFile%" >nul 2>&1

echo.
echo ✅ 所有同步任务已完成。
pause

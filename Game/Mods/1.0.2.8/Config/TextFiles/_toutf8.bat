@echo off
chcp 65001
setlocal enabledelayedexpansion

echo Start processing files...

for %%f in (*.txt) do (
    set "filename=%%~nxf"
    set "basename=%%~nf"
    set "skip="

    rem 跳过已是 utf8 文件
    echo !filename! | findstr /i "_utf8" >nul
    if !errorlevel! equ 0 (
        set "skip=已是 UTF-8 文件"
    )

    rem 用 PowerShell 判断是否包含中文（范围为：\u4E00-\u9FFF）
    for /f %%C in ('powershell -Command "[regex]::IsMatch('%%~nf','[\u4e00-\u9fff]')"') do (
        if %%C==True (
            set "skip=文件名包含中文字符"
        )
    )

    if not defined skip (
        echo 正在更新或生成 "!basename!_utf8.txt" ...
        type "%%f" > "!basename!_utf8.txt"
    ) else (
        echo 跳过 "%%f"（!skip!）
    )
)

echo Done.
pause

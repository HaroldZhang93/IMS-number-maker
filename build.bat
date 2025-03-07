@echo off
echo 正在清理旧的构建文件...
rmdir /s /q build dist
echo.

echo 选择打包方式:
echo 1. 文件夹模式 (启动更快，但有多个文件)
echo 2. 单文件模式 (启动较慢，但只有一个文件)
echo.

set /p choice=请选择打包方式 (1 或 2): 

if "%choice%"=="1" (
    echo 正在使用文件夹模式打包...
    pyinstaller IMS-number-maker.spec
    echo 打包完成! 可执行文件位于 dist\IMS号码生成器 目录中
) else if "%choice%"=="2" (
    echo 正在使用单文件模式打包...
    pyinstaller IMS-number-maker-onefile.spec
    echo 打包完成! 可执行文件位于 dist 目录中
) else (
    echo 无效的选择!
)

echo.
pause 
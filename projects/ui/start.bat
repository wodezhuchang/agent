@echo off
chcp 65001 > nul
echo.
echo ========================================
echo   校园校小助 UI 管理界面
echo ========================================
echo.
echo 正在启动本地服务器...
echo.

:: 启动本地服务器
start "" cmd /k "cd /d %~dp0ui && python -m http.server 8080"

:: 等待服务器启动
timeout /t 2 /nobreak > nul

:: 打开浏览器
start http://localhost:8080

echo 服务器已启动：http://localhost:8080
echo.
echo 按任意键退出此窗口（服务器将继续运行）
pause > nul

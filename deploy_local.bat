@echo off
setlocal enabledelayedexpansion

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
echo 错误：未找到Python环境，请先安装Python
pause
exit /b 1
)

REM 检查Hugo是否安装
hugo version >nul 2>&1
if %errorlevel% neq 0 (
echo 错误：未找到Hugo，请先安装Hugo并添加到环境变量
pause
exit /b 1
)

REM 检查.env文件是否存在
if not exist .env (
echo 警告：未找到.env文件，将使用系统环境变量
)

REM 检查GitHub Actions所需密钥是否配置
if "%ACTIONS_DEPLOY_KEY%" == "" (
echo 警告：未配置 ACTIONS_DEPLOY_KEY，GitHub Pages 部署可能失败，请在仓库设置中配置此密钥
)
if "%OPENAI_API_KEY%" == "" (
echo 警告：未配置 OPENAI_API_KEY，AI 文章生成可能失败，请在.env文件或系统环境变量中配置此密钥
)

REM 安装Python依赖
echo 正在安装Python依赖...
pip install openai python-dotenv scikit-learn pandas >nul 2>&1
if %errorlevel% neq 0 (
echo 错误：Python依赖安装失败
pause
exit /b 1
)

REM 生成AI文章
echo 正在生成AI文章...
python generate_post.py
if %errorlevel% neq 0 (
echo 错误：文章生成失败
pause
exit /b 1
)

REM 提交变更到仓库
git add .
git commit -m "Auto: 本地部署更新" || echo "No changes to commit"

REM 构建Hugo网站
echo 正在构建网站...
hugo --minify
if %errorlevel% neq 0 (
echo 错误：网站构建失败
pause
exit /b 1
)

REM 启动本地服务器预览
echo 部署完成，正在启动本地预览...
hugo server -D

endlocal
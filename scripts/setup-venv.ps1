# 创建虚拟环境并安装依赖

Write-Host "Creating Python virtual environment..." -ForegroundColor Green

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\.venv\Scripts\Activate.ps1

# 安装依赖
Write-Host "Installing dependencies..." -ForegroundColor Green
pip install -r requirements.txt

# 安装打包工具
Write-Host "Installing PyInstaller..." -ForegroundColor Green
pip install pyinstaller

Write-Host "Environment setup complete!" -ForegroundColor Green
Write-Host "To activate: .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
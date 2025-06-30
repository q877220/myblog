# 自动推送脚本
Write-Host "开始自动推送流程..."

# 检查Git状态
$status = git status --porcelain
if (-not $status) {
    Write-Host "没有需要提交的更改"
    exit 0
}

# 添加所有更改
git add .

# 提交更改
git commit -m "自动提交: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# 先拉取远程更改
git pull --rebase

# 推送到远程
git push

if ($LASTEXITCODE -ne 0) {
    Write-Host "推送失败，尝试强制推送..."
    git push --force
}

Write-Host "自动推送完成"
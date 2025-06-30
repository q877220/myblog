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

# 推送到远程
git push

Write-Host "自动推送完成"
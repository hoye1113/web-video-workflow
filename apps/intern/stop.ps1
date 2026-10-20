# 停止实习工作台（只停 8900 这个端口的进程）
$port = 8900
$c = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if ($c) {
    Stop-Process -Id $c[0].OwningProcess -Force
    Write-Host "已停止（pid $($c[0].OwningProcess)）"
} else {
    Write-Host "没在跑"
}

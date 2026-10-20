# 启动实习工作台：已经在跑就不重复起；起好后用默认浏览器打开
$ErrorActionPreference = "SilentlyContinue"
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $root
$port = 8900

$listening = Get-NetTCPConnection -LocalPort $port -State Listen
if (-not $listening) {
    New-Item -ItemType Directory -Force -Path (Join-Path $root "logs") | Out-Null
    $log = Join-Path $root "logs\intern.log"
    $err = Join-Path $root "logs\intern.err.log"
    Start-Process -FilePath "python" `
        -ArgumentList "apps\intern\server.py", "--port", $port, "--host", "0.0.0.0" `
        -WorkingDirectory $root -WindowStyle Hidden `
        -RedirectStandardOutput $log -RedirectStandardError $err
    Start-Sleep -Seconds 3
    Write-Host "已启动（日志：logs\intern.log / intern.err.log）"
} else {
    Write-Host "已经在跑（pid $($listening[0].OwningProcess)）"
}

Start-Process "http://127.0.0.1:$port/"
Write-Host "打开：http://127.0.0.1:$port/"
Write-Host "局域网里的实习生用：http://$((Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notmatch '^(127\.|169\.254\.)' } | Select-Object -First 1).IPAddress):$port/"

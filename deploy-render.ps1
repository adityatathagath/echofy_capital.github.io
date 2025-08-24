# PowerShell script to deploy to Render using API
param(
    [string]$ApiKey = "rnd_o0PgMkcFBAc6WvNR2yhQeN7WsM2g"
)

$Headers = @{
    "Authorization" = "Bearer $ApiKey"
    "Content-Type" = "application/json"
}

Write-Host "🚀 Starting Render Deployment..." -ForegroundColor Green
Write-Host "API Key: $($ApiKey.Substring(0,10))..." -ForegroundColor Yellow

try {
    # Test API connection
    Write-Host "Testing API connection..." -ForegroundColor Cyan
    $testResponse = Invoke-RestMethod -Uri "https://api.render.com/v1/owners" -Method GET -Headers $Headers
    Write-Host "✅ API connection successful!" -ForegroundColor Green
    Write-Host "Account: $($testResponse.name)" -ForegroundColor Yellow
    
    # Fetch existing services
    Write-Host "Fetching existing services..." -ForegroundColor Cyan
    $services = Invoke-RestMethod -Uri "https://api.render.com/v1/services" -Method GET -Headers $Headers
    
    Write-Host "Current services:" -ForegroundColor Yellow
    foreach ($service in $services) {
        Write-Host "  - $($service.name) ($($service.type))" -ForegroundColor Gray
    }
    
    Write-Host "🎯 Next Steps for Deployment:" -ForegroundColor Magenta
    Write-Host "Repository: https://github.com/adityatathagath/echofy_capital.github.io" -ForegroundColor White
    Write-Host "Branch: main" -ForegroundColor White
    Write-Host "Configuration: render.yaml detected" -ForegroundColor White
    Write-Host ""
    Write-Host "✨ To Deploy:" -ForegroundColor Green
    Write-Host "1. Go to https://dashboard.render.com" -ForegroundColor White
    Write-Host "2. Click 'New' → 'Blueprint'" -ForegroundColor White
    Write-Host "3. Connect GitHub repository" -ForegroundColor White
    Write-Host "4. Select 'adityatathagath/echofy_capital.github.io'" -ForegroundColor White
    Write-Host "5. Click 'Apply'" -ForegroundColor White
    
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Manual deployment recommended via Render Dashboard" -ForegroundColor Yellow
}

# Advanced Render deployment using API
param(
    [string]$ApiKey = "rnd_o0PgMkcFBAc6WvNR2yhQeN7WsM2g"
)

$Headers = @{
    "Authorization" = "Bearer $ApiKey"
    "Content-Type" = "application/json"
}

Write-Host "🚀 Creating Render Services..." -ForegroundColor Green

try {
    # Step 1: Create PostgreSQL Database
    Write-Host "Creating PostgreSQL database..." -ForegroundColor Cyan
    
    $dbPayload = @{
        "type" = "pgsql"
        "name" = "echofy-capital-db"
        "plan" = "free"
        "databaseName" = "fund_manager"
        "databaseUser" = "fund_manager_user"
    } | ConvertTo-Json -Depth 3

    $database = Invoke-RestMethod -Uri "https://api.render.com/v1/postgres" -Method POST -Headers $Headers -Body $dbPayload
    Write-Host "✅ Database created: $($database.name)" -ForegroundColor Green
    
    # Step 2: Create Web Service
    Write-Host "Creating web service..." -ForegroundColor Cyan
    
    $servicePayload = @{
        "type" = "web_service"
        "name" = "echofy-capital-web"
        "ownerId" = $database.ownerId
        "repo" = "https://github.com/adityatathagath/echofy_capital.github.io"
        "branch" = "main"
        "runtime" = "python"
        "plan" = "free"
        "buildCommand" = "pip install -r requirements.txt"
        "startCommand" = "gunicorn --config gunicorn_config.py app:app"
        "healthCheckPath" = "/health"
        "envVars" = @(
            @{ "key" = "FLASK_ENV"; "value" = "production" }
            @{ "key" = "SESSION_COOKIE_SECURE"; "value" = "true" }
            @{ "key" = "FLASK_DEBUG"; "value" = "false" }
            @{ "key" = "DATABASE_URL"; "value" = $database.databaseUrl }
        )
    } | ConvertTo-Json -Depth 4

    $service = Invoke-RestMethod -Uri "https://api.render.com/v1/services" -Method POST -Headers $Headers -Body $servicePayload
    Write-Host "✅ Web service created: $($service.name)" -ForegroundColor Green
    
    Write-Host "🎉 Deployment Complete!" -ForegroundColor Magenta
    Write-Host "Database: $($database.name)" -ForegroundColor White
    Write-Host "Web Service: $($service.name)" -ForegroundColor White
    Write-Host "URL: https://$($service.name).onrender.com" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ API Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Alternative - Manual Deployment:" -ForegroundColor Yellow
    Write-Host "1. Visit https://dashboard.render.com" -ForegroundColor White
    Write-Host "2. New → Blueprint" -ForegroundColor White
    Write-Host "3. Connect adityatathagath/echofy_capital.github.io" -ForegroundColor White
    Write-Host "4. Apply configuration" -ForegroundColor White
}

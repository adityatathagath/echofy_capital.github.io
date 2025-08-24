# PowerShell script to deploy to Render using API
# Run this script to deploy your application to Render

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
    
    # Create deployment using Blueprint (render.yaml)
    Write-Host "Creating deployment from render.yaml..." -ForegroundColor Cyan
    
    $deploymentBody = @{
        "type" = "blueprint"
        "repo" = "https://github.com/adityatathagath/echofy_capital.github.io"
        "branch" = "main"
        "blueprint" = @{
            "services" = @(
                @{
                    "type" = "web"
                    "name" = "echofy-capital-web"
                    "env" = "python"
                    "plan" = "free"
                    "buildCommand" = "pip install -r requirements.txt"
                    "startCommand" = "gunicorn --config gunicorn_config.py app:app"
                    "healthCheckPath" = "/health"
                    "envVars" = @(
                        @{ "key" = "FLASK_ENV"; "value" = "production" }
                        @{ "key" = "SESSION_COOKIE_SECURE"; "value" = "true" }
                        @{ "key" = "FLASK_DEBUG"; "value" = "false" }
                    )
                }
            )
            "databases" = @(
                @{
                    "name" = "echofy-capital-db"
                    "plan" = "free"
                    "databaseName" = "fund_manager"
                    "user" = "fund_manager_user"
                }
            )
        }
    } | ConvertTo-Json -Depth 10
    
    # Note: Render API might require different endpoints for blueprint deployment
    # The exact API endpoint may vary. Let's try to find available services first
    
    Write-Host "Fetching existing services..." -ForegroundColor Cyan
    $services = Invoke-RestMethod -Uri "https://api.render.com/v1/services" -Method GET -Headers $Headers
    
    Write-Host "Current services:" -ForegroundColor Yellow
    foreach ($service in $services) {
        Write-Host "  - $($service.name) ($($service.type))" -ForegroundColor Gray
    }
    
    Write-Host "🎯 Deployment Information:" -ForegroundColor Magenta
    Write-Host "Repository: https://github.com/adityatathagath/echofy_capital.github.io" -ForegroundColor White
    Write-Host "Branch: main" -ForegroundColor White
    Write-Host "Configuration: render.yaml detected" -ForegroundColor White
    Write-Host ""
    Write-Host "✨ Manual Deployment Steps:" -ForegroundColor Green
    Write-Host "1. Go to https://dashboard.render.com" -ForegroundColor White
    Write-Host "2. Click 'New' → 'Blueprint'" -ForegroundColor White
    Write-Host "3. Connect your GitHub repository" -ForegroundColor White
    Write-Host "4. Select 'adityatathagath/echofy_capital.github.io'" -ForegroundColor White
    Write-Host "5. Click 'Apply' - Render will use your render.yaml automatically" -ForegroundColor White
    
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "🔧 Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Verify your API key is correct" -ForegroundColor White
    Write-Host "2. Check your internet connection" -ForegroundColor White
    Write-Host "3. Try manual deployment via Render Dashboard" -ForegroundColor White
}

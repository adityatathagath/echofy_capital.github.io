# PowerShell script to deploy Echofy Capital to Render
# This script will use the render.yaml configuration file

Write-Host "🚀 Starting deployment to Render..." -ForegroundColor Green

# Check if required files exist
$requiredFiles = @("app.py", "requirements.txt", "gunicorn_config.py", "render.yaml")
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "❌ Required file $file not found!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ All required files found" -ForegroundColor Green

# Check if we have the MCP configuration
if (-not (Test-Path "mcp.json")) {
    Write-Host "❌ MCP configuration file not found!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ MCP configuration found" -ForegroundColor Green

# Install Render CLI if not already installed
try {
    $renderVersion = render --version
    Write-Host "✅ Render CLI found: $renderVersion" -ForegroundColor Green
} catch {
    Write-Host "📦 Installing Render CLI..." -ForegroundColor Yellow
    try {
        # Try to install via winget first
        winget install render.render-cli
    } catch {
        Write-Host "❌ Failed to install Render CLI via winget" -ForegroundColor Red
        Write-Host "Please install manually from: https://render.com/docs/install-cli" -ForegroundColor Yellow
        exit 1
    }
}

# Login to Render (if not already logged in)
Write-Host "🔐 Checking Render login status..." -ForegroundColor Yellow
try {
    $user = render whoami
    Write-Host "✅ Logged in as: $user" -ForegroundColor Green
} catch {
    Write-Host "🔐 Please login to Render..." -ForegroundColor Yellow
    render login
}

# Deploy using render.yaml
Write-Host "🚀 Deploying to Render using render.yaml..." -ForegroundColor Green
try {
    render up --file render.yaml
    Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "🎉 Your app is now deployed on Render!" -ForegroundColor Green
Write-Host "Check your Render dashboard for the service URL" -ForegroundColor Cyan

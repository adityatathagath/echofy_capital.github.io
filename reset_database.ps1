# Database Reset Script for Echofy Capital
# This PowerShell script safely resets the database for production launch

Write-Host "🗄️  Echofy Capital Database Reset" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# Check if reset script exists
if (-not (Test-Path "reset_database.py")) {
    Write-Host "❌ reset_database.py not found in current directory." -ForegroundColor Red
    exit 1
}

Write-Host "⚠️  WARNING: This will delete ALL existing data!" -ForegroundColor Yellow
Write-Host "This includes:" -ForegroundColor Yellow
Write-Host "  - All users (except default admin)" -ForegroundColor Yellow  
Write-Host "  - All contributors" -ForegroundColor Yellow
Write-Host "  - All transactions" -ForegroundColor Yellow
Write-Host "  - All withdrawal requests" -ForegroundColor Yellow
Write-Host "  - All trade records" -ForegroundColor Yellow
Write-Host ""

# Confirmation prompt
$confirmation = Read-Host "Are you sure you want to proceed? Type 'YES' to confirm"

if ($confirmation -eq "YES") {
    Write-Host ""
    Write-Host "🚀 Starting database reset..." -ForegroundColor Green
    
    # Run the reset script
    try {
        python reset_database.py --confirm
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Database reset completed successfully!" -ForegroundColor Green
            Write-Host ""
            Write-Host "🔐 Default Admin Credentials:" -ForegroundColor Cyan
            Write-Host "   Username: admin1" -ForegroundColor White
            Write-Host "   Password: admin123" -ForegroundColor White
            Write-Host ""
            Write-Host "📋 Next Steps:" -ForegroundColor Cyan
            Write-Host "1. Test locally: python app.py" -ForegroundColor White
            Write-Host "2. Commit changes: git add . && git commit -m 'Reset database for launch'" -ForegroundColor White
            Write-Host "3. Push to GitHub: git push origin main" -ForegroundColor White
            Write-Host "4. Deploy to Render (automatic via GitHub)" -ForegroundColor White
            Write-Host "5. Change admin password after first login!" -ForegroundColor Yellow
        } else {
            Write-Host "❌ Database reset failed. Check the output above." -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Error running reset script: $_" -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "❌ Database reset cancelled." -ForegroundColor Red
    Write-Host "No changes were made to your database." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

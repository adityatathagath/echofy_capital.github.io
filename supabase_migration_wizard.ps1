#!/usr/bin/env powershell
# Complete Supabase Setup and Migration Script

Write-Host "🚀 Echofy Capital - Supabase Migration Wizard" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Step 1: Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

if (!(Test-Path "fund_manager.db")) {
    Write-Host "❌ Local database 'fund_manager.db' not found!" -ForegroundColor Red
    Write-Host "💡 Make sure you're in the project directory and have used the app before." -ForegroundColor Yellow
    exit 1
}

if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Local database found" -ForegroundColor Green
Write-Host "✅ Python is available" -ForegroundColor Green
Write-Host ""

# Step 2: Get Supabase connection string
Write-Host "🔗 Setting up Supabase connection..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Please provide your Supabase connection string." -ForegroundColor White
Write-Host "It should look like:" -ForegroundColor Gray
Write-Host "postgresql://postgres:password@db.xyz.supabase.co:5432/postgres" -ForegroundColor Gray
Write-Host ""

$connectionString = Read-Host "Enter your Supabase DATABASE_URL"

if ([string]::IsNullOrEmpty($connectionString)) {
    Write-Host "❌ No connection string provided!" -ForegroundColor Red
    exit 1
}

if (!($connectionString.StartsWith("postgresql://") -or $connectionString.StartsWith("postgres://"))) {
    Write-Host "❌ Invalid connection string! Must start with postgresql:// or postgres://" -ForegroundColor Red
    exit 1
}

# Set environment variable
$env:DATABASE_URL = $connectionString
Write-Host "✅ Database URL set successfully" -ForegroundColor Green
Write-Host ""

# Step 3: Install dependencies
Write-Host "📦 Installing required dependencies..." -ForegroundColor Yellow
try {
    pip install psycopg2-binary | Out-Null
    Write-Host "✅ PostgreSQL driver installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install psycopg2-binary" -ForegroundColor Red
    Write-Host "💡 Try: pip install psycopg2-binary" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Step 4: Setup Supabase database
Write-Host "🏗️ Setting up Supabase database schema..." -ForegroundColor Yellow
try {
    python setup_database.py
    Write-Host "✅ Supabase database setup completed" -ForegroundColor Green
} catch {
    Write-Host "❌ Database setup failed!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 5: Run migration
Write-Host "🚀 Starting data migration..." -ForegroundColor Yellow
Write-Host "This will copy all your existing data to Supabase." -ForegroundColor White
$confirm = Read-Host "Continue with migration? (y/N)"

if ($confirm -eq "y" -or $confirm -eq "Y") {
    try {
        python migrate_to_supabase.py
        Write-Host "✅ Data migration completed!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Migration failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ Migration cancelled" -ForegroundColor Yellow
    exit 0
}
Write-Host ""

# Step 6: Test local connection
Write-Host "🧪 Testing local connection..." -ForegroundColor Yellow
$testChoice = Read-Host "Test the app locally with Supabase? (y/N)"

if ($testChoice -eq "y" -or $testChoice -eq "Y") {
    Write-Host "🚀 Starting local test server..." -ForegroundColor Green
    Write-Host "Opening browser to http://127.0.0.1:5000" -ForegroundColor White
    Write-Host "Login with: admin1 / admin123" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the server when done testing." -ForegroundColor Yellow
    Write-Host ""
    
    Start-Sleep -Seconds 2
    Start-Process "http://127.0.0.1:5000"
    python app.py
}

Write-Host ""
Write-Host "🎉 Supabase setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Update your Render deployment:" -ForegroundColor White
Write-Host "   - Go to https://dashboard.render.com" -ForegroundColor Gray
Write-Host "   - Find your echofy-capital-web service" -ForegroundColor Gray
Write-Host "   - Go to Environment tab" -ForegroundColor Gray
Write-Host "   - Update DATABASE_URL with your Supabase connection string" -ForegroundColor Gray
Write-Host "   - Save and redeploy" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Test production deployment:" -ForegroundColor White
Write-Host "   - Visit https://echofy-capital-web.onrender.com" -ForegroundColor Gray
Write-Host "   - Login and verify all data is present" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Security:" -ForegroundColor White
Write-Host "   - Change admin password after first login" -ForegroundColor Gray
Write-Host "   - Keep your Supabase credentials secure" -ForegroundColor Gray
Write-Host ""
Write-Host "Your database is now permanent and will never expire! 🎊" -ForegroundColor Green

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

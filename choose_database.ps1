#!/usr/bin/env powershell
# Quick Database Setup Script for Windows

Write-Host "🗄️ Free Database Setup for Echofy Capital" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

Write-Host ""
Write-Host "🎯 Recommended Free Database Providers:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. 🟢 Supabase (PostgreSQL) - RECOMMENDED" -ForegroundColor Green
Write-Host "   • 2 projects, 500MB storage, unlimited requests"
Write-Host "   • Permanent free tier, excellent features"
Write-Host "   • Sign up: https://supabase.com"
Write-Host ""

Write-Host "2. 🟣 Neon (PostgreSQL)" -ForegroundColor Magenta  
Write-Host "   • 3 projects, 0.5GB storage per database"
Write-Host "   • Serverless PostgreSQL, instant scaling"
Write-Host "   • Sign up: https://neon.tech"
Write-Host ""

Write-Host "3. 🔵 PlanetScale (MySQL)" -ForegroundColor Blue
Write-Host "   • 1 database, 5GB storage, 1 billion reads/month" 
Write-Host "   • Large storage, MySQL compatible"
Write-Host "   • Sign up: https://planetscale.com"
Write-Host ""

Write-Host "4. 🟡 Railway (PostgreSQL)" -ForegroundColor Yellow
Write-Host "   • $5/month credit (covers small database)"
Write-Host "   • Simple deployment, PostgreSQL"
Write-Host "   • Sign up: https://railway.app"
Write-Host ""

$choice = Read-Host "Choose your preferred provider (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🟢 Setting up Supabase..." -ForegroundColor Green
        Write-Host ""
        Write-Host "📋 Steps to set up Supabase:" -ForegroundColor Cyan
        Write-Host "1. Go to https://supabase.com and sign up" -ForegroundColor White
        Write-Host "2. Click 'New Project'" -ForegroundColor White
        Write-Host "3. Fill in:" -ForegroundColor White
        Write-Host "   - Name: echofy-capital" -ForegroundColor Gray
        Write-Host "   - Database Password: [choose secure password]" -ForegroundColor Gray
        Write-Host "   - Region: [closest to you]" -ForegroundColor Gray
        Write-Host "4. Click 'Create new project' (takes ~2 minutes)" -ForegroundColor White
        Write-Host "5. Go to Settings → Database" -ForegroundColor White
        Write-Host "6. Copy the 'Connection string' under 'Connection parameters'" -ForegroundColor White
        Write-Host "7. Replace [YOUR-PASSWORD] with your actual password" -ForegroundColor White
        Write-Host ""
        Write-Host "Example connection string:" -ForegroundColor Yellow
        Write-Host "postgresql://postgres:your-password@db.xyz.supabase.co:5432/postgres" -ForegroundColor Gray
    }
    
    "2" {
        Write-Host ""
        Write-Host "🟣 Setting up Neon..." -ForegroundColor Magenta
        Write-Host ""
        Write-Host "📋 Steps to set up Neon:" -ForegroundColor Cyan
        Write-Host "1. Go to https://neon.tech and sign up" -ForegroundColor White
        Write-Host "2. Create a new project:" -ForegroundColor White
        Write-Host "   - Project name: echofy-capital" -ForegroundColor Gray
        Write-Host "   - Region: [closest to you]" -ForegroundColor Gray
        Write-Host "3. Copy the connection string from dashboard" -ForegroundColor White
        Write-Host ""
        Write-Host "Example connection string:" -ForegroundColor Yellow
        Write-Host "postgresql://user:password@ep-xyz.us-east-2.aws.neon.tech/neondb" -ForegroundColor Gray
    }
    
    "3" {
        Write-Host ""
        Write-Host "🔵 Setting up PlanetScale..." -ForegroundColor Blue
        Write-Host ""
        Write-Host "📋 Steps to set up PlanetScale:" -ForegroundColor Cyan
        Write-Host "1. Go to https://planetscale.com and sign up" -ForegroundColor White
        Write-Host "2. Create a new database:" -ForegroundColor White
        Write-Host "   - Name: echofy-capital" -ForegroundColor Gray
        Write-Host "   - Region: [closest to you]" -ForegroundColor Gray
        Write-Host "3. Go to database → Connect" -ForegroundColor White
        Write-Host "4. Create a password and copy connection string" -ForegroundColor White
        Write-Host ""
        Write-Host "⚠️ Note: Requires minor code changes for MySQL compatibility" -ForegroundColor Yellow
        Write-Host "Example connection string:" -ForegroundColor Yellow
        Write-Host "mysql://user:password@aws.connect.psdb.cloud/echofy-capital" -ForegroundColor Gray
    }
    
    "4" {
        Write-Host ""
        Write-Host "🟡 Setting up Railway..." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "📋 Steps to set up Railway:" -ForegroundColor Cyan
        Write-Host "1. Go to https://railway.app and sign up" -ForegroundColor White
        Write-Host "2. Create new project" -ForegroundColor White
        Write-Host "3. Add PostgreSQL database" -ForegroundColor White
        Write-Host "4. Copy connection string from Variables tab" -ForegroundColor White
        Write-Host ""
        Write-Host "Example connection string:" -ForegroundColor Yellow
        Write-Host "postgresql://postgres:password@containers-us-west-xxx.railway.app:5432/railway" -ForegroundColor Gray
    }
    
    default {
        Write-Host "❌ Invalid choice. Please run the script again." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🔧 After getting your connection string:" -ForegroundColor Cyan
Write-Host "1. Set environment variable:" -ForegroundColor White
Write-Host "   `$env:DATABASE_URL='your-connection-string'" -ForegroundColor Gray
Write-Host "2. Run setup script:" -ForegroundColor White  
Write-Host "   python setup_database.py" -ForegroundColor Gray
Write-Host "3. Test locally:" -ForegroundColor White
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host "4. Deploy to Render with new DATABASE_URL" -ForegroundColor White
Write-Host ""

Write-Host "🎉 Your free database will be permanent and much better than Renders temporary solution!" -ForegroundColor Green

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

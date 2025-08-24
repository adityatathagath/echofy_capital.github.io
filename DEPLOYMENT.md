# Echofy Capital - Render Deployment Guide

This guide will help you deploy your Echofy Capital fund management application to Render with a PostgreSQL database.

## Prerequisites

- GitHub repository with your code
- Render account (free tier available)
- MCP server configured (already done)

## Files Overview

Your project already has all the necessary files for deployment:

- `app.py` - Main Flask application with PostgreSQL support
- `requirements.txt` - Python dependencies including psycopg2-binary
- `gunicorn_config.py` - Production server configuration
- `render.yaml` - Render deployment configuration
- `migrate_data.py` - Database migration script
- `mcp.json` - MCP server configuration

## Deployment Options

### Option 1: Deploy via Render Dashboard (Recommended)

1. **Go to Render Dashboard**
   - Visit [https://dashboard.render.com](https://dashboard.render.com)
   - Sign in with your account

2. **Create New Blueprint**
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select `echofy_capital.github.io-1`

3. **Review Configuration**
   - The `render.yaml` file will automatically configure:
     - Web service with Python environment
     - PostgreSQL database
     - Environment variables
     - Health check endpoint

4. **Deploy**
   - Click "Apply" to start deployment
   - Wait for both database and web service to be ready

### Option 2: Deploy via PowerShell Script

Run the PowerShell script:
```powershell
.\deploy-render.ps1
```

### Option 3: Deploy via Python Script

Run the Python deployment script:
```bash
python deploy-to-render.py
```

## Database Migration

After deployment, if you have existing SQLite data:

1. **Set Environment Variables**
   ```bash
   export DATABASE_URL="your_postgres_connection_string"
   export SQLITE_DB_PATH="fund_manager.db"
   ```

2. **Run Migration**
   ```bash
   python migrate_data.py
   ```

## Environment Variables

The following environment variables are automatically set:

- `FLASK_ENV=production`
- `SESSION_COOKIE_SECURE=true`
- `FLASK_DEBUG=false`
- `SECRET_KEY` (auto-generated)
- `DATABASE_URL` (from PostgreSQL database)

## Health Check

Your app includes a health check endpoint at `/health` that Render uses to monitor the service.

## Default Admin Account

The app automatically creates a default admin account:
- Username: `admin1`
- Password: `admin123`

**Important**: Change these credentials after first login!

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check `requirements.txt` for correct dependencies
   - Ensure all files are committed to GitHub

2. **Database Connection Issues**
   - Verify `DATABASE_URL` is set correctly
   - Check if PostgreSQL service is running

3. **Service Not Starting**
   - Check logs in Render dashboard
   - Verify `gunicorn_config.py` settings

### Logs

View logs in the Render dashboard:
- Go to your service
- Click "Logs" tab
- Check for error messages

## Post-Deployment

1. **Test the Application**
   - Visit your app URL
   - Login with admin credentials
   - Test all major features

2. **Security**
   - Change default admin password
   - Review environment variables
   - Enable HTTPS (automatic on Render)

3. **Monitoring**
   - Set up alerts in Render dashboard
   - Monitor database performance
   - Check health check endpoint regularly

## Support

If you encounter issues:
1. Check Render documentation
2. Review application logs
3. Verify all configuration files
4. Test locally with PostgreSQL

## Cost

- **Free Tier**: Includes 750 hours/month for web services and 90 days for databases
- **Paid Plans**: Start at $7/month for persistent databases and additional resources

---

**Happy Deploying! 🚀**

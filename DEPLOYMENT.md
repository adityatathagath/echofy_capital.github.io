# 🚀 Render Deployment Guide

This guide will help you deploy your Flask fund management application to Render with PostgreSQL.

## 📋 Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com) if you haven't already
2. **GitHub Repository**: Your code should be pushed to GitHub (already done ✅)

## 🗄️ Database Setup

### Option 1: Using Render Dashboard (Recommended)

1. **Create PostgreSQL Database**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "PostgreSQL"
   - Choose the **Free** plan
   - Database Name: `fund_manager`
   - Database User: `fund_manager_user`
   - Click "Create Database"

2. **Note Connection Details**:
   - After creation, you'll see the connection string
   - Copy the "External Database URL" (starts with `postgres://`)

### Option 2: Using Infrastructure as Code

The `render.yaml` file in your repository will automatically create both the web service and database when you connect the repository.

## 🌐 Web Service Setup

### Method 1: Using render.yaml (Recommended)

1. **Connect Repository**:
   - Go to Render Dashboard
   - Click "New" → "Blueprint"
   - Connect your GitHub repository: `adityatathagath/echofy_capital.github.io`
   - Render will automatically detect the `render.yaml` file

2. **Review Configuration**:
   - Service Name: `echofy-capital-web`
   - Environment: `python`
   - Plan: `Free`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --config gunicorn_config.py app:app`

3. **Deploy**:
   - Click "Apply" to deploy both database and web service
   - Render will automatically set up environment variables

### Method 2: Manual Setup

If you prefer manual setup:

1. **Create Web Service**:
   - Go to Render Dashboard
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Choose the following settings:
     - Environment: `Python`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn --config gunicorn_config.py app:app`

2. **Set Environment Variables**:
   ```
   FLASK_ENV=production
   SESSION_COOKIE_SECURE=true
   FLASK_DEBUG=false
   SECRET_KEY=<generate-random-secret>
   DATABASE_URL=<your-postgres-connection-string>
   ```

## 🔄 Data Migration (If you have existing data)

If you have existing data in your local SQLite database:

1. **Set DATABASE_URL locally**:
   ```bash
   export DATABASE_URL="your-postgres-connection-string"
   ```

2. **Run migration**:
   ```bash
   python migrate_data.py --confirm
   ```

## 🔍 Monitoring & Testing

1. **Health Check**: Your app includes a health check at `/health`
2. **Logs**: View logs in Render Dashboard → Your Service → Logs
3. **Database**: Monitor database in Render Dashboard → Your Database

## 🔐 Security Checklist

- ✅ CSRF protection enabled
- ✅ Password hashing implemented
- ✅ Secure session cookies
- ✅ Security headers configured
- ✅ Environment variables for secrets

## 🎯 Default Login

- **Username**: `admin1`
- **Password**: `admin123`

**⚠️ Important**: Change the default password immediately after deployment!

## 🚨 Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check `requirements.txt` is correct
   - Verify Python version in `runtime.txt`

2. **Database Connection Errors**:
   - Verify DATABASE_URL is set correctly
   - Check if PostgreSQL service is running

3. **App Won't Start**:
   - Check logs in Render Dashboard
   - Verify health check endpoint `/health`

### Getting Help:

1. Check Render logs first
2. Verify environment variables
3. Test health check endpoint
4. Review database connection

## 📞 Support

If you encounter issues:
1. Check the Render documentation
2. Review application logs
3. Test locally first with PostgreSQL

---

## 🎉 You're All Set!

Once deployed, your application will be available at:
`https://your-service-name.onrender.com`

The database will be automatically backed up by Render, and your application will be production-ready! 🚀

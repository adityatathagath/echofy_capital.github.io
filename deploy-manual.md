# Manual Deployment to Render

Since the Render CLI has some issues, here's how to deploy manually:

## Step 1: Push to GitHub

1. Commit and push your changes:
```bash
git add .
git commit -m "Fix delete contributor functionality and prepare for Render deployment"
git push origin main
```

## Step 2: Deploy via Render Dashboard

1. **Go to Render Dashboard**
   - Visit [https://dashboard.render.com](https://dashboard.render.com)
   - Sign in with your account

2. **Create New Blueprint**
   - Click "New" → "Blueprint"
   - Connect your GitHub repository: `echofy_capital.github.io-1`
   - Render will automatically detect the `render.yaml` file

3. **Review Configuration**
   - The `render.yaml` will create:
     - PostgreSQL database: `echofy-capital-db`
     - Web service: `echofy-capital-web`
     - All necessary environment variables

4. **Deploy**
   - Click "Apply" to start deployment
   - Wait for both database and web service to be ready

## Step 3: Verify Deployment

1. **Check Service Status**
   - Go to your web service
   - Verify it shows "Live" status
   - Check the logs for any errors

2. **Test the Application**
   - Visit your app URL (e.g., `https://echofy-capital-web.onrender.com`)
   - Login with admin credentials:
     - Username: `admin1`
     - Password: `admin123`

3. **Test Delete Functionality**
   - Go to "Manage Contributors"
   - Try to delete a contributor
   - Check if it works properly

## Step 4: Data Migration (if needed)

If you have existing SQLite data:

1. **Get Database URL**
   - Go to your PostgreSQL database in Render
   - Copy the "External Database URL"

2. **Set Environment Variables**
   ```bash
   export DATABASE_URL="your_postgres_connection_string"
   export SQLITE_DB_PATH="fund_manager.db"
   ```

3. **Run Migration**
   ```bash
   python migrate_data.py
   ```

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check `requirements.txt` for correct dependencies
   - Ensure all files are committed to GitHub

2. **Database Connection Issues**
   - Verify `DATABASE_URL` is set correctly
   - Check if PostgreSQL service is running

3. **Delete Not Working**
   - Check browser console for JavaScript errors
   - Verify CSRF token is being sent
   - Check application logs in Render dashboard

### Logs

View logs in the Render dashboard:
- Go to your service
- Click "Logs" tab
- Check for error messages

## Post-Deployment

1. **Security**
   - Change default admin password
   - Review environment variables
   - Enable HTTPS (automatic on Render)

2. **Monitoring**
   - Set up alerts in Render dashboard
   - Monitor database performance
   - Check health check endpoint regularly

---

**Your app will be available at: `https://echofy-capital-web.onrender.com`**

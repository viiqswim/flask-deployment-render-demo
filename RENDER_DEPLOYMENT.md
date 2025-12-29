# Deploying Flask App to Render

This guide walks through deploying a Flask application to Render using both the web dashboard and the Render CLI.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Project Requirements](#project-requirements)
- [Deployment Methods](#deployment-methods)
  - [Method 1: Web Dashboard (Recommended for First Deploy)](#method-1-web-dashboard-recommended-for-first-deploy)
  - [Method 2: Render CLI](#method-2-render-cli)
- [Verification](#verification)
- [Managing Your Deployment](#managing-your-deployment)
- [Troubleshooting](#troubleshooting)
- [Important Notes](#important-notes)

## Prerequisites

Before deploying to Render, ensure you have:

1. **A Render Account**
   - Sign up at https://render.com
   - Free tier available for testing

2. **A GitHub Account**
   - Your code must be in a GitHub repository
   - Render deploys directly from GitHub

3. **Git Repository Setup**
   ```bash
   # Initialize git if not already done
   git init

   # Add your files
   git add .

   # Commit your changes
   git commit -m "Initial commit"

   # Create a repository on GitHub, then:
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

## Project Requirements

Your Flask project must include:

### 1. `requirements.txt`
```
Flask==3.0.0
gunicorn==21.2.0
```

**Important:** Gunicorn is required for production deployment on Render.

### 2. Flask Application
Your app should be in a file (e.g., `app.py`) with the Flask app variable properly exported:
```python
from flask import Flask

app = Flask(__name__)

# Your routes here

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 3. `.gitignore`
Ensure sensitive files and Python artifacts are ignored:
```
__pycache__/
*.pyc
venv/
.env
```

## Deployment Methods

### Method 1: Web Dashboard (Recommended for First Deploy)

#### Step 1: Create a New Web Service

1. Log in to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** button
3. Select **"Web Service"**

#### Step 2: Connect Your Repository

1. Click **"Connect a repository"** (or select from already connected repos)
2. If first time: Authorize Render to access your GitHub account
3. Select your Flask app repository

#### Step 3: Configure the Service

Fill in the following settings:

- **Name:** Choose a unique name (e.g., `flask-deployment-render-demo`)
  - This will be part of your URL: `https://<name>.onrender.com`

- **Environment:** `Python 3`

- **Region:** Choose closest to your users (e.g., `Oregon (US West)`)

- **Branch:** `main` (or your primary branch)

- **Build Command:**
  ```bash
  pip install -r requirements.txt
  ```

- **Start Command:**
  ```bash
  gunicorn app:app
  ```
  - Format: `gunicorn <filename>:<app_variable>`
  - If your app is in `server.py` with variable `application`, use: `gunicorn server:application`

- **Instance Type:** `Free` (or choose a paid plan)

#### Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start your application
3. Monitor the build logs in real-time
4. Once complete, you'll see "Your service is live 🎉"

---

### Method 2: Render CLI

The Render CLI allows you to manage deployments from your terminal.

#### Step 1: Install Render CLI

**macOS (Homebrew):**
```bash
brew tap render-oss/render
brew install render
```

**Linux/WSL:**
```bash
# Download the latest release from:
# https://github.com/render-oss/render-cli/releases

# Extract and move to PATH
tar -xzf render-cli-*.tar.gz
sudo mv render /usr/local/bin/
```

**Verify Installation:**
```bash
render --version
```

#### Step 2: Authenticate

```bash
render login
```

This will open your browser to authenticate. Once complete, you'll see:
```
Successfully logged in!
```

#### Step 3: Set Workspace (if part of a team)

List available workspaces:
```bash
render workspaces list -o json
```

Set the workspace:
```bash
render config set workspace <workspace-id>
```

#### Step 4: Create Service (First Time)

If you haven't created the service via web dashboard:

1. Create the service using the web dashboard first (easier for initial setup)
2. Then manage it via CLI for subsequent deployments

#### Step 5: View Your Services

List all services:
```bash
render services list -o json
```

Get specific service details:
```bash
render services get <service-id> -o json
```

Example output:
```json
{
  "service": {
    "id": "srv-xxxxx",
    "name": "flask-deployment-render-demo",
    "type": "web_service",
    "url": "https://flask-deployment-render-demo.onrender.com",
    "branch": "main",
    "autoDeploy": "yes"
  }
}
```

#### Step 6: Trigger Deployments

Trigger a manual deployment:
```bash
render deploys create <service-id> --confirm -o json
```

The `--confirm` flag skips the confirmation prompt (useful for automation).

Monitor deployment progress:
```bash
render deploys list <service-id> -o json
```

Example output:
```json
[
  {
    "id": "dep-xxxxx",
    "status": "live",
    "createdAt": "2025-12-29T23:26:03Z",
    "finishedAt": "2025-12-29T23:27:40Z"
  }
]
```

**Deployment Statuses:**
- `build_in_progress` - Building your application
- `live` - Successfully deployed and running
- `build_failed` - Build encountered errors
- `deploy_failed` - Deployment failed

## Verification

### Test Your Endpoints

Once deployed, verify your application is working:

#### 1. Test Home Page
```bash
curl https://<your-app-name>.onrender.com
```

#### 2. Test API Endpoints
```bash
# Health check
curl https://<your-app-name>.onrender.com/api/health

# Expected response:
# {"message":"Application is running","status":"healthy"}

# Info endpoint
curl https://<your-app-name>.onrender.com/api/info

# Expected response:
# {"app_name":"Flask Demo App","description":"...","version":"1.0.0"}
```

#### 3. Check HTTP Status
```bash
curl -i https://<your-app-name>.onrender.com/api/health
```

Should return `HTTP/2 200` for successful requests.

### Using Render CLI for Verification

Get service details:
```bash
render services get <service-id> -o json
```

Check recent deployments:
```bash
render deploys list <service-id> -o json
```

## Managing Your Deployment

### Auto-Deploy

By default, Render automatically deploys when you push to your connected branch:

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push origin main

# Render automatically detects and deploys the new commit
```

### Manual Deploy via CLI

Trigger deployment without code changes:
```bash
render deploys create <service-id> --confirm -o json
```

### Environment Variables

Add environment variables via CLI or dashboard:

**Dashboard:**
1. Go to your service settings
2. Navigate to "Environment" section
3. Add key-value pairs

**Note:** Render CLI currently has limited support for environment variable management. Use the dashboard for this.

### View Service URL

```bash
render services list -o json | grep "url"
```

### Service Dashboard

Get the dashboard URL:
```bash
render services get <service-id> -o json | grep "dashboardUrl"
```

## Troubleshooting

### Service Returns 404 with "x-render-routing: no-server"

**Problem:** Free tier services spin down after 15 minutes of inactivity.

**Solution:**
- First request after inactivity takes 30-60 seconds to wake up
- This is normal for free tier
- Upgrade to paid plan for always-on service

**Test:**
```bash
# First request may be slow
curl https://<your-app-name>.onrender.com

# Wait a few seconds, then try again
sleep 5
curl https://<your-app-name>.onrender.com/api/health
```

### Build Fails: "Could not find requirements.txt"

**Solution:** Ensure `requirements.txt` is:
1. In the root directory of your repository
2. Committed to git
3. Pushed to GitHub

### Wrong Start Command

**Problem:** Service fails to start with `gunicorn` errors.

**Solution:** Verify your start command matches your file structure:
- File: `app.py`, Variable: `app` → `gunicorn app:app`
- File: `main.py`, Variable: `app` → `gunicorn main:app`
- File: `server.py`, Variable: `application` → `gunicorn server:application`

### Port Binding Issues

**Solution:** Render automatically sets the `PORT` environment variable. Gunicorn handles this automatically. If you need custom configuration, use:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

### CLI TTY Errors

**Problem:** `panic: Failed to initialize interface... could not open a new TTY`

**Solution:** Always use `-o json` flag for non-interactive output:
```bash
render services list -o json
render deploys list <service-id> -o json
```

## Important Notes

### Free Tier Limitations

- **Spin Down:** Services spin down after 15 minutes of inactivity
- **Spin Up Time:** First request takes 30-60 seconds after spin down
- **Build Minutes:** 400 build minutes per month
- **Bandwidth:** 100 GB per month

### Best Practices

1. **Health Check Endpoint:** Add a `/health` or `/api/health` endpoint
   - Configure in Render dashboard under "Health Check Path"
   - Helps Render monitor service availability

2. **Logging:** Flask logs are visible in Render dashboard under "Logs" tab

3. **Git Workflow:**
   - Keep `main` branch production-ready
   - Test locally before pushing
   - Use feature branches for development

4. **Dependencies:**
   - Pin dependency versions in `requirements.txt`
   - Update regularly for security patches

5. **Auto-Deploy:**
   - Convenient for continuous deployment
   - Disable if you prefer manual deployments

### Production Considerations

Before going to production:

1. **Use HTTPS:** Render provides free SSL certificates automatically
2. **Environment Variables:** Store secrets in environment variables, never in code
3. **Database:** Add a managed database if needed (PostgreSQL, Redis available)
4. **Monitoring:** Set up health checks and monitoring
5. **Scaling:** Upgrade to paid plan for:
   - Always-on service
   - More instances
   - Better performance
   - Custom domains

## Additional Resources

- **Render Documentation:** https://render.com/docs
- **Render CLI GitHub:** https://github.com/render-oss/render-cli
- **Render Status:** https://status.render.com
- **Support:** https://render.com/support

## Quick Reference

### Common CLI Commands

```bash
# Authentication
render login
render whoami

# Workspaces
render workspaces list -o json
render config set workspace <workspace-id>

# Services
render services list -o json
render services get <service-id> -o json

# Deployments
render deploys list <service-id> -o json
render deploys create <service-id> --confirm -o json

# Configuration
render config
```

### Service Configuration Summary

| Setting | Value |
|---------|-------|
| Environment | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Port | Automatic (via `$PORT`) |
| Auto Deploy | Enabled by default |

---

**Last Updated:** December 2025

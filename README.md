# Flask Demo App

A simple Flask boilerplate application ready for deployment on Render.

## Features

- Simple Flask application with multiple endpoints
- Health check endpoint for monitoring
- API endpoints returning JSON
- Styled home page
- Ready for production deployment with Gunicorn

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Available Endpoints

- `GET /` - Home page with application information
- `GET /api/health` - Health check endpoint
- `GET /api/info` - Application information in JSON format

## Deployment on Render

### Prerequisites
- A GitHub account
- A Render account (sign up at https://render.com)

### Steps to Deploy

1. **Push to GitHub:**
   - Create a new repository on GitHub
   - Link your local repository to GitHub:
     ```bash
     git remote add origin <your-github-repo-url>
     git push -u origin main
     ```

2. **Connect to Render:**
   - Log in to your Render dashboard
   - Click "New +" and select "Web Service"
   - Connect your GitHub account if not already connected
   - Select this repository

3. **Configure the Web Service:**
   - **Name:** Choose a name for your service
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Choose based on your needs (Free tier available)

4. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically deploy your application
   - Once deployed, you'll receive a URL like: `https://your-app-name.onrender.com`

### Environment Variables (Optional)

If you need to add environment variables:
- Go to your service settings in Render
- Navigate to "Environment" section
- Add key-value pairs as needed

## Project Structure

```
sample-flask-deployment/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Technologies Used

- **Flask 3.0.0** - Web framework
- **Gunicorn 21.2.0** - Production WSGI server

## Notes

- The app uses Gunicorn for production deployment (required by Render)
- Health check endpoint is useful for Render's monitoring
- The free tier on Render may spin down after inactivity

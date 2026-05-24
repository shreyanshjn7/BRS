# Quick Setup Guide

## Option 1: Local Setup (Recommended for Development)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Backend will be available at: `http://localhost:5000`

### Frontend Setup

```bash
# Open a new terminal
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

Frontend will be available at: `http://localhost:3000`

## Option 2: Docker Setup (Easiest)

```bash
# From the root directory
docker-compose up --build
```

Both services will start automatically:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5000`

## Testing the Application

1. Open `http://localhost:3000` in your browser
2. Use the sample data file: `sample_data/sample_statement.csv`
3. Upload the file and explore the features

## Verifying Installation

### Check Backend
Visit: `http://localhost:5000/api/health`

You should see: `{"status":"ok","message":"Bank Statement Analyzer API is running"}`

### Check Frontend
Visit: `http://localhost:3000`

You should see the Bank Statement Analyzer interface.

## Common Issues

### Backend not starting
- Make sure port 5000 is not in use
- Check if all Python packages installed correctly
- Try: `pip install --upgrade -r requirements.txt`

### Frontend not starting
- Make sure port 3000 is not in use
- Delete `node_modules` and run `npm install` again
- Clear npm cache: `npm cache clean --force`

### Connection errors
- Ensure both backend and frontend are running
- Check if firewall is blocking ports 3000 or 5000
- Verify `.env` file has correct API URL

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Try uploading the sample CSV file
3. Customize categories in `backend/app.py`
4. Deploy to production when ready

## Production Deployment

### Backend (Python)
- Use Gunicorn: `gunicorn -w 4 app:app`
- Set environment variables
- Use PostgreSQL/MySQL for data persistence (if needed)

### Frontend (React)
```bash
npm run build
# Serve the build folder using nginx or any static server
```

### Using Cloud Services
- **Heroku**: Push both apps separately
- **AWS**: Use Elastic Beanstalk or EC2
- **DigitalOcean**: Use App Platform
- **Vercel**: For frontend only, backend on separate service

## Support

For detailed feature documentation, see [README.md](README.md)

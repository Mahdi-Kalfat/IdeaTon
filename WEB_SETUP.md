# Web Application Setup Guide

Complete guide to set up and run the Light Detection web application.

## Prerequisites

- Python 3.8+ installed
- Trained model (`light_detection_model.h5`)
- MongoDB installed and running

---

## Step 1: Install MongoDB

### Option A: MongoDB Community Server (Recommended)

1. **Download MongoDB**
   - Visit: https://www.mongodb.com/try/download/community
   - Download MongoDB Community Server for Windows
   - Run the installer

2. **Install MongoDB**
   - Choose "Complete" installation
   - Install as a Windows Service (recommended)
   - Optionally install MongoDB Compass (GUI tool)

3. **Verify Installation**
   ```powershell
   mongo --version
   ```

### Option B: MongoDB Atlas (Cloud - Free Tier)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a free cluster
4. Get your connection string
5. Update `.env` file with your connection string

### Option C: Docker (If you have Docker installed)

```powershell
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

---

## Step 2: Install Python Dependencies

```powershell
# Install web application dependencies
pip install -r requirements-web.txt
```

**Note**: If you already installed the ML dependencies, you can install just the web packages:

```powershell
pip install flask flask-cors pymongo python-dotenv
```

---

## Step 3: Configure Environment (Optional)

Create a `.env` file in the project root:

```bash
MONGO_URI=mongodb://localhost:27017/
FLASK_ENV=development
```

**For MongoDB Atlas**, use your connection string:
```bash
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

---

## Step 4: Run the Web Application

```powershell
python app.py
```

You should see:
```
✓ Connected to MongoDB: light_detection
✓ Model loaded successfully: light_detection_model.h5

Starting server at http://localhost:5000
```

---

## Step 5: Access the Application

Open your browser and go to:
```
http://localhost:5000
```

---

## Using the Application

### 1. Upload Image
- **Drag & drop** an image onto the upload area, OR
- Click "**Select Image**" to browse files
- Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP
- Maximum size: 16MB

### 2. Analyze
- Click "**Analyze Image**" button
- Wait for prediction (usually 1-2 seconds)
- View the result with confidence score

### 3. View History
- All predictions are automatically saved to MongoDB
- View past predictions in the history table
- See statistics in the header (Total, Lights ON, Lights OFF)

### 4. Manage History
- **Refresh**: Update the history table
- **Clear All**: Delete all prediction history from database

---

## API Endpoints

The application provides a REST API:

### POST `/api/predict`
Upload and analyze an image
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5000/api/predict
```

### GET `/api/history?limit=50`
Get prediction history
```bash
curl http://localhost:5000/api/history
```

### GET `/api/stats`
Get prediction statistics
```bash
curl http://localhost:5000/api/stats
```

### GET `/api/prediction/<id>`
Get specific prediction with image
```bash
curl http://localhost:5000/api/prediction/507f1f77bcf86cd799439011
```

### DELETE `/api/clear-history`
Clear all prediction history
```bash
curl -X DELETE http://localhost:5000/api/clear-history
```

### GET `/health`
Health check endpoint
```bash
curl http://localhost:5000/health
```

---

## Database Structure

**Database**: `light_detection`  
**Collection**: `predictions`

Document schema:
```json
{
  "_id": "ObjectId",
  "filename": "image.jpg",
  "prediction": "LIGHTS ON",
  "confidence": 95.5,
  "raw_score": 0.955,
  "timestamp": "2024-01-01T12:00:00",
  "image_data": "base64_encoded_image"
}
```

---

## Troubleshooting

### Model Not Found
```
⚠ Error loading model: [Errno 2] No such file or directory: 'light_detection_model.h5'
```
**Solution**: Train the model first
```powershell
python train_model.py
```

### MongoDB Connection Error
```
⚠ MongoDB connection error: [Errno 111] Connection refused
```
**Solution**: Make sure MongoDB is running
```powershell
# Check if MongoDB service is running
net start MongoDB
```

### Port Already in Use
```
OSError: [Errno 98] Address already in use
```
**Solution**: Change the port in `app.py` or stop the other process
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### File Upload Fails
- Check file size (max 16MB)
- Check file format (only images allowed)
- Check `uploads/` folder permissions

### Cannot Access from Other Devices
To allow access from other devices on your network:
1. Make sure `host='0.0.0.0'` in `app.py`
2. Find your local IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
3. Access from other devices: `http://YOUR_IP:5000`
4. Check firewall settings

---

## Production Deployment

For production use:

1. **Disable Debug Mode**
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

2. **Use Production Server**
   ```powershell
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set Environment Variables**
   ```bash
   FLASK_ENV=production
   MONGO_URI=your_production_mongo_uri
   ```

4. **Enable HTTPS**
   - Use a reverse proxy (nginx, Apache)
   - Get SSL certificate (Let's Encrypt)

5. **Secure MongoDB**
   - Enable authentication
   - Use strong passwords
   - Restrict network access

---

## Features

✅ **Drag & Drop Upload** - Easy image upload interface  
✅ **Real-time Prediction** - Instant AI analysis  
✅ **History Tracking** - All predictions saved to MongoDB  
✅ **Statistics Dashboard** - View prediction stats  
✅ **Responsive Design** - Works on desktop and mobile  
✅ **REST API** - Integrate with other applications  
✅ **Image Storage** - Images stored as base64 in database  

---

## System Requirements

- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB for model + dependencies
- **Network**: Internet for first-time package installation
- **Browser**: Modern browser (Chrome, Firefox, Edge, Safari)

---

## Need Help?

1. Check the main `README.md` for model training
2. Check MongoDB logs: `C:\Program Files\MongoDB\Server\*\log\`
3. Check Flask logs in the terminal
4. Verify model file exists: `light_detection_model.h5`

---

**Enjoy your Light Detection Web Application! 💡**

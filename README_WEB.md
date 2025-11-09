# Light Detection Web Application

A modern web interface for the Light Detection AI model with MongoDB integration for tracking prediction history.

## 🚀 Quick Start

### 1. Install Web Dependencies

```powershell
pip install flask flask-cors pymongo python-dotenv
```

Or install all dependencies:
```powershell
pip install -r requirements-web.txt
```

### 2. Install MongoDB

**Option A: Local MongoDB**
- Download from: https://www.mongodb.com/try/download/community
- Install and run as a service

**Option B: MongoDB Atlas (Free Cloud)**
- Sign up at: https://www.mongodb.com/cloud/atlas
- Create free cluster and get connection string

**Option C: Docker**
```powershell
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 3. Start the Application

```powershell
python app.py
```

Or use the startup script:
```powershell
.\start_web.ps1
```

### 4. Open in Browser

Go to: **http://localhost:5000**

---

## 🎨 Features

### 📤 Image Upload
- **Drag & drop** interface
- Click to browse files
- Supports: PNG, JPG, JPEG, GIF, BMP, WEBP
- Max size: 16MB
- Real-time preview

### 🤖 AI Prediction
- Instant analysis (1-2 seconds)
- Confidence score percentage
- Visual result display with color coding
  - 🟡 Yellow = Lights ON
  - ⚫ Gray = Lights OFF

### 📊 History Tracking
- All predictions saved to MongoDB
- Sortable table view
- Shows:
  - Filename
  - Prediction result
  - Confidence percentage
  - Raw score
  - Timestamp
- Clear all history option

### 📈 Statistics Dashboard
- Total predictions count
- Lights ON count
- Lights OFF count
- Average confidence score

---

## 🛠️ API Endpoints

### Upload & Predict
```http
POST /api/predict
Content-Type: multipart/form-data

file: <image_file>
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "filename": "room.jpg",
  "prediction": "LIGHTS ON",
  "confidence": 94.32,
  "raw_score": 0.9432,
  "timestamp": "2024-01-01T12:00:00",
  "image_url": "/uploads/20240101_120000_room.jpg"
}
```

### Get History
```http
GET /api/history?limit=50
```

### Get Statistics
```http
GET /api/stats
```

### Get Specific Prediction
```http
GET /api/prediction/<id>
```

### Clear History
```http
DELETE /api/clear-history
```

### Health Check
```http
GET /health
```

---

## 📁 Project Structure

```
mdl/
├── app.py                      # Flask backend
├── templates/
│   └── index.html             # Web interface
├── uploads/                    # Uploaded images (auto-created)
├── predict.py                 # Prediction logic
├── light_detection_model.h5   # Trained model
├── requirements-web.txt       # Web dependencies
└── WEB_SETUP.md              # Detailed setup guide
```

---

## 🔧 Configuration

Create a `.env` file for custom configuration:

```bash
# MongoDB connection
MONGO_URI=mongodb://localhost:27017/

# Flask settings
FLASK_ENV=development
FLASK_DEBUG=True
```

### Environment Variables

- `MONGO_URI`: MongoDB connection string
- `FLASK_ENV`: Environment (development/production)
- `FLASK_DEBUG`: Enable debug mode (True/False)

---

## 💾 Database Schema

**Database**: `light_detection`  
**Collection**: `predictions`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "filename": "room.jpg",
  "prediction": "LIGHTS ON",
  "confidence": 94.32,
  "raw_score": 0.9432,
  "timestamp": ISODate("2024-01-01T12:00:00Z"),
  "image_data": "base64_encoded_string"
}
```

---

## 🚨 Troubleshooting

### Model Not Found
```
⚠ Error loading model
```
**Solution**: Train the model first
```powershell
python train_model.py
```

### MongoDB Not Connected
```
⚠ MongoDB connection error
```
**Solution**: 
1. Check if MongoDB is running: `net start MongoDB`
2. Verify connection string in `.env`
3. App will still work but won't save history

### Port Already in Use
**Solution**: Change port in `app.py`
```python
app.run(debug=True, port=5001)  # Use different port
```

---

## 🌐 Accessing from Other Devices

1. Find your computer's IP address:
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address"

2. Make sure `app.py` uses `host='0.0.0.0'`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5000)
   ```

3. On other devices, go to:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```

4. Check Windows Firewall if connection fails

---

## 📱 Screenshots

The interface includes:
- 📤 **Upload Section**: Drag & drop area with preview
- 📊 **Results Section**: Color-coded prediction display
- 📋 **History Table**: All past predictions
- 📈 **Stats Header**: Real-time statistics

---

## 🔐 Security Notes

For production deployment:
- Disable debug mode
- Use HTTPS (SSL certificate)
- Enable MongoDB authentication
- Validate all user inputs
- Use environment variables for secrets
- Implement rate limiting
- Add user authentication if needed

---

## 📚 Additional Resources

- **Full Setup Guide**: See `WEB_SETUP.md`
- **Model Training**: See `README.md`
- **API Testing**: Use tools like Postman or curl

---

## 🎯 Use Cases

- 🏠 **Smart Home**: Monitor room lighting status
- 🏢 **Building Management**: Track office light usage
- 💡 **Energy Monitoring**: Analyze lighting patterns
- 🔒 **Security**: Detect unauthorized light usage
- 📊 **Data Analysis**: Collect lighting statistics

---

## ⚡ Performance

- **Prediction Time**: 1-2 seconds per image
- **Upload Limit**: 16MB per file
- **Concurrent Users**: Supports multiple simultaneous uploads
- **Database**: Efficient MongoDB indexing on timestamps

---

**Built with**: Flask, TensorFlow, MongoDB, TailwindCSS, Font Awesome

**Happy analyzing! 💡✨**

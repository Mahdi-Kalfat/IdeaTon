# Quick Start Guide 🚀

Get your light detection model up and running in 3 simple steps!

## Step 1: Install Dependencies ⚙️

```bash
pip install -r requirements.txt
```

This will install TensorFlow and other required packages. It may take a few minutes.

## Step 2: Prepare Your Data 📁

Create a folder structure like this:

```
mdl/
  data/
    train/
      lights_on/       ← Put images with lights ON here
      lights_off/      ← Put images with lights OFF here
```

**Quick tip**: You can use your phone to take 50-100 photos of rooms with lights ON and OFF!

### Creating the folders:

**On Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Path "data\train\lights_on" -Force
New-Item -ItemType Directory -Path "data\train\lights_off" -Force
```

**On Linux/Mac:**
```bash
mkdir -p data/train/lights_on
mkdir -p data/train/lights_off
```

## Step 3: Train the Model 🎓

```bash
python train_model.py
```

This will:
- Train a deep learning model on your images
- Save the trained model as `light_detection_model.h5`
- Take about 10-30 minutes depending on your dataset

## Step 4: Make Predictions! 🔮

Once training is complete, test it on a new image:

```bash
python predict.py your_image.jpg
```

You'll see:
```
==================================================
Prediction: LIGHTS ON
Confidence: 94.32%
Raw Score: 0.9432
==================================================
```

---

## Common Issues & Solutions

### "Training directory not found"
→ Make sure you created the `data/train/lights_on` and `data/train/lights_off` folders

### "Model file not found"
→ Train the model first using `python train_model.py`

### "Not enough data" or low accuracy
→ Add more images (aim for 100+ per category)

### TensorFlow installation issues
→ Try: `pip install tensorflow-cpu` if you don't have a GPU

---

## What's Next?

✅ Train the model with your images  
✅ Test it with `predict.py`  
✅ Check out `example_usage.py` for integration ideas  
✅ Read `README.md` for detailed documentation  

**Need help?** Check the full README.md for troubleshooting tips!

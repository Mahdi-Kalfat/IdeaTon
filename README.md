# Light Detection Model

A machine learning model that detects whether lights are **ON** or **OFF** in images using deep learning and transfer learning with MobileNetV2.

## Features

- **Transfer Learning**: Uses pre-trained MobileNetV2 for better accuracy with less training data
- **Easy to Use**: Simple command-line interface for predictions
- **Batch Processing**: Analyze multiple images at once
- **High Accuracy**: Fine-tuned model with data augmentation
- **Confidence Scores**: Get probability scores for each prediction

## Installation

### 1. Clone or Download This Repository

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: This will install TensorFlow, NumPy, Pillow, Matplotlib, and scikit-learn.

## Usage

### Step 1: Prepare Training Data

Organize your training images in the following directory structure:

```
data/
  train/
    lights_on/
      image1.jpg
      image2.jpg
      ...
    lights_off/
      image1.jpg
      image2.jpg
      ...
```

**Tips for collecting data:**
- Take photos of rooms/spaces with lights ON and OFF
- Use various angles and lighting conditions
- Aim for at least 50-100 images per category (more is better)
- Images can be JPG, PNG, or other common formats

### Step 2: Train the Model

Run the training script:

```bash
python train_model.py
```

This will:
- Load and preprocess your images
- Train a deep learning model using transfer learning
- Apply data augmentation to improve generalization
- Fine-tune the model for better accuracy
- Save the trained model as `light_detection_model.h5`
- Generate a training history plot

**Training typically takes 10-30 minutes depending on your dataset size and hardware.**

### Step 3: Make Predictions

Once the model is trained, you can use it to predict if lights are ON or OFF in new images.

#### Single Image Prediction

```bash
python predict.py path/to/your/image.jpg
```

Example output:
```
==================================================
Prediction: LIGHTS ON
Confidence: 94.32%
Raw Score: 0.9432
==================================================
```

#### Batch Prediction (Multiple Images)

```bash
python predict.py path/to/images/folder --batch
```

This will process all images in the specified folder and show results for each.

#### Advanced Options

```bash
# Use a custom threshold (default is 0.5)
python predict.py image.jpg --threshold 0.7

# Use a different model file
python predict.py image.jpg --model my_custom_model.h5
```

## How It Works

### Model Architecture

1. **Base Model**: MobileNetV2 (pre-trained on ImageNet)
2. **Global Average Pooling**: Reduces spatial dimensions
3. **Dense Layers**: 128 neurons with ReLU activation
4. **Dropout**: 20% dropout for regularization
5. **Output Layer**: Single neuron with sigmoid activation (binary classification)

### Training Process

1. **Initial Training**: Trains only the top layers while keeping MobileNetV2 frozen
2. **Fine-Tuning**: Unfreezes the last 20 layers of MobileNetV2 and trains with a lower learning rate
3. **Data Augmentation**: Applies random rotations, shifts, flips, and zooms to increase dataset diversity
4. **Early Stopping**: Stops training if validation loss doesn't improve for 5 epochs

### Prediction

- Images are resized to 224x224 pixels
- Model outputs a probability score between 0 and 1
- Score ≥ 0.5 → **LIGHTS ON**
- Score < 0.5 → **LIGHTS OFF**

## Files Description

- **`train_model.py`**: Script to train the light detection model
- **`predict.py`**: Script to make predictions on new images
- **`requirements.txt`**: Python package dependencies
- **`light_detection_model.h5`**: Trained model file (generated after training)
- **`training_history.png`**: Training metrics visualization (generated after training)

## Tips for Better Results

1. **Quality Data**: Use clear, well-lit images from various angles
2. **Balanced Dataset**: Have roughly equal numbers of lights ON and OFF images
3. **Diverse Conditions**: Include different rooms, times of day, and lighting types
4. **More Data**: More training images = better accuracy (100+ per category recommended)
5. **Consistent Labeling**: Make sure images are correctly categorized

## Troubleshooting

### Model file not found
```
Error: Model file 'light_detection_model.h5' not found!
```
**Solution**: Train the model first using `python train_model.py`

### Training directory not found
```
Error: Training directory './data/train' not found!
```
**Solution**: Create the directory structure and add your training images

### Low accuracy
- Add more training images
- Ensure images are correctly labeled
- Try training for more epochs (edit `EPOCHS` in `train_model.py`)
- Check that images clearly show the difference between lights ON/OFF

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB for model and dependencies
- **GPU**: Optional but recommended for faster training (CUDA-compatible)

## Example Use Cases

- Smart home automation
- Energy usage monitoring
- Security systems
- Building management
- Automated lighting control

## License

This project is open-source and free to use for any purpose.

## Contributing

Feel free to improve this model by:
- Adding more sophisticated architectures
- Implementing multi-class detection (dim, bright, off)
- Adding real-time video detection
- Creating a web interface

---

**Happy detecting! 💡**

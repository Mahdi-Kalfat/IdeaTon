"""
Light Detection Prediction Script
This script loads the trained model and predicts if lights are ON or OFF in images.
"""

import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import argparse


class LightDetector:
    def __init__(self, model_path='light_detection_model.h5'):
        """Initialize the light detector with a trained model"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file '{model_path}' not found!")
        
        print(f"Loading model from {model_path}...")
        self.model = keras.models.load_model(model_path)
        self.img_size = (224, 224)
        print("Model loaded successfully!")
    
    def preprocess_image(self, image_path):
        """Load and preprocess an image for prediction"""
        try:
            # Load image
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to model input size
            img = img.resize(self.img_size)
            
            # Convert to numpy array
            img_array = np.array(img)
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def predict(self, image_path, threshold=0.5):
        """
        Predict if lights are ON or OFF in an image
        
        Args:
            image_path: Path to the image file
            threshold: Decision threshold (default: 0.5)
        
        Returns:
            dict: Prediction results with label, confidence, and raw score
        """
        # Preprocess image
        img_array = self.preprocess_image(image_path)
        
        if img_array is None:
            return None
        
        # Make prediction
        prediction = self.model.predict(img_array, verbose=0)
        score = float(prediction[0][0])
        
        # Determine label (assuming lights_on=1, lights_off=0 based on alphabetical order)
        if score >= threshold:
            label = "LIGHTS ON"
            confidence = score * 100
        else:
            label = "LIGHTS OFF"
            confidence = (1 - score) * 100
        
        return {
            'label': label,
            'confidence': confidence,
            'raw_score': score,
            'image_path': image_path
        }
    
    def predict_batch(self, image_paths, threshold=0.5):
        """Predict multiple images at once"""
        results = []
        for image_path in image_paths:
            result = self.predict(image_path, threshold)
            if result:
                results.append(result)
        return results


def main():
    parser = argparse.ArgumentParser(description='Detect if lights are ON or OFF in images')
    parser.add_argument('image_path', type=str, help='Path to the image file or directory')
    parser.add_argument('--model', type=str, default='light_detection_model.h5',
                        help='Path to the trained model (default: light_detection_model.h5)')
    parser.add_argument('--threshold', type=float, default=0.5,
                        help='Decision threshold (default: 0.5)')
    parser.add_argument('--batch', action='store_true',
                        help='Process all images in a directory')
    
    args = parser.parse_args()
    
    # Initialize detector
    try:
        detector = LightDetector(args.model)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease train the model first using train_model.py")
        return
    
    # Process single image or batch
    if args.batch and os.path.isdir(args.image_path):
        # Get all image files in directory
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        image_files = [
            os.path.join(args.image_path, f)
            for f in os.listdir(args.image_path)
            if os.path.splitext(f)[1].lower() in image_extensions
        ]
        
        if not image_files:
            print(f"No image files found in {args.image_path}")
            return
        
        print(f"\nProcessing {len(image_files)} images...\n")
        results = detector.predict_batch(image_files, args.threshold)
        
        # Display results
        for result in results:
            print(f"Image: {os.path.basename(result['image_path'])}")
            print(f"  Prediction: {result['label']}")
            print(f"  Confidence: {result['confidence']:.2f}%")
            print(f"  Raw Score: {result['raw_score']:.4f}\n")
    
    else:
        # Single image prediction
        if not os.path.exists(args.image_path):
            print(f"Error: Image file '{args.image_path}' not found!")
            return
        
        print(f"\nAnalyzing image: {args.image_path}\n")
        result = detector.predict(args.image_path, args.threshold)
        
        if result:
            print("=" * 50)
            print(f"Prediction: {result['label']}")
            print(f"Confidence: {result['confidence']:.2f}%")
            print(f"Raw Score: {result['raw_score']:.4f}")
            print("=" * 50)


if __name__ == "__main__":
    # If no arguments provided, show example usage
    if len(sys.argv) == 1:
        print("Light Detection Prediction Tool")
        print("\nUsage:")
        print("  python predict.py <image_path> [options]")
        print("\nExamples:")
        print("  python predict.py image.jpg")
        print("  python predict.py image.jpg --threshold 0.6")
        print("  python predict.py ./images --batch")
        print("\nOptions:")
        print("  --model PATH       Path to trained model (default: light_detection_model.h5)")
        print("  --threshold FLOAT  Decision threshold (default: 0.5)")
        print("  --batch            Process all images in a directory")
        print("\nFor help: python predict.py --help")
    else:
        main()

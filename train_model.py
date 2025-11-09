"""
Light Detection Model Training Script
This script trains a CNN model to detect if lights are ON or OFF in images.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.001

class LightDetectionModel:
    def __init__(self, img_size=IMG_SIZE):
        self.img_size = img_size
        self.model = None
        
    def build_model(self):
        """Build a transfer learning model using MobileNetV2"""
        # Load pre-trained MobileNetV2 without top layer
        base_model = MobileNetV2(
            input_shape=(*self.img_size, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze the base model
        base_model.trainable = False
        
        # Create new model
        inputs = keras.Input(shape=(*self.img_size, 3))
        
        # Pre-processing
        x = layers.Rescaling(1./127.5, offset=-1)(inputs)
        
        # Base model
        x = base_model(x, training=False)
        
        # Classification head
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.2)(x)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        outputs = layers.Dense(1, activation='sigmoid')(x)
        
        self.model = keras.Model(inputs, outputs)
        
        # Compile model
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
        
        return self.model
    
    def train(self, train_dir, validation_split=0.2):
        """
        Train the model using images from a directory structure:
        train_dir/
            lights_on/
                image1.jpg
                image2.jpg
                ...
            lights_off/
                image1.jpg
                image2.jpg
                ...
        """
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            validation_split=validation_split
        )
        
        # Training data generator
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=self.img_size,
            batch_size=BATCH_SIZE,
            class_mode='binary',
            subset='training',
            shuffle=True
        )
        
        # Validation data generator
        validation_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=self.img_size,
            batch_size=BATCH_SIZE,
            class_mode='binary',
            subset='validation',
            shuffle=False
        )
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7
            ),
            keras.callbacks.ModelCheckpoint(
                'light_detection_model_best.h5',
                monitor='val_accuracy',
                save_best_only=True
            )
        ]
        
        # Train the model
        history = self.model.fit(
            train_generator,
            validation_data=validation_generator,
            epochs=EPOCHS,
            callbacks=callbacks
        )
        
        # Fine-tuning: Unfreeze some layers and train again
        print("\n=== Fine-tuning the model ===")
        base_model = self.model.layers[2]
        base_model.trainable = True
        
        # Freeze all layers except the last 20
        for layer in base_model.layers[:-20]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE/10),
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
        
        # Continue training
        history_fine = self.model.fit(
            train_generator,
            validation_data=validation_generator,
            epochs=10,
            callbacks=callbacks
        )
        
        return history, history_fine
    
    def save_model(self, filepath='light_detection_model.h5'):
        """Save the trained model"""
        self.model.save(filepath)
        print(f"Model saved to {filepath}")
    
    def plot_training_history(self, history):
        """Plot training metrics"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Accuracy
        axes[0, 0].plot(history.history['accuracy'], label='Train')
        axes[0, 0].plot(history.history['val_accuracy'], label='Validation')
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Loss
        axes[0, 1].plot(history.history['loss'], label='Train')
        axes[0, 1].plot(history.history['val_loss'], label='Validation')
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Precision
        axes[1, 0].plot(history.history['precision'], label='Train')
        axes[1, 0].plot(history.history['val_precision'], label='Validation')
        axes[1, 0].set_title('Model Precision')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Precision')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Recall
        axes[1, 1].plot(history.history['recall'], label='Train')
        axes[1, 1].plot(history.history['val_recall'], label='Validation')
        axes[1, 1].set_title('Model Recall')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Recall')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig('training_history.png')
        print("Training history plot saved to training_history.png")


def main():
    """Main training function"""
    # Directory containing training data
    train_dir = './data/train'
    
    # Check if training data exists
    if not os.path.exists(train_dir):
        print(f"Error: Training directory '{train_dir}' not found!")
        print("\nPlease organize your data as follows:")
        print("data/")
        print("  train/")
        print("    lights_on/")
        print("      image1.jpg")
        print("      image2.jpg")
        print("      ...")
        print("    lights_off/")
        print("      image1.jpg")
        print("      image2.jpg")
        print("      ...")
        return
    
    # Create and build model
    print("Building model...")
    light_model = LightDetectionModel()
    light_model.build_model()
    
    # Print model summary
    light_model.model.summary()
    
    # Train model
    print("\nStarting training...")
    history, history_fine = light_model.train(train_dir)
    
    # Save model
    light_model.save_model('light_detection_model.h5')
    
    # Plot training history
    light_model.plot_training_history(history)
    
    print("\nTraining complete!")
    print("Model saved as 'light_detection_model.h5'")


if __name__ == "__main__":
    main()

"""
Data Preparation Helper Script

This script helps you organize and prepare your training data.
It can:
1. Create the required directory structure
2. Move/copy images to the correct folders
3. Validate your dataset
4. Show dataset statistics
"""

import os
import shutil
from pathlib import Path


def create_directory_structure():
    """Create the required directory structure for training"""
    directories = [
        'data/train/lights_on',
        'data/train/lights_off'
    ]
    
    print("Creating directory structure...")
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created: {dir_path}")
    
    print("\nDirectory structure created successfully!")
    print("\nNext steps:")
    print("1. Add images of lights ON to: data/train/lights_on/")
    print("2. Add images of lights OFF to: data/train/lights_off/")
    print("3. Run: python train_model.py")


def validate_dataset():
    """Check if dataset is ready for training"""
    print("Validating dataset...\n")
    
    lights_on_dir = 'data/train/lights_on'
    lights_off_dir = 'data/train/lights_off'
    
    # Check if directories exist
    if not os.path.exists(lights_on_dir):
        print(f"❌ Directory not found: {lights_on_dir}")
        print("   Run this script with --create to create the structure")
        return False
    
    if not os.path.exists(lights_off_dir):
        print(f"❌ Directory not found: {lights_off_dir}")
        print("   Run this script with --create to create the structure")
        return False
    
    # Count images
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    
    lights_on_images = [
        f for f in os.listdir(lights_on_dir)
        if os.path.splitext(f)[1].lower() in image_extensions
    ]
    
    lights_off_images = [
        f for f in os.listdir(lights_off_dir)
        if os.path.splitext(f)[1].lower() in image_extensions
    ]
    
    # Display statistics
    print("=" * 50)
    print("DATASET STATISTICS")
    print("=" * 50)
    print(f"Lights ON images:  {len(lights_on_images)}")
    print(f"Lights OFF images: {len(lights_off_images)}")
    print(f"Total images:      {len(lights_on_images) + len(lights_off_images)}")
    print("=" * 50)
    
    # Validation checks
    total_images = len(lights_on_images) + len(lights_off_images)
    
    if total_images == 0:
        print("\n❌ No images found!")
        print("   Please add images to the training folders")
        return False
    
    if total_images < 20:
        print("\n⚠ WARNING: Very few images (< 20)")
        print("   Recommended: At least 50-100 images per category")
        print("   The model may not train well with so few images")
    
    elif total_images < 50:
        print("\n⚠ WARNING: Limited images (< 50)")
        print("   Recommended: At least 50-100 images per category")
        print("   Consider adding more images for better accuracy")
    
    elif total_images < 100:
        print("\n✓ Good: Decent amount of images")
        print("   You can proceed with training")
        print("   Tip: More images = better accuracy")
    
    else:
        print("\n✓ Excellent: Plenty of images!")
        print("   Your dataset looks ready for training")
    
    # Check balance
    if len(lights_on_images) > 0 and len(lights_off_images) > 0:
        ratio = max(len(lights_on_images), len(lights_off_images)) / min(len(lights_on_images), len(lights_off_images))
        
        if ratio > 3:
            print("\n⚠ WARNING: Unbalanced dataset")
            print(f"   Ratio: {ratio:.1f}:1")
            print("   Try to have roughly equal numbers in both categories")
        else:
            print(f"\n✓ Dataset is balanced (ratio: {ratio:.1f}:1)")
    
    if total_images >= 20:
        print("\n✓ Dataset is ready for training!")
        print("   Run: python train_model.py")
        return True
    
    return False


def show_sample_images():
    """Show sample image filenames from the dataset"""
    print("\nSample images in dataset:\n")
    
    lights_on_dir = 'data/train/lights_on'
    lights_off_dir = 'data/train/lights_off'
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    
    # Show lights ON samples
    if os.path.exists(lights_on_dir):
        lights_on_images = [
            f for f in os.listdir(lights_on_dir)
            if os.path.splitext(f)[1].lower() in image_extensions
        ][:5]
        
        if lights_on_images:
            print("Lights ON folder:")
            for img in lights_on_images:
                print(f"  - {img}")
        else:
            print("Lights ON folder: (empty)")
    
    print()
    
    # Show lights OFF samples
    if os.path.exists(lights_off_dir):
        lights_off_images = [
            f for f in os.listdir(lights_off_dir)
            if os.path.splitext(f)[1].lower() in image_extensions
        ][:5]
        
        if lights_off_images:
            print("Lights OFF folder:")
            for img in lights_off_images:
                print(f"  - {img}")
        else:
            print("Lights OFF folder: (empty)")


def main():
    """Main function"""
    import sys
    
    print("=" * 50)
    print("LIGHT DETECTION - DATA PREPARATION")
    print("=" * 50)
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--create':
        create_directory_structure()
    
    elif len(sys.argv) > 1 and sys.argv[1] == '--validate':
        validate_dataset()
        show_sample_images()
    
    else:
        print("Usage:")
        print("  python prepare_data.py --create     Create directory structure")
        print("  python prepare_data.py --validate   Check if data is ready")
        print()
        print("Quick Start:")
        print("1. python prepare_data.py --create")
        print("2. Add your images to data/train/lights_on and lights_off")
        print("3. python prepare_data.py --validate")
        print("4. python train_model.py")


if __name__ == "__main__":
    main()

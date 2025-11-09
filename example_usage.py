"""
Example: Using the Light Detection Model Programmatically

This script demonstrates how to use the LightDetector class in your own Python code.
"""

from predict import LightDetector
import os


def example_single_prediction():
    """Example 1: Predict a single image"""
    print("=" * 60)
    print("Example 1: Single Image Prediction")
    print("=" * 60)
    
    # Initialize the detector
    detector = LightDetector('light_detection_model.h5')
    
    # Predict on an image
    image_path = 'test_image.jpg'
    
    if os.path.exists(image_path):
        result = detector.predict(image_path)
        
        if result:
            print(f"\nImage: {result['image_path']}")
            print(f"Prediction: {result['label']}")
            print(f"Confidence: {result['confidence']:.2f}%")
            print(f"Raw Score: {result['raw_score']:.4f}")
    else:
        print(f"\nImage file '{image_path}' not found!")
        print("Please provide a valid image path.")


def example_batch_prediction():
    """Example 2: Predict multiple images"""
    print("\n" + "=" * 60)
    print("Example 2: Batch Prediction")
    print("=" * 60)
    
    # Initialize the detector
    detector = LightDetector('light_detection_model.h5')
    
    # List of images to predict
    image_paths = [
        'image1.jpg',
        'image2.jpg',
        'image3.jpg'
    ]
    
    # Filter existing images
    existing_images = [img for img in image_paths if os.path.exists(img)]
    
    if existing_images:
        results = detector.predict_batch(existing_images)
        
        print(f"\nProcessed {len(results)} images:\n")
        for result in results:
            print(f"  {os.path.basename(result['image_path'])}")
            print(f"    → {result['label']} ({result['confidence']:.1f}% confidence)\n")
    else:
        print("\nNo image files found!")
        print("Please add some test images to try batch prediction.")


def example_custom_threshold():
    """Example 3: Using a custom threshold"""
    print("\n" + "=" * 60)
    print("Example 3: Custom Threshold")
    print("=" * 60)
    
    # Initialize the detector
    detector = LightDetector('light_detection_model.h5')
    
    image_path = 'test_image.jpg'
    
    if os.path.exists(image_path):
        # Try different thresholds
        thresholds = [0.3, 0.5, 0.7, 0.9]
        
        print(f"\nTesting image '{image_path}' with different thresholds:\n")
        
        for threshold in thresholds:
            result = detector.predict(image_path, threshold=threshold)
            if result:
                print(f"  Threshold {threshold}: {result['label']} "
                      f"({result['confidence']:.1f}% confidence)")
    else:
        print(f"\nImage file '{image_path}' not found!")


def example_integration():
    """Example 4: Integration in an application"""
    print("\n" + "=" * 60)
    print("Example 4: Application Integration")
    print("=" * 60)
    
    # Initialize detector once (reuse for multiple predictions)
    detector = LightDetector('light_detection_model.h5')
    
    def check_lights_and_take_action(image_path):
        """Simulate an automation system"""
        result = detector.predict(image_path)
        
        if result:
            if result['label'] == "LIGHTS ON":
                print(f"✓ Lights detected as ON (confidence: {result['confidence']:.1f}%)")
                # In a real application, you might:
                # - Log the event
                # - Send a notification
                # - Turn off lights automatically
                # - Update a database
                return "lights_on"
            else:
                print(f"✗ Lights detected as OFF (confidence: {result['confidence']:.1f}%)")
                # In a real application, you might:
                # - Turn on lights if it's dark
                # - Send a security alert
                # - Update energy monitoring system
                return "lights_off"
        return None
    
    print("\nSimulating smart home automation...\n")
    
    # Example monitoring scenario
    test_images = ['room1.jpg', 'room2.jpg', 'room3.jpg']
    
    for i, img in enumerate(test_images, 1):
        print(f"Room {i}: ", end="")
        if os.path.exists(img):
            check_lights_and_take_action(img)
        else:
            print(f"Image '{img}' not found (using placeholder)")
    
    print("\n→ In a real system, this could trigger automated actions!")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("LIGHT DETECTION MODEL - USAGE EXAMPLES")
    print("=" * 60)
    
    # Check if model exists
    if not os.path.exists('light_detection_model.h5'):
        print("\n⚠ WARNING: Trained model not found!")
        print("Please train the model first using: python train_model.py")
        print("\nThese examples require a trained model to work.")
        return
    
    # Run examples
    try:
        example_single_prediction()
        example_batch_prediction()
        example_custom_threshold()
        example_integration()
        
        print("\n" + "=" * 60)
        print("Examples completed!")
        print("=" * 60)
        print("\nYou can modify this script to integrate light detection")
        print("into your own applications.")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Make sure you have a trained model and test images.")


if __name__ == "__main__":
    main()

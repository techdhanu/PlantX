#!/usr/bin/env python3
"""
Test script to verify soil model loading and prediction
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.soil_classifier import soil_classifier
from PIL import Image
import numpy as np

def test_model_loading():
    """Test if the model can be loaded successfully"""
    print("Testing model loading...")
    try:
        # Reset the classifier
        soil_classifier.reset_model()

        # Try to load the model
        success = soil_classifier.load_model()
        if success:
            print("✅ Model loaded successfully!")
            return True
        else:
            print("❌ Model loading failed!")
            return False
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def test_prediction():
    """Test prediction with a dummy image"""
    print("Testing prediction with dummy image...")
    try:
        # Create a dummy RGB image (224x224)
        dummy_image = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8), 'RGB')

        # Convert to bytes
        import io
        img_bytes = io.BytesIO()
        dummy_image.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()

        # Test prediction
        predictions = soil_classifier.classify_soil(img_bytes)

        if predictions and len(predictions) > 0:
            print("✅ Prediction successful!")
            for i, pred in enumerate(predictions[:3]):
                print(f"   {i+1}. {pred['soil_type']}: {pred['confidence']:.2f}%")
            return True
        else:
            print("❌ Prediction failed - no results returned!")
            return False

    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Soil Model Test ===")

    # Test 1: Model loading
    model_ok = test_model_loading()

    if model_ok:
        # Test 2: Prediction
        pred_ok = test_prediction()

        if pred_ok:
            print("🎉 All tests passed! The soil classifier is working correctly.")
        else:
            print("⚠️  Model loads but prediction failed.")
    else:
        print("⚠️  Model loading failed.")

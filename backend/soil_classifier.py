import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os
import io
import numpy as np

# Cache directory for the model
model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
model_path = os.path.join(model_dir, "soil_model2.pth")

class SoilClassifier(nn.Module):
    def __init__(self, num_classes):
        super(SoilClassifier, self).__init__()
        # Using ResNet50 as base model
        self.model = models.resnet50(weights=None)  # Updated for PyTorch 2.0+ compatibility
        num_ftrs = self.model.fc.in_features
        # Replace fc with a sequential layer to match saved model structure
        self.model.fc = nn.Sequential(
            nn.Linear(num_ftrs, num_classes)
        )

    def forward(self, x):
        return self.model(x)

class SoilTypeClassifier:
    def __init__(self):
        self.model = None
        self.labels = [
            'Alluvial soil', 'Black Soil', 'Cinder Soil', 'Clay soil',
            'Laterite Soil', 'Loamy soil', 'Peat Soil', 'Red soil',
            'Sandy soil', 'Yellow Soil'
        ]
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.initialized = False
        # ResNet50 standard preprocessing
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def reset_model(self):
        """Reset the model state"""
        self.model = None
        self.initialized = False
        print("Model state reset.")

    def load_model(self):
        if not self.initialized:
            try:
                print("Loading soil classification model...")
                self.model = SoilClassifier(len(self.labels))

                if os.path.exists(model_path):
                    print(f"Loading model from {model_path}")
                    checkpoint = torch.load(model_path, map_location=self.device)

                    # Handle different possible checkpoint formats
                    if isinstance(checkpoint, dict):
                        if 'state_dict' in checkpoint:
                            state_dict = checkpoint['state_dict']
                        elif 'model_state_dict' in checkpoint:
                            state_dict = checkpoint['model_state_dict']
                        else:
                            state_dict = checkpoint
                    else:
                        state_dict = checkpoint

                    # Clean the state dict keys and map them properly
                    cleaned_state_dict = {}
                    for k, v in state_dict.items():
                        # Remove any module prefixes
                        clean_key = k.replace('module.', '')

                        # Handle the specific fc layer mapping
                        if clean_key == 'model.fc.1.weight':
                            clean_key = 'model.fc.0.weight'
                        elif clean_key == 'model.fc.1.bias':
                            clean_key = 'model.fc.0.bias'

                        cleaned_state_dict[clean_key] = v

                    # Load the cleaned state dict
                    missing_keys, unexpected_keys = self.model.load_state_dict(cleaned_state_dict, strict=False)
                    print(f"Missing keys: {missing_keys}")
                    print(f"Unexpected keys: {unexpected_keys}")
                    print("Model weights loaded successfully")
                else:
                    print(f"Warning: Model file not found at {model_path}")
                    return False

                self.model = self.model.to(self.device)
                self.model.eval()
                self.initialized = True
                return True
            except Exception as e:
                print(f"Error loading soil model: {str(e)}")
                import traceback
                traceback.print_exc()
                return False
        return True

    def preprocess_image(self, image):
        try:
            # Ensure image is in RGB format
            if image.mode != 'RGB':
                image = image.convert('RGB')

            print(f"Original image size: {image.size}")

            # Apply the transformations
            tensor = self.transform(image)
            print(f"Tensor shape after transform: {tensor.shape}")

            # Add batch dimension
            tensor = tensor.unsqueeze(0)
            print(f"Tensor shape after unsqueeze: {tensor.shape}")

            # Move to device
            tensor = tensor.to(self.device)
            print(f"Tensor moved to device: {self.device}")

            return tensor
        except Exception as e:
            print(f"Error in preprocessing: {e}")
            import traceback
            traceback.print_exc()
            return None

    def classify_soil(self, image_path_or_bytes):
        try:
            print("Starting soil classification...")

            # Reset model state for fresh prediction
            if self.initialized:
                print("Resetting model for new prediction...")
                self.reset_model()

            if isinstance(image_path_or_bytes, str):
                print("Loading image from path...")
                image = Image.open(image_path_or_bytes).convert("RGB")
            elif hasattr(image_path_or_bytes, 'read'):
                print("Loading image from file-like object...")
                image = Image.open(image_path_or_bytes).convert("RGB")
            else:
                print("Loading image from bytes...")
                image = Image.open(io.BytesIO(image_path_or_bytes)).convert("RGB")

            if self.load_model():
                print("Model loaded successfully. Processing image...")
                input_tensor = self.preprocess_image(image)
                if input_tensor is None:
                    print("Error: Preprocessing failed.")
                    return [{"soil_type": "Error", "confidence": 0.0}]

                with torch.no_grad():
                    outputs = self.model(input_tensor)
                    raw_output = outputs[0].cpu().numpy()

                    # Debugging raw outputs
                    print(f"Raw model outputs: {raw_output}")
                    print(f"Output shape: {raw_output.shape}")

                    # Apply softmax to get probabilities
                    import numpy as np
                    exp_scores = np.exp(raw_output - np.max(raw_output))  # For numerical stability
                    probabilities = exp_scores / np.sum(exp_scores)

                    # Get top 3 predictions
                    top_indices = np.argsort(probabilities)[::-1][:3]

                    predictions = []
                    for idx in top_indices:
                        confidence = probabilities[idx] * 100
                        predictions.append({
                            "soil_type": self.labels[idx],
                            "confidence": float(confidence)
                        })
                        print(f"Prediction: {self.labels[idx]}, Confidence: {confidence:.2f}%")

                    return predictions

            print("Error: Model not loaded.")
            return [{"soil_type": "Error", "confidence": 0.0}]

        except Exception as e:
            print(f"Error during classification: {str(e)}")
            import traceback
            traceback.print_exc()
            return [{"soil_type": "Error", "confidence": 0.0}]

    def get_soil_characteristics(self, soil_type):
        """Get characteristics for the identified soil type"""
        soil_info = {
            'Alluvial soil': {
                'Water Retention': 'Good',
                'Fertility': 'High',
                'Best For': 'Rice, Wheat, Sugarcane, Jute',
                'Management': 'Regular irrigation, balanced fertilization'
            },
            'Black Soil': {
                'Water Retention': 'Very High',
                'Fertility': 'High',
                'Best For': 'Cotton, Soybeans, Wheat',
                'Management': 'Proper drainage, careful tillage when wet'
            },
            'Cinder Soil': {
                'Water Retention': 'Low',
                'Fertility': 'Low',
                'Best For': 'Succulents, Cacti',
                'Management': 'Add organic matter, frequent watering'
            },
            'Clay soil': {
                'Water Retention': 'High',
                'Fertility': 'High',
                'Best For': 'Rice, Wheat, Corn',
                'Management': 'Improve drainage, add organic matter'
            },
            'Laterite Soil': {
                'Water Retention': 'Poor',
                'Fertility': 'Low',
                'Best For': 'Cashews, Tea, Coffee',
                'Management': 'Regular fertilization, soil amendments'
            },
            'Loamy soil': {
                'Water Retention': 'Balanced',
                'Fertility': 'High',
                'Best For': 'Most crops and vegetables',
                'Management': 'Maintain organic matter content'
            },
            'Peat Soil': {
                'Water Retention': 'Very High',
                'Fertility': 'High in organic matter',
                'Best For': 'Vegetables, berries',
                'Management': 'Manage water table, pH adjustment'
            },
            'Red soil': {
                'Water Retention': 'Medium',
                'Fertility': 'Medium',
                'Best For': 'Groundnuts, Potatoes, Citrus fruits',
                'Management': 'Add organic matter, proper irrigation'
            },
            'Sandy soil': {
                'Water Retention': 'Low',
                'Fertility': 'Low',
                'Best For': 'Root vegetables, carrots',
                'Management': 'Add organic matter, frequent watering'
            },
            'Yellow Soil': {
                'Water Retention': 'Medium',
                'Fertility': 'Medium to Low',
                'Best For': 'Rice, Vegetables, Fruits',
                'Management': 'Regular fertilization, pH management'
            }
        }
        return soil_info.get(soil_type, {
            'Water Retention': 'Unknown',
            'Fertility': 'Unknown',
            'Best For': 'Unknown',
            'Management': 'Conduct soil test for specific recommendations'
        })

# Create a singleton instance
soil_classifier = SoilTypeClassifier()

# For testing
if __name__ == "__main__":
    print("Soil classifier module loaded successfully")

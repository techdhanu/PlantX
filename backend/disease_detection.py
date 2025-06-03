import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import os
import io

# Cache directory for the model
cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "disease_model_cache")

# Ensure cache directory exists
os.makedirs(cache_dir, exist_ok=True)

class PlantDiseaseDetector:
    def __init__(self):
        self.model = None
        self.processor = None
        self.labels = None
        self.initialized = False

    def load_model(self):
        """Load the model only when needed to save memory"""
        if not self.initialized:
            try:
                print("Loading plant disease detection model...")
                self.processor = AutoImageProcessor.from_pretrained(
                    "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification",
                    cache_dir=cache_dir
                )
                self.model = AutoModelForImageClassification.from_pretrained(
                    "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification",
                    cache_dir=cache_dir
                )
                self.labels = self.model.config.id2label
                self.initialized = True
                print("Model loaded successfully.")
                return True
            except Exception as e:
                print(f"Error loading model: {str(e)}")
                return False
        return True

    def detect_disease(self, image_path_or_bytes):
        """
        Detect plant disease from an image

        Args:
            image_path_or_bytes: Path to image file or bytes of the image

        Returns:
            dict: Top 3 predictions with disease names and probabilities
        """
        if not self.load_model():
            return {"error": "Failed to load model"}

        try:
            # Check if input is a file path, bytes stream, or raw bytes
            if isinstance(image_path_or_bytes, str):
                # Handle path string
                image = Image.open(image_path_or_bytes).convert("RGB")
            elif hasattr(image_path_or_bytes, 'read'):
                # Handle BytesIO or file-like object
                image = Image.open(image_path_or_bytes).convert("RGB")
            else:
                # This is a fallback that shouldn't be needed now that we're passing BytesIO objects
                image = Image.open(io.BytesIO(image_path_or_bytes)).convert("RGB")

            # Preprocess image
            inputs = self.processor(images=image, return_tensors="pt")

            # Make prediction
            with torch.no_grad():
                outputs = self.model(**inputs)

            # Get predicted class probabilities
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]

            # Get top 3 predictions
            top_3_indices = torch.topk(probabilities, 3).indices

            # Format results
            results = []
            for idx in top_3_indices:
                idx = idx.item()
                # Extract disease name and clean it up
                disease_name = self.labels[idx]
                # Remove plant name prefix if present (e.g., "Tomato_Late_blight" -> "Late blight")
                if "_" in disease_name:
                    parts = disease_name.split("_")
                    plant_name = parts[0]
                    # Rejoin the rest with spaces
                    disease_part = " ".join([p.capitalize() for p in parts[1:]])
                    formatted_name = f"{plant_name} - {disease_part}"
                else:
                    formatted_name = disease_name.replace("_", " ")

                results.append({
                    "disease": formatted_name,
                    "confidence": float(probabilities[idx].item()) * 100  # Convert to percentage
                })

            return {
                "success": True,
                "predictions": results
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_treatment_info(self, disease_name):
        """
        Get treatment information for detected plant diseases

        Args:
            disease_name: Name of the disease

        Returns:
            dict: Treatment information
        """
        # Simple generic treatments for all diseases - minimal implementation to avoid errors
        treatments = {
            "Generic": {
                "cause": "Various pathogens including fungi, bacteria, or viruses",
                "symptoms": "Symptoms vary by disease but may include spots, wilting, or abnormal growth",
                "treatment": [
                    "Remove and destroy infected plant parts",
                    "Apply appropriate fungicides or pesticides if needed",
                    "Improve air circulation around plants",
                    "Avoid overhead watering"
                ],
                "prevention": "Practice crop rotation, use resistant varieties, maintain proper plant spacing"
            },
            "Healthy": {
                "cause": "No disease detected",
                "symptoms": "Plant appears healthy with normal coloration and growth pattern",
                "treatment": [
                    "Continue regular plant care",
                    "Monitor for early signs of pests or disease",
                    "Maintain proper watering and fertilization"
                ],
                "prevention": "Regular monitoring, proper spacing, crop rotation, and sanitation will help maintain plant health"
            }
        }

        # Return generic treatment for any disease, or healthy info for healthy plants
        if "healthy" in disease_name.lower():
            return {
                "success": True,
                "treatment_info": treatments["Healthy"]
            }
        else:
            return {
                "success": True,
                "treatment_info": treatments["Generic"]
            }

# Create a singleton instance
disease_detector = PlantDiseaseDetector()

import numpy as np
from PIL import Image
import io

class SceneClassifier:
    """
    A simple classifier to detect if an image contains agricultural content (plants/farmland)
    or non-agricultural content (buildings, urban scenes, etc.)
    
    This uses color analysis and simple heuristics as a fallback when ML models are not available.
    """
    
    def __init__(self):
        self.initialized = True
        
    def classify_scene(self, image_path_or_bytes):
        """
        Classify whether the image shows agricultural content or non-agricultural content
        
        Args:
            image_path_or_bytes: Path to image file or bytes of the image
            
        Returns:
            dict: Classification result with type and confidence
        """
        try:
            # Load the image
            if isinstance(image_path_or_bytes, str):
                # Handle path string
                image = Image.open(image_path_or_bytes).convert("RGB")
            elif hasattr(image_path_or_bytes, 'read'):
                # Handle BytesIO or file-like object
                image = Image.open(image_path_or_bytes).convert("RGB")
            else:
                # Handle raw bytes
                image = Image.open(io.BytesIO(image_path_or_bytes)).convert("RGB")
                
            # Resize image for faster processing
            img_small = image.resize((100, 100))
            img_array = np.array(img_small)
            
            # Extract color features
            # Calculate average RGB values
            avg_r = np.mean(img_array[:,:,0])
            avg_g = np.mean(img_array[:,:,1])
            avg_b = np.mean(img_array[:,:,2])
            
            # Calculate green dominance (key indicator for plants)
            green_ratio = avg_g / (avg_r + avg_b + 1e-5)
            
            # Calculate color variance (buildings often have lower variance)
            color_variance = np.std(img_array)
            
            # Calculate edge density (buildings have more straight edges)
            edge_density = self._calculate_edge_density(img_array)
            
            # Determine scene type based on features
            is_agricultural = self._is_agricultural(green_ratio, color_variance, edge_density)
            
            # Calculate confidence score
            if is_agricultural:
                confidence = min(90, 50 + (green_ratio * 20) + (color_variance / 30))
            else:
                confidence = min(90, 50 + (1/green_ratio * 10) + (edge_density * 40))
                
            # Return classification result
            return {
                "scene_type": "agricultural" if is_agricultural else "non_agricultural",
                "confidence": float(confidence),
                "details": {
                    "green_ratio": float(green_ratio),
                    "color_variance": float(color_variance),
                    "edge_density": float(edge_density)
                }
            }
            
        except Exception as e:
            print(f"Error in scene classification: {str(e)}")
            # Return default classification with error
            return {
                "scene_type": "unknown",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _calculate_edge_density(self, img_array):
        """
        Calculate a simplified edge density metric from image array
        
        Args:
            img_array: Numpy array of image
            
        Returns:
            float: Edge density score (higher for more edges)
        """
        try:
            # Calculate horizontal and vertical gradients
            hor_gradient = np.abs(img_array[:, 1:, :] - img_array[:, :-1, :]).mean()
            ver_gradient = np.abs(img_array[1:, :, :] - img_array[:-1, :, :]).mean()
            
            # Combine gradients
            edge_score = (hor_gradient + ver_gradient) / 2
            
            # Normalize to 0-1 range (typical values are 0-50)
            return min(1.0, edge_score / 50.0)
        except:
            return 0.5  # Default value
    
    def _is_agricultural(self, green_ratio, color_variance, edge_density):
        """
        Determine if image is agricultural based on calculated features
        
        Args:
            green_ratio: Ratio of green channel to other colors
            color_variance: Variance in image colors
            edge_density: Density of edges in the image
            
        Returns:
            bool: True if image is likely agricultural, False otherwise
        """
        # Agricultural scenes typically have:
        # 1. Higher green ratio
        # 2. Medium to high color variance
        # 3. Lower edge density (fewer straight lines)
        
        # Simple decision tree
        if green_ratio > 1.1:  # Strong green dominance
            return True
        elif edge_density > 0.7 and green_ratio < 0.9:  # Many edges and not much green
            return False
        elif color_variance > 50 and green_ratio > 0.9:  # Varied colors with some green
            return True
        else:
            # Default case - use green ratio as deciding factor
            return green_ratio > 1.0
    
    def get_scene_guidance(self, scene_type):
        """
        Get guidance message based on scene classification
        
        Args:
            scene_type: Type of scene detected
            
        Returns:
            dict: Guidance information
        """
        if scene_type == "agricultural":
            return {
                "status": "Valid Image",
                "message": "This image appears to contain plants or agricultural content and is suitable for disease detection.",
                "action": "continue"
            }
        elif scene_type == "non_agricultural":
            return {
                "status": "Non-Agricultural Image",
                "message": "This image appears to show a building or non-plant scene. For accurate disease detection, please upload an image of plants or crops.",
                "action": "retry"
            }
        else:
            return {
                "status": "Unknown Scene",
                "message": "Unable to determine if this image contains plants. For best results, please ensure your image clearly shows the plant you want to analyze.",
                "action": "warning"
            }

# Create a singleton instance
scene_classifier = SceneClassifier()

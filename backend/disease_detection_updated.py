import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import os

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
            # Check if input is a file path or bytes
            if isinstance(image_path_or_bytes, str):
                image = Image.open(image_path_or_bytes).convert("RGB")
            else:
                image = Image.open(image_path_or_bytes).convert("RGB")

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
        # Comprehensive disease treatments with detailed actionable recommendations
        treatments = {
            "Tomato - Late blight": {
                "cause": "Caused by the water mold pathogen Phytophthora infestans",
                "symptoms": "Dark brown spots on leaves that spread rapidly, white fungal growth on undersides, fruit lesions",
                "treatment": [
                    "Apply copper-based fungicides like Bordeaux mixture every 7-10 days",
                    "Remove and destroy infected plant parts immediately",
                    "Increase spacing between plants to improve air circulation",
                    "Water at the base of plants in the morning to allow foliage to dry quickly",
                    "Rotate crops with non-solanaceous plants for at least 2 years"
                ],
                "prevention": "Plant resistant varieties, use raised beds for better drainage, apply preventative fungicide during humid weather, avoid overhead irrigation"
            },
            "Tomato - Early blight": {
                "cause": "Fungal pathogen Alternaria solani that survives in soil and plant debris",
                "symptoms": "Dark concentric rings forming target-like patterns on lower leaves, leaf yellowing and dropping",
                "treatment": [
                    "Apply fungicides containing chlorothalonil or copper at first sign of disease",
                    "Remove infected leaves and destroy (do not compost)",
                    "Mulch around plants to prevent soil splash onto leaves",
                    "Stake plants to improve air circulation"
                ],
                "prevention": "Practice crop rotation, use drip irrigation to keep foliage dry, apply mulch around plants, clean garden tools between use"
            },
            "Tomato - Leaf mold": {
                "cause": "Fungus Passalora fulva (previously Fulvia fulva), common in greenhouse conditions",
                "symptoms": "Yellow patches on upper leaf surfaces with olive-green to gray fuzzy mold on undersides",
                "treatment": [
                    "Apply fungicides containing chlorothalonil or copper",
                    "Improve greenhouse ventilation immediately",
                    "Remove severely infected leaves",
                    "Reduce humidity below 85%"
                ],
                "prevention": "Maintain good air circulation, avoid overhead watering, space plants adequately, use resistant varieties when possible"
            },
            "Tomato - Septoria leaf spot": {
                "cause": "Fungus Septoria lycopersici that overwinters in plant debris",
                "symptoms": "Small dark spots with light centers and dark edges, beginning on lower leaves",
                "treatment": [
                    "Apply fungicides with chlorothalonil, copper, or mancozeb",
                    "Remove infected leaves promptly",
                    "Avoid working with plants when wet",
                    "Apply organic fungicides like copper octanoate or sulfur for organic gardens"
                ],
                "prevention": "Practice crop rotation, remove plant debris after harvest, mulch around plants, avoid overhead irrigation"
            },
            "Tomato - Bacterial spot": {
                "cause": "Bacterial pathogens Xanthomonas spp.",
                "symptoms": "Small dark spots on leaves, stems and fruits; spots may have yellow halos; fruit lesions are raised and scabby",
                "treatment": [
                    "Apply copper-based bactericides weekly at first sign",
                    "Remove infected plant parts",
                    "Avoid overhead irrigation",
                    "Disinfect garden tools and stakes between uses",
                    "Use streptomycin sulfate in severe cases (where legally permitted)",
                    "Apply copper-based products like Copper Hydroxide or Copper Oxychloride"
                ],
                "prevention": "Use disease-free seeds and transplants, rotate crops for 2-3 years, avoid working with plants when wet, use drip irrigation"
            },
            "Tomato - Leaf Curl Virus": {
                "cause": "Tomato Yellow Leaf Curl Virus (TYLCV) transmitted by whiteflies",
                "symptoms": "Upward curling of leaves, yellow leaf edges, stunted growth, flower drop, reduced fruit production",
                "treatment": [
                    "Apply systemic insecticides containing Imidacloprid to control whitefly vectors",
                    "Remove and destroy infected plants immediately to prevent spread",
                    "Use reflective mulch to repel whiteflies",
                    "Apply neem oil or insecticidal soap to control whitefly populations",
                    "Install yellow sticky traps around plants to monitor and reduce whitefly populations"
                ],
                "prevention": "Use virus-resistant tomato varieties, control weeds that host whiteflies, cover young plants with fine mesh, maintain clean garden area, rotate planting locations"
            },
            "Tomato - Target Spot": {
                "cause": "Fungus Corynespora cassiicola that thrives in warm, humid conditions",
                "symptoms": "Concentric rings forming target-like spots on leaves, stems and fruits; leaf yellowing and premature drop",
                "treatment": [
                    "Apply fungicides containing chlorothalonil, mancozeb, or azoxystrobin",
                    "Prune plants to improve air circulation",
                    "Remove infected leaves and fruit immediately",
                    "Stake plants to keep foliage off the ground",
                    "Apply copper-based fungicides as preventative measure"
                ],
                "prevention": "Rotate crops, maintain adequate spacing between plants, avoid overhead irrigation, use mulch to prevent soil splash"
            },
            "Tomato - Spider Mites": {
                "cause": "Two-spotted spider mites (Tetranychus urticae) that thrive in hot, dry conditions",
                "symptoms": "Stippling on leaves (tiny yellow/white spots), fine webbing on undersides of leaves, bronzing of foliage, leaf drop",
                "treatment": [
                    "Spray plants forcefully with water to knock off mites",
                    "Apply insecticidal soap or horticultural oil to all leaf surfaces",
                    "Use miticides specifically labeled for spider mites in severe cases",
                    "Introduce predatory mites as biological control",
                    "Apply neem oil every 7 days until infestation is controlled"
                ],
                "prevention": "Maintain proper plant humidity, regularly inspect plants, avoid water stress, keep plants well-watered during hot periods"
            },
            "Apple - Scab": {
                "cause": "Fungus Venturia inaequalis that overwinters in fallen leaves",
                "symptoms": "Olive-green to brown velvety spots on leaves and fruits, scabby lesions on fruits",
                "treatment": [
                    "Apply fungicides containing captan or sulfur at 7-10 day intervals",
                    "Remove and destroy fallen leaves in autumn",
                    "Prune trees to improve air circulation",
                    "Thin fruit clusters to prevent fruit-to-fruit contact"
                ],
                "prevention": "Plant resistant varieties, rake and destroy fallen leaves, apply preventative fungicides starting at bud break"
            },
            "Apple - Black rot": {
                "cause": "Fungus Botryosphaeria obtusa that infects through wounds",
                "symptoms": "Circular purple or brown spots on leaves, fruit rot with concentric rings, branch cankers",
                "treatment": [
                    "Prune out diseased branches 8 inches below visible infection",
                    "Apply fungicides containing captan, myclobutanil, or thiophanate-methyl",
                    "Remove mummified fruits from trees",
                    "Improve tree vigor with proper fertilization"
                ],
                "prevention": "Maintain tree health, remove dead wood promptly, protect trees from wounds, practice good sanitation"
            },
            "Apple - Cedar Apple Rust": {
                "cause": "Fungus Gymnosporangium juniperi-virginianae that requires both apple and cedar/juniper to complete lifecycle",
                "symptoms": "Bright orange-yellow spots on leaves and fruit, orange protrusions on undersides of leaves, deformed fruit",
                "treatment": [
                    "Apply fungicides containing myclobutanil or propiconazole at 7-14 day intervals",
                    "Remove galls from nearby cedar/juniper trees during dormant season",
                    "Prune to improve air circulation in the canopy",
                    "Collect and destroy fallen infected leaves"
                ],
                "prevention": "Plant resistant apple varieties, remove nearby cedar/juniper trees if possible, apply protective fungicides starting at bud break"
            },
            "Apple - Fire Blight": {
                "cause": "Bacterium Erwinia amylovora that spreads through wind, rain and insects",
                "symptoms": "Blackened, shriveled shoots appearing as if burned, bacterial ooze, shepherd's crook appearance of shoots",
                "treatment": [
                    "Prune infected branches at least 12 inches below visible infection during dry weather",
                    "Sterilize pruning tools between cuts with 10% bleach or 70% alcohol",
                    "Apply streptomycin sprays during bloom period (where legally permitted)",
                    "Remove severely infected young trees entirely",
                    "Apply copper-based products during dormant season"
                ],
                "prevention": "Plant resistant varieties, avoid excessive nitrogen fertilization, avoid overhead irrigation, remove nearby wild hosts"
            },
            "Corn - Common rust": {
                "cause": "Fungus Puccinia sorghi spread by airborne spores",
                "symptoms": "Small, reddish-brown pustules on leaves that release powdery spores when touched",
                "treatment": [
                    "Apply fungicides containing azoxystrobin or propiconazole",
                    "Time planting to avoid peak rust season",
                    "Maintain plant vigor through proper fertilization",
                    "Remove severely affected plants if detected early"
                ],
                "prevention": "Plant resistant hybrids, schedule planting to avoid disease-favorable conditions, maintain weed control, ensure adequate plant spacing"
            },
            "Corn - Northern Leaf Blight": {
                "cause": "Fungus Setosphaeria turcica (Exserohilum turcicum) that survives in crop debris",
                "symptoms": "Large, cigar-shaped gray-green to tan lesions on leaves, lesions develop primarily on upper leaves",
                "treatment": [
                    "Apply fungicides containing azoxystrobin, propiconazole or pyraclostrobin",
                    "Time applications at early disease detection or before tasseling",
                    "Remove and destroy crop debris after harvest",
                    "Rotate with non-host crops like soybeans or alfalfa"
                ],
                "prevention": "Plant resistant hybrids, practice crop rotation for at least 1-2 years, till soil to bury crop residue, control grassy weeds"
            },
            "Corn - Gray Leaf Spot": {
                "cause": "Fungus Cercospora zeae-maydis that survives in crop residue",
                "symptoms": "Rectangular lesions restricted by leaf veins, tan to gray color, lesions may coalesce killing entire leaves",
                "treatment": [
                    "Apply fungicides containing strobilurin, triazole, or mixed-mode of action products",
                    "Time applications between tasseling and early silking stages",
                    "Maintain balanced soil fertility to promote plant health",
                    "Remove or bury crop debris after harvest"
                ],
                "prevention": "Plant resistant hybrids, rotate crops for 1-2 years, practice conservation tillage, avoid continuous corn production"
            },
            "Potato - Late blight": {
                "cause": "Oomycete pathogen Phytophthora infestans, same as tomato late blight",
                "symptoms": "Water-soaked black/brown lesions on leaves, stems and tubers; white fuzzy growth in humid conditions",
                "treatment": [
                    "Apply fungicides containing chlorothalonil, mancozeb, or copper at 5-7 day intervals",
                    "Cut foliage completely and wait 2-3 weeks before harvest if infection is severe",
                    "Destroy all infected plant material",
                    "Harvest during dry weather and allow tubers to cure properly"
                ],
                "prevention": "Plant certified disease-free seed potatoes, plant resistant varieties, avoid overhead irrigation, practice crop rotation"
            },
            "Potato - Early Blight": {
                "cause": "Fungus Alternaria solani that overwinters in plant debris and soil",
                "symptoms": "Dark brown to black target-like concentric rings on older leaves, yellowing and leaf drop, lesions on stems and tubers",
                "treatment": [
                    "Apply fungicides containing chlorothalonil, azoxystrobin, or copper-based products",
                    "Remove and destroy infected lower leaves",
                    "Hill soil around plants to prevent spores from washing onto tubers",
                    "Maintain adequate nutrition, especially nitrogen",
                    "Improve air circulation by proper spacing"
                ],
                "prevention": "Practice 3-4 year crop rotation, plant certified disease-free seed potatoes, avoid overhead irrigation, destroy volunteer potatoes"
            },
            "Grape - Black rot": {
                "cause": "Fungus Guignardia bidwellii that overwinters in mummified berries",
                "symptoms": "Circular tan spots with dark borders on leaves, black wrinkled berries",
                "treatment": [
                    "Apply fungicides containing myclobutanil, mancozeb, or captan",
                    "Remove mummified fruits from vines and ground",
                    "Prune to improve air circulation",
                    "Thin leaf canopy around fruit clusters"
                ],
                "prevention": "Clean up all fallen fruits and leaves, prune for good air circulation, begin preventative spraying early in season"
            },
            "Grape - Downy Mildew": {
                "cause": "Oomycete Plasmopara viticola that thrives in humid conditions",
                "symptoms": "Yellow to reddish-brown oily spots on upper leaf surface, white downy growth on leaf undersides, young fruit turns brown and shrivels",
                "treatment": [
                    "Apply copper-based fungicides or phosphorus acid products",
                    "Spray both sides of leaves thoroughly",
                    "Remove infected leaves and fruit",
                    "Improve air circulation through pruning",
                    "Apply fungicides containing mancozeb, captan, or metalaxyl in severe cases"
                ],
                "prevention": "Train vines for good air circulation, avoid overhead irrigation, plant resistant varieties, apply preventative fungicides before rainy periods"
            },
            "Strawberry - Leaf Scorch": {
                "cause": "Fungus Diplocarpon earlianum that overwinters in infected leaves",
                "symptoms": "Small purple to red spots on upper leaf surface that enlarge to resemble sunscald, leaf edges curl upward",
                "treatment": [
                    "Apply fungicides containing captan or myclobutanil",
                    "Remove and destroy infected leaves",
                    "Ensure adequate plant spacing for air circulation",
                    "Avoid overhead irrigation",
                    "Apply copper sulfate or Bordeaux mixture in early spring"
                ],
                "prevention": "Plant resistant varieties, practice annual renovation, use plastic mulch, practice crop rotation, maintain narrow plant rows"
            },
            "Bell Pepper - Bacterial Spot": {
                "cause": "Bacteria Xanthomonas campestris pv. vesicatoria spread by water splash and seeds",
                "symptoms": "Small, raised, water-soaked spots on leaves, stems and fruits that become brown and scabby, leaves with yellow halos",
                "treatment": [
                    "Apply copper-based bactericides at first sign of disease",
                    "Rotate with copper and mancozeb mixtures to prevent resistance",
                    "Remove infected plant parts and destroy",
                    "Avoid working with wet plants",
                    "Use plastic mulch to prevent soil splash"
                ],
                "prevention": "Use disease-free seeds and transplants, practice crop rotation, use drip irrigation, space plants adequately"
            },
            "Bell Pepper - Powdery Mildew": {
                "cause": "Fungus Leveillula taurica that thrives in warm conditions with high humidity",
                "symptoms": "White powdery patches on upper and lower leaf surfaces, yellowing leaves, premature leaf drop",
                "treatment": [
                    "Apply fungicides containing sulfur, potassium bicarbonate, or neem oil",
                    "Remove heavily infected leaves",
                    "Improve air circulation around plants",
                    "Apply water-based silicon sprays as preventative",
                    "Use biological fungicides containing Bacillus subtilis"
                ],
                "prevention": "Plant resistant varieties, maintain proper plant spacing, avoid excessive nitrogen fertilization"
            },
            "Healthy": {
                "cause": "No disease detected",
                "symptoms": "Plant appears healthy with normal coloration and growth pattern",
                "treatment": [
                    "Continue regular plant care",
                    "Monitor for early signs of pests or disease",
                    "Maintain proper watering and fertilization",
                    "Practice preventative measures"
                ],
                "prevention": "Regular monitoring, proper spacing, crop rotation, and sanitation will help maintain plant health"
            }
        }

        # Handle case variations and partial matches
        for disease_key in treatments.keys():
            if disease_name.lower() in disease_key.lower() or disease_key.lower() in disease_name.lower():
                return {
                    "success": True,
                    "treatment_info": treatments[disease_key]
                }

        # If no exact match, return a generic response
        return {
            "success": False,
            "error": "No specific treatment information available for this disease"
        }

# Create a singleton instance
disease_detector = PlantDiseaseDetector()

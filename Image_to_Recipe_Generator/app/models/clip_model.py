"""
Model for classifying food images using CLIP.
"""
import os
import json
import torch
from transformers import CLIPProcessor, CLIPModel
import logging
from pathlib import Path
from dotenv import load_dotenv
from ..utils.image_preprocessing import load_image, preprocess_image_for_clip

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class FoodClassifier:
    def __init__(self):
        """Initialize the FoodClassifier."""
        # Get the model name from environment variables or use default
        self.model_name = os.getenv("CLIP_MODEL_NAME", "openai/clip-vit-base-patch32")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load food classes
        self.load_food_classes()
        
        # Load CLIP model and processor
        self.load_model()
    
    def load_food_classes(self):
        """Load food classes from the JSON file."""
        try:
            data_dir = Path(__file__).resolve().parents[2] / "data"
            with open(data_dir / "food_classes.json", "r") as f:
                data = json.load(f)
                self.food_classes = data["classes"]
                self.class_descriptions = data["class_descriptions"]
            logger.info(f"Loaded {len(self.food_classes)} food classes")
        except Exception as e:
            logger.error(f"Error loading food classes: {e}")
            # Default to a small set of classes if file can't be loaded
            self.food_classes = ["pizza", "pasta", "sushi", "burger", "salad"]
            self.class_descriptions = {}
    
    def load_model(self):
        """Load the CLIP model and processor."""
        try:
            logger.info(f"Loading CLIP model: {self.model_name}")
            self.processor = CLIPProcessor.from_pretrained(self.model_name)
            self.model = CLIPModel.from_pretrained(self.model_name).to(self.device)
            logger.info("CLIP model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading CLIP model: {e}")
            raise RuntimeError("Failed to load CLIP model. Please check the model name and your environment.")

    def classify(self, image_input, top_k=3):
        """
        Classify a food image using CLIP.
        
        Args:
            image_input: Path to image file or file-like object.
            top_k: Number of top predictions to return.
            
        Returns:
            List of (class_name, score) tuples for the top_k predictions.
        """
        try:
            # Load and preprocess the image
            image = load_image(image_input)
            
            # Prepare text inputs for all food classes
            text_inputs = self.processor(
                text=["a photo of " + food_class for food_class in self.food_classes],
                return_tensors="pt",
                padding=True
            ).to(self.device)
            
            # Prepare image input
            image_inputs = self.processor(
                images=image,
                return_tensors="pt"
            ).to(self.device)
            
            # Get model outputs
            with torch.no_grad():
                outputs = self.model(**{**image_inputs, **text_inputs})
                
            # Calculate similarity scores
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)[0].cpu().numpy()
            
            # Get top k predictions
            top_indices = probs.argsort()[-top_k:][::-1]
            results = [
                (self.food_classes[idx], float(probs[idx]), self.class_descriptions.get(self.food_classes[idx], ""))
                for idx in top_indices
            ]
            
            return results
        
        except Exception as e:
            logger.error(f"Error during classification: {e}")
            raise RuntimeError("Failed to classify the image. Please check the input and try again.")

# For testing
if __name__ == "__main__":
    classifier = FoodClassifier()
    # Test with a sample image if available
    test_image_path = Path(__file__).resolve().parents[2] / "data" / "test_image.jpg"
    if test_image_path.exists():
        results = classifier.classify(str(test_image_path))
        for food, score, desc in results:
            print(f"{food}: {score:.4f} - {desc}")

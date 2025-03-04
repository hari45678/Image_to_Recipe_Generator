# This file will contain the implementation of the recipe generator logic.
"""
Model for generating recipes using Google's Gemini API.
"""
import os
import logging
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from ..utils.recipe_formatting import parse_recipe_from_text, recipe_to_markdown

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class RecipeGenerator:
    def __init__(self):
        """Initialize the RecipeGenerator."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.error("GEMINI_API_KEY not found in environment variables")
            raise ValueError("GEMINI_API_KEY must be set in the environment variables.")

        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Get the list of available models
        self.models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Use the most capable model available
        if 'gemini-1.5-pro' in self.models:
            self.model_name = 'gemini-1.5-pro'
        elif 'gemini-pro' in self.models:
            self.model_name = 'gemini-pro'
        else:
            # Use first available model
            self.model_name = self.models[0] if self.models else None
            
        if not self.model_name:
            raise ValueError("No suitable Gemini model found")
            
            logger.info(f"Using Gemini model: {self.model_name}.")

        
        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)
        
        # Setup the recipe prompt template
        self.recipe_prompt = PromptTemplate(
            input_variables=["food_item", "details"],
            template="""
            Create a detailed recipe for {food_item}. {details}
            
            Please include the following sections:
            1. A title for the recipe
            2. A brief description/introduction
            3. List of ingredients with quantities
            4. Step-by-step cooking instructions
            5. Preparation time, cooking time, and servings
            6. Difficulty level
            7. Tips for best results
            
            Format the recipe with clear section headers and organize the ingredients and instructions in a clean, easily readable format.
            """
        )
    
    def generate_recipe(self, food_item: str, additional_details: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a recipe for the given food item.
        
        Args:
            food_item: The food item to generate a recipe for.
            additional_details: Optional additional details to include in the recipe generation.
            
        Returns:
            Dictionary containing the structured recipe.
        """
        try:
            # Prepare the prompt
            details = additional_details if additional_details else ""
            prompt = self.recipe_prompt.format(food_item=food_item, details=details)
            
            logger.info(f"Generating recipe for: {food_item}")
            
            # Generate content with Gemini
            response = self.model.generate_content(prompt)
            
            # Extract the recipe text
            if hasattr(response, 'text'):
                recipe_text = response.text
            else:
                recipe_text = response.parts[0].text
            
            # Parse the generated text into a structured recipe
            recipe = parse_recipe_from_text(recipe_text)
            
            # If the title is empty, use the food item as the title
            if not recipe["title"]:
                recipe["title"] = f"{food_item.title()} Recipe"
            
            # Add the source food item to the recipe
            recipe["food_item"] = food_item
            
            logger.info(f"Successfully generated recipe for {food_item}")
            return recipe
        
        except Exception as e:
            logger.error(f"Error generating recipe: {e}")
            return {
                "title": f"Recipe for {food_item}",
                "description": "We couldn't generate a complete recipe at this time.",
                "ingredients": ["Ingredients could not be generated."],
                "instructions": ["Instructions could not be generated."],
                "error": f"Error: {str(e)}"
            }

    
    def generate_recipe_from_image_results(self, 
                                          classification_results: List[tuple], 
                                          additional_prefs: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a recipe based on image classification results.
        
        Args:
            classification_results: List of (food_item, confidence, description) tuples from classifier.
            additional_prefs: Optional string with user's dietary preferences or requirements.
            
        Returns:
            Dictionary containing the structured recipe.
        """
        try:
            # Get the top food item
            top_food, confidence, description = classification_results[0]
            
            # Prepare additional details
            details = f"The image shows {top_food}."
            
            # Add alternative possibilities if confidence is low
            if confidence < 0.8 and len(classification_results) > 1:
                alternatives = [food for food, _, _ in classification_results[1:3]]
                details += f" It might also be {' or '.join(alternatives)}."
            
            # Add any food description if available
            if description:
                details += f" {description}"
            
            # Add user preferences
            if additional_prefs:
                details += f" Please consider these dietary preferences: {additional_prefs}."
            
            # Generate the recipe
            recipe = self.generate_recipe(top_food, details)
            
            # Add confidence score to the recipe
            recipe["confidence"] = confidence
            recipe["alternatives"] = [food for food, _, _ in classification_results[1:]]
            
            return recipe
        
        except Exception as e:
            logger.error(f"Error generating recipe from image results: {e}")
            # Return a basic error recipe
            return {
                "title": "Recipe could not be generated",
                "description": "We couldn't generate a recipe based on the image classification.",
                "ingredients": [],
                "instructions": [],
                "error": str(e)
            }

# For testing
if __name__ == "__main__":
    generator = RecipeGenerator()
    recipe = generator.generate_recipe("chocolate chip cookies")
    print(recipe_to_markdown(recipe))

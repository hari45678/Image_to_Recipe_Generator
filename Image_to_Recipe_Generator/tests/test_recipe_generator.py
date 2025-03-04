# This file will contain tests for the recipe generator implementation.
import pytest
from app.models.recipe_generator import RecipeGenerator

class TestRecipeGenerator:
    @pytest.fixture
    def recipe_generator(self):
        return RecipeGenerator()
    
    def test_initialization(self, recipe_generator):
        assert recipe_generator is not None
        assert recipe_generator.model_name is not None
    
    def test_generate_recipe(self, recipe_generator):
        food_item = "chocolate chip cookies"
        recipe = recipe_generator.generate_recipe(food_item)
        
        # Check recipe structure
        assert 'title' in recipe
        assert 'ingredients' in recipe
        assert 'instructions' in recipe
        
        # Check non-empty lists
        assert len(recipe['ingredients']) > 0
        assert len(recipe['instructions']) > 0
    
    def test_generate_recipe_with_preferences(self, recipe_generator):
        food_item = "vegetarian lasagna"
        additional_details = "Gluten-free, low-carb"
        
        recipe = recipe_generator.generate_recipe(
            food_item, 
            additional_details
        )
        
        # Basic checks
        assert recipe['title'] is not None
        assert len(recipe['ingredients']) > 0
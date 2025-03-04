# This file will contain functions for formatting the generated recipes.
"""
Utility functions for formatting and processing recipes.
"""
import re
import json
from typing import Dict, List, Any

def format_ingredients(ingredients_text: str) -> List[str]:
    """
    Format a block of ingredients text into a list of ingredients.
    
    Args:
        ingredients_text: String containing ingredients.
        
    Returns:
        List of formatted ingredient strings.
    """
    # Split by new lines and handle various delimiters
    if '\n' in ingredients_text:
        ingredients = [line.strip() for line in ingredients_text.split('\n') if line.strip()]
    else:
        # Try to split by other common delimiters if no newlines
        ingredients = [item.strip() for item in re.split(r'[;,]', ingredients_text) if item.strip()]
    
    # Clean up any bullets or numbers at the beginning
    ingredients = [re.sub(r'^[\d\-\*\•\.\s]+', '', ing).strip() for ing in ingredients]
    
    # Remove empty items
    ingredients = [ing for ing in ingredients if ing]
    
    return ingredients

def format_instructions(instructions_text: str) -> List[str]:
    """
    Format a block of instructions text into a list of steps.
    
    Args:
        instructions_text: String containing cooking instructions.
        
    Returns:
        List of formatted instruction steps.
    """
    # Split by numbered steps or new lines
    steps = []
    
    # Try to split by "Step X" patterns
    step_pattern = re.compile(r'Step\s+\d+[:.]\s*', re.IGNORECASE)
    if step_pattern.search(instructions_text):
        # Split by "Step X" pattern
        split_steps = step_pattern.split(instructions_text)
        # Remove any empty first element
        if split_steps and not split_steps[0].strip():
            split_steps = split_steps[1:]
        steps = [step.strip() for step in split_steps if step.strip()]
    else:
        # Try to split by numbers at the beginning of lines
        number_pattern = re.compile(r'^\s*\d+[.):]\s*', re.MULTILINE)
        if number_pattern.search(instructions_text):
            # Split by newlines first
            lines = instructions_text.split('\n')
            current_step = ""
            
            for line in lines:
                if number_pattern.match(line):
                    if current_step:
                        steps.append(current_step.strip())
                    current_step = number_pattern.sub('', line).strip()
                else:
                    if current_step:
                        current_step += " " + line.strip()
                    else:
                        current_step = line.strip()
            
            if current_step:
                steps.append(current_step.strip())
        else:
            # Just split by newlines if no other pattern is found
            steps = [line.strip() for line in instructions_text.split('\n') if line.strip()]
    
    # If we still don't have steps, try a simple period-based split
    if not steps and '.' in instructions_text:
        steps = [s.strip() + '.' for s in instructions_text.split('.') if s.strip()]
    
    return steps

def parse_recipe_from_text(recipe_text: str) -> Dict[str, Any]:
    """
    Parse recipe text into a structured format.
    
    Args:
        recipe_text: Generated recipe text.
        
    Returns:
        Dictionary with recipe components.
    """
    recipe = {
        "title": "",
        "description": "",
        "ingredients": [],
        "instructions": [],
        "prepTime": "",
        "cookTime": "",
        "servings": "",
        "difficulty": "",
        "tips": []
    }
    
    # Extract title
    title_match = re.search(r'^#\s*(.+?)$', recipe_text, re.MULTILINE) or \
                 re.search(r'^(.+?)$', recipe_text, re.MULTILINE)
    if title_match:
        recipe["title"] = title_match.group(1).strip()
    
    # Extract description
    desc_match = re.search(r'(?:description|introduction):(.*?)(?=##|\*\*ingredients|\*\*instructions|ingredients:|instructions:)', 
                          recipe_text, re.IGNORECASE | re.DOTALL)
    if desc_match:
        recipe["description"] = desc_match.group(1).strip()
    
    # Extract ingredients
    ingredients_match = re.search(r'(?:\*\*ingredients\*\*|ingredients:)(.*?)(?=\*\*instructions\*\*|instructions:|##\s*instructions|preparation:|directions:)', 
                                 recipe_text, re.IGNORECASE | re.DOTALL)
    if ingredients_match:
        ingredients_text = ingredients_match.group(1).strip()
        recipe["ingredients"] = format_ingredients(ingredients_text)
    
    # Extract instructions
    instructions_match = re.search(r'(?:\*\*instructions\*\*|instructions:|preparation:|directions:|method:)(.*?)(?=\*\*tips\*\*|tips:|##\s*tips|notes:|$)', 
                                  recipe_text, re.IGNORECASE | re.DOTALL)
    if instructions_match:
        instructions_text = instructions_match.group(1).strip()
        recipe["instructions"] = format_instructions(instructions_text)
    
    # Extract prep time
    prep_match = re.search(r'prep\s*time:?\s*([^,\n]+)', recipe_text, re.IGNORECASE)
    if prep_match:
        recipe["prepTime"] = prep_match.group(1).strip()
    
    # Extract cook time
    cook_match = re.search(r'cook\s*time:?\s*([^,\n]+)', recipe_text, re.IGNORECASE)
    if cook_match:
        recipe["cookTime"] = cook_match.group(1).strip()
    
    # Extract servings
    servings_match = re.search(r'(?:servings|yield|serves):?\s*([^,\n]+)', recipe_text, re.IGNORECASE)
    if servings_match:
        recipe["servings"] = servings_match.group(1).strip()
    
    # Extract difficulty
    difficulty_match = re.search(r'difficulty:?\s*([^,\n]+)', recipe_text, re.IGNORECASE)
    if difficulty_match:
        recipe["difficulty"] = difficulty_match.group(1).strip()
    
    # Extract tips
    tips_match = re.search(r'(?:\*\*tips\*\*|tips:|notes:)(.*?)$', recipe_text, re.IGNORECASE | re.DOTALL)
    if tips_match:
        tips_text = tips_match.group(1).strip()
        recipe["tips"] = [tip.strip() for tip in tips_text.split('\n') if tip.strip()]
    
    return recipe

def recipe_to_markdown(recipe: Dict[str, Any]) -> str:
    """
    Convert a recipe dictionary to a formatted markdown string.
    
    Args:
        recipe: Dictionary containing recipe information.
        
    Returns:
        Formatted markdown string.
    """
    md = f"# {recipe['title']}\n\n"
    
    if recipe['description']:
        md += f"{recipe['description']}\n\n"
    
    # Add prep time, cook time, servings, and difficulty if available
    meta = []
    if recipe['prepTime']:
        meta.append(f"**Prep Time:** {recipe['prepTime']}")
    if recipe['cookTime']:
        meta.append(f"**Cook Time:** {recipe['cookTime']}")
    if recipe['servings']:
        meta.append(f"**Servings:** {recipe['servings']}")
    if recipe['difficulty']:
        meta.append(f"**Difficulty:** {recipe['difficulty']}")
    
    if meta:
        md += " | ".join(meta) + "\n\n"
    
    # Ingredients
    if recipe['ingredients']:
        md += "## Ingredients\n\n"
        for ingredient in recipe['ingredients']:
            md += f"- {ingredient}\n"
        md += "\n"
    
    # Instructions
    if recipe['instructions']:
        md += "## Instructions\n\n"
        for i, step in enumerate(recipe['instructions'], 1):
            md += f"{i}. {step}\n"
        md += "\n"
    
    # Tips
    if recipe['tips']:
        md += "## Tips\n\n"
        for tip in recipe['tips']:
            md += f"- {tip}\n"
    
    return md
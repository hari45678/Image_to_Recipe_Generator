# This file will contain functions for preprocessing images before feeding them to the model.
"""
Utility functions for preprocessing images before feeding them to the models.
"""
import io
from PIL import Image
import torch
from torchvision import transforms
import numpy as np
import logging

# Configure logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def load_image(image_file):
    """
    Load an image from a file or file-like object.
    
    Args:
        image_file: A file path or file-like object containing image data.
        
    Returns:
        A PIL Image object.
    """
    try:
        if isinstance(image_file, str):
            return Image.open(image_file).convert('RGB')
        else:
            image_bytes = image_file.read()
            return Image.open(io.BytesIO(image_bytes)).convert('RGB')
    except Exception as e:
        logger.error(f"Error loading image: {e}")
        raise ValueError("Failed to load the image. Please check the file path or format.")

def preprocess_image_for_clip(image, model_name="openai/clip-vit-base-patch32"):
    """
    Preprocess an image for CLIP model.
    
    Args:
        image: PIL Image object.
        model_name: Name of the CLIP model.
        
    Returns:
        Preprocessed image tensor.
    """
    # Standard CLIP preprocessing
    preprocess = transforms.Compose([
        transforms.Resize(224, interpolation=transforms.InterpolationMode.BICUBIC),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), 
                             (0.26862954, 0.26130258, 0.27577711))
    ])
    
    return preprocess(image).unsqueeze(0)

def preprocess_image_for_vit(image, model_name="google/vit-base-patch16-224"):
    """
    Preprocess an image for Vision Transformer (ViT) model.
    
    Args:
        image: PIL Image object.
        model_name: Name of the ViT model.
        
    Returns:
        Preprocessed image tensor.
    """
    # Standard ViT preprocessing
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], 
                             std=[0.5, 0.5, 0.5])
    ])
    
    return preprocess(image).unsqueeze(0)

def get_image_features(model, processor, image):
    """
    Extract features from an image using a vision model.
    
    Args:
        model: The vision model.
        processor: The image processor for the model.
        image: PIL Image object.
        
    Returns:
        Image features.
    """
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get the image features from the model's output
    if hasattr(outputs, "image_embeds"):
        return outputs.image_embeds
    elif hasattr(outputs, "pooler_output"):
        return outputs.pooler_output
    else:
        return outputs.last_hidden_state[:, 0]  # Take the [CLS] token embedding

"""
FastAPI backend for the Image-to-Recipe Converter with Gemini AI integration.
"""

import os
import io
import base64
import google.generativeai as genai
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image

# Initialize FastAPI
app = FastAPI()

# Set up Gemini AI (Replace with your actual API key)
GENAI_API_KEY = "GEMINI_API_KEY"
genai.configure(api_key=GENAI_API_KEY)

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Validate file
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        # Check file type
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}")
        
        # Check file size (max 5MB)
        file_size = file.size
        if file_size > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Maximum 5MB allowed")

        # Read file contents
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))  # Convert bytes to Image

        # Convert image to base64
        image_base64 = encode_image_base64(image)

        # Call AI model to generate recipe
        recipe = generate_recipe_from_image(image_base64)

    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

    return {"filename": file.filename, "recipe": recipe}

def encode_image_base64(image):
    """
    Converts PIL Image to Base64 string.
    """
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")  # Convert image to PNG format
    return base64.b64encode(buffered.getvalue()).decode()

def generate_recipe_from_image(image_base64):
    """
    Sends the image to Google Gemini AI and generates a recipe.
    """
    try:
        # Use Gemini AI multimodal model
        model = genai.GenerativeModel("gemini-pro-vision")
        
        # Get response from AI
        response = model.generate_content(
            [
                {"mime_type": "image/png", "data": image_base64},
                "Generate a detailed recipe based on this image.",
            ]
        )

        return response.text if response.text else "No recipe generated"

    except Exception as e:
        return f"AI Model Error: {str(e)}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Validate file
        if not file:
            raise ValueError("No file uploaded")
        
        # Check file type
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        # Check file size (max 5MB)
        file_size = file.size
        if file_size > 5 * 1024 * 1024:
            raise ValueError("File too large. Maximum 5MB allowed")

        # Read file contents
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))  # Convert bytes to Image

        # Convert image to base64
        image_base64 = encode_image_base64(image)

        # Call AI model to generate recipe
        recipe = generate_recipe_from_image(image_base64)

    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

    return {"filename": file.filename, "recipe": recipe}

def encode_image_base64(image):
    """
    Converts PIL Image to Base64 string.
    """
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")  # Convert image to PNG format
    return base64.b64encode(buffered.getvalue()).decode()

def generate_recipe_from_image(image_base64):
    """
    Sends the image to Google Gemini AI and generates a recipe.
    """
    try:
        # Use Gemini AI multimodal model
        model = genai.GenerativeModel("gemini-pro-vision")
        
        # Get response from AI
        response = model.generate_content(
            [
                {"mime_type": "image/png", "data": image_base64},
                "Generate a detailed recipe based on this image.",
            ]
        )

        return response.text if response.text else "No recipe generated"

    except Exception as e:
        return f"AI Model Error: {str(e)}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

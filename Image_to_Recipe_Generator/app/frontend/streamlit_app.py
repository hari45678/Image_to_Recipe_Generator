import os
import streamlit as st
import requests
from PIL import Image
import time

# Improved API Configuration with Error Handling
class APIConnectionHandler:
    def __init__(self, base_url="http://localhost:8000", max_retries=3):
        self.base_url = base_url
        self.max_retries = max_retries

    def make_request(self, endpoint, method='post', files=None, data=None):
        """
        Robust API request method with retry and error handling
        
        Args:
            endpoint (str): API endpoint
            method (str): HTTP method (post/get)
            files (dict): Files to upload
            data (dict): Additional form data
        
        Returns:
            dict or None: API response or None if failed
        """
        for attempt in range(self.max_retries):
            try:
                url = f"{self.base_url}{endpoint}"
                
                # Choose request method dynamically
                if method.lower() == 'post':
                    response = requests.post(url, files=files, data=data)
                else:
                    response = requests.get(url, params=data)
                
                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.ConnectionError:
                st.warning(f"Connection attempt {attempt + 1} failed. Retrying...")
                time.sleep(2)  # Wait before retry
            
            except requests.exceptions.RequestException as e:
                st.error(f"API Request Error: {e}")
                return None
        
        # Final error if all retries fail
        st.error("Could not connect to the backend server. Please ensure it's running.")
        return None

# Modify existing functions to use the new connection handler
def classify_image(image_file, api_handler):
    """
    Robust image classification with error handling
    """
    try:
        files = {"file": image_file}
        results = api_handler.make_request("/classify", files=files)
        
        if not results:
            st.warning("No classification results received.")
            return None
        
        return results
    except Exception as e:
        st.error(f"Classification Error: {e}")
        return None

def generate_recipe(image_file, api_handler, dietary_prefs=None):
    """
    Robust recipe generation with error handling
    """
    try:
        files = {"file": image_file}
        data = {"dietary_prefs": dietary_prefs} if dietary_prefs else {}
        
        recipe = api_handler.make_request("/generate-recipe", files=files, data=data)
        
        if not recipe:
            st.warning("Could not generate recipe.")
            return None
        
        return recipe
    except Exception as e:
        st.error(f"Recipe Generation Error: {e}")
        return None

def main():
    # Initialize API Connection Handler
    api_handler = APIConnectionHandler(
        base_url=os.getenv("API_BASE_URL", "http://localhost:8000")
    )
    
    # Rest of your existing main function...
    # File uploader for image input
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_image is not None:
        # Replace direct requests calls with api_handler method calls
        classification_results = classify_image(uploaded_image, api_handler)
        
        # Define prefs_str before using it
        prefs_str = st.text_input("Enter dietary preferences (optional):")
        recipe = generate_recipe(uploaded_image, api_handler, prefs_str)

if __name__ == "__main__":
    main()
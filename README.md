# Culinary Oracle AI - Image to Recipe Generator

Transform food images into detailed recipes using AI! This application uses Google's Gemini AI to analyze food images and generate comprehensive recipes with ingredients and instructions.

## Features

- Upload food images (JPG, JPEG, PNG)
- AI-powered recipe generation
- Beautiful and intuitive user interface
- Detailed recipe output with ingredients and instructions
- Real-time processing

## Prerequisites

- Python 3.8 or higher
- Google Gemini AI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Image_to_Recipe_Generator.git
cd Image_to_Recipe_Generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Google Gemini AI API key:
```
GENAI_API_KEY=your_api_key_here
```

## Running the Application

1. Start the FastAPI backend:
```bash
cd app
uvicorn api.main:app --reload
```

2. In a new terminal, start the Streamlit frontend:
```bash
cd app
streamlit run frontend/streamlit_app.py
```

3. Open your browser and navigate to `http://localhost:8501`

## Usage

1. Upload a clear photo of the food you want to analyze
2. Click "Generate Recipe"
3. Wait for the AI to analyze the image and generate a recipe
4. View the detailed recipe with ingredients and instructions

## API Endpoints

- `POST /generate-recipe/`: Upload an image and receive a generated recipe

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
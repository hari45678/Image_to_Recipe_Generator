# Image to Recipe Generator
This project generates recipes based on images of food.
# 🍳 Image-to-Recipe Converter

## Project Overview
An AI-powered application that converts food images into detailed recipes using advanced machine learning techniques.

### Key Features
- Food image classification using CLIP/ViT
- Recipe generation with Gemini AI
- Streamlit interactive frontend
- FastAPI backend

## Prerequisites
- Python 3.8+
- pip
- Virtual Environment

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/image-to-recipe-converter.git
cd image-to-recipe-converter
```

2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Set Up Environment Variables
Create a `.env` file in the project root with the following:
```
GEMINI_API_KEY=your_gemini_api_key_here
API_BASE_URL=http://localhost:8000
```

## Running the Application

### Start the Backend API
```bash
# In one terminal
uvicorn app.api.main:app --reload
```

### Start the Streamlit Frontend
```bash
# In another terminal
streamlit run app/frontend/streamlit_app.py
```

## Project Structure
```
image-to-recipe-converter/
│
├── app/
│   ├── api/           # FastAPI backend
│   ├── frontend/      # Streamlit UI
│   ├── models/        # ML models
│   └── utils/         # Utility functions
│
├── data/              # Data files
├── tests/             # Unit tests
├── .env               # Environment variables
└── requirements.txt   # Project dependencies
```

## Technologies Used
- CLIP/ViT for Image Classification
- Gemini AI for Recipe Generation
- FastAPI for Backend
- Streamlit for Frontend
- PyTorch for Machine Learning

## Evaluation Criteria
1. **Functionality**: Converts images to recipes
2. **Code Quality**: Modular, well-documented
3. **AI Integration**: Effective use of generative models
4. **Creativity**: Unique problem-solving approach
5. **Scalability**: Handles diverse food images

## Troubleshooting
- Ensure all dependencies are installed
- Check API keys are correctly set
- Verify Python version compatibility

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Specify your license, e.g., MIT]

## Contact
[Your Name]
[Your Email/Contact Information]
```

## Future Enhancements
- Support more cuisines
- Add nutrition information
- Implement user recipe customization
```

## Deployment Notes
For production:
- Use secure environment variable management
- Implement proper error handling
- Set up logging and monitoring
```

## API Endpoints
- `/classify`: Classify food images
- `/generate-recipe`: Generate recipes from images
- `/generate-recipe-from-text`: Generate recipes from text descriptions

## Performance Metrics
- Average Classification Accuracy
- Recipe Generation Time
- User Satisfaction Rate
```

## Acknowledgments
- Thanks to Gemini AI
- Inspired by culinary technology innovations
```

## Disclaimer
This is an experimental project. Recipe suggestions should be verified for accuracy.
```
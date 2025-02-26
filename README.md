# AspAIra

AspAIra is a financial empowerment platform designed specifically for domestic workers in Dubai, providing AI-driven financial literacy education and personalized financial coaching.

## Project Structure

```
AspAIra/
├── backend/           # FastAPI backend server
│   └── app/          # Application code
├── frontend/         # Streamlit frontend application
│   └── pages/        # Application pages
├── datascience/      # Data science and ML components
│   ├── personalization/  # Personalization models
│   └── evaluation/      # Model evaluation
└── deploy/          # Deployment configurations
```

## Setup Instructions

1. Install dependencies:
   ```bash
   # Backend
   cd AspAIra/backend
   pip install -r requirements.txt

   # Frontend
   cd ../frontend
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the variables as needed

3. Start DynamoDB Local:
   ```bash
   docker run -p 8000:8000 amazon/dynamodb-local
   ```

4. Start the backend server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

5. Start the frontend application:
   ```bash
   cd frontend
   streamlit run Home.py
   ```

## Features

- Mobile-first design
- Two-part profile creation process
- AI-powered financial coaching
- Multi-language support (English and Tagalog)
- Secure user authentication
- Personalized financial recommendations

## Tech Stack

- Frontend: Streamlit
- Backend: FastAPI
- Database: DynamoDB
- AI/ML: Custom models for personalization
- Authentication: JWT-based 
# AispAIra - AI Financial Coach

AispAIra is an intelligent financial coaching platform that provides personalized guidance and expert insights to help users make informed financial decisions.

## Features

- User authentication and profile management
- Personalized financial profile creation
- Interactive financial coaching sessions
- Topic-based learning modules
- Dynamic content customization based on user preferences

## Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: Streamlit
- **Database**: Amazon DynamoDB
- **Authentication**: JWT tokens
- **Dependencies**: See requirements.txt files in backend and frontend directories

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd AispAIra
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd ../frontend
pip install -r requirements.txt
```

4. Configure AWS:
- Set up an AWS account
- Configure AWS credentials
- Create a DynamoDB table named 'AispAIra_Users' with 'email' as the primary key

5. Start the backend server:
```bash
cd backend
uvicorn app.main:app --reload
```

6. Start the frontend server:
```bash
cd frontend
streamlit run Home.py
```

## Project Structure

```
AspAIra/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── routers/
│   │       └── user.py
│   └── requirements.txt
├── frontend/
│   ├── pages/
│   │   ├── 1_Login.py
│   │   ├── 2_Profile_Form.py
│   │   └── 3_Financial_Coaching.py
│   ├── Home.py
│   └── requirements.txt
└── README.md
```

## Usage

1. Access the landing page at http://localhost:8501
2. Create an account or log in
3. Complete your financial profile
4. Explore personalized financial coaching topics

## API Documentation

The API documentation is available at http://localhost:8000/docs when the backend server is running.

## Security Notes

- Change the SECRET_KEY in production
- Configure proper AWS credentials
- Set up proper CORS settings for production
- Use environment variables for sensitive information

## License

[Your chosen license]

## Contributing

[Your contribution guidelines] 
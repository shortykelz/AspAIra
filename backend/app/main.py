from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user

app = FastAPI(title="AispAIra API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router, prefix="/api/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to AispAIra API"} 
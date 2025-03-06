from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import models, database
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Literal, Dict
import uvicorn
from dify_service import DifyService
from models import AgentInteraction

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize Dify service
dify_service = DifyService()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = database.get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = database.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = database.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/signup")
async def create_user(user: models.UserCreate):
    print(f"Received signup request for username: {user.username}")  # Debug log
    try:
        if not user.username or not user.password:
            return JSONResponse(
                status_code=400,
                content={"message": "Username and password are required"}
            )
            
        if len(user.password) < 6:
            return JSONResponse(
                status_code=400,
                content={"message": "Password must be at least 6 characters long"}
            )
            
        result = database.create_user(user.username, user.password)
        if result:
            print(f"User created successfully: {user.username}")  # Debug log
            return {"message": "User created successfully"}
        else:
            print(f"Username already exists: {user.username}")  # Debug log
            return JSONResponse(
                status_code=400,
                content={"message": "Username already exists"}
            )
    except Exception as e:
        print(f"Error in create_user: {str(e)}")  # Debug log
        return JSONResponse(
            status_code=500,
            content={"message": f"Error creating account: {str(e)}"}
        )

@app.post("/user/profile1")
async def update_profile_part1(
    profile: models.ProfilePart1,
    current_user: dict = Depends(get_current_user)
):
    print(f"Received profile update request for user: {current_user['username']}")  # Debug log
    print(f"Profile data received: {profile.dict()}")  # Debug log
    try:
        result = database.update_profile_part1(current_user["username"], profile.dict())
        if not result:
            print("Failed to update profile in database")  # Debug log
            raise HTTPException(
                status_code=500, 
                detail="Failed to update profile. Please check server logs for details."
            )
        print("Profile updated successfully")  # Debug log
        return {"message": "Profile updated successfully"}
    except Exception as e:
        print(f"Error updating profile: {str(e)}")  # Debug log
        raise HTTPException(
            status_code=400,
            detail=f"Error updating profile: {str(e)}"
        )

@app.post("/user/profile2")
async def update_profile_part2(
    profile: models.ProfilePart2,
    current_user: dict = Depends(get_current_user)
):
    result = database.update_profile_part2(current_user["username"], profile.dict())
    if not result:
        raise HTTPException(status_code=500, detail="Failed to update profile")
    return {"message": "Profile updated successfully"}

@app.get("/user/profile-status")
async def get_profile_status(current_user: dict = Depends(get_current_user)):
    status = database.get_profile_status(current_user["username"])
    return status

@app.get("/debug/users")
async def get_all_users():
    users = database.scan_all_users()
    return {"users": users}

@app.post("/chat")
async def chat_with_agent(
    message: str,
    user_id: str,
    session_id: str,
    user_profile: Dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Chat endpoint for interacting with the Dify agent
    """
    try:
        # Call Dify service
        response, interaction = await dify_service.chat(
            user_id=user_id,
            message=message,
            session_id=session_id,
            user_profile=user_profile
        )
        
        # Save interaction
        await database.save_interaction(interaction)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/test-dify")
async def test_dify_connection():
    """Test endpoint to verify Dify API connection"""
    try:
        # Test message
        test_profile = {
            "number_of_dependents": "2",
            "remittance_amount": "1000",
            "bank_account": "yes",
            "debt_information": "none",
            "remittance_information": "monthly"
        }
        
        response, _ = await dify_service.chat(
            user_id="test_user",
            message="Hello, can you help me with budgeting?",
            session_id="test_session",
            user_profile=test_profile
        )
        
        return {"status": "success", "message": "Dify API connection successful", "response": response}
    except Exception as e:
        return {"status": "error", "message": f"Dify API connection failed: {str(e)}"}

@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy"}

@app.get("/test/dynamodb")
async def test_dynamodb():
    """Test DynamoDB connection"""
    try:
        # Try to create a test table
        database.create_tables()
        return {"status": "success", "message": "DynamoDB connection successful"}
    except Exception as e:
        return {"status": "error", "message": f"DynamoDB error: {str(e)}"}

@app.get("/test/dify")
async def test_dify():
    """Test Dify integration"""
    try:
        # Test message
        test_profile = {
            "number_of_dependents": "2",
            "remittance_amount": "1000",
            "bank_account": "yes",
            "debt_information": "none",
            "remittance_information": "monthly"
        }
        
        response, _ = await dify_service.chat(
            user_id="test_user",
            message="Hello, can you help me with budgeting?",
            session_id="test_session",
            user_profile=test_profile
        )
        
        return {
            "status": "success", 
            "message": "Dify API connection successful",
            "response": response
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Dify API error: {str(e)}"
        }

# Add startup event to create tables
@app.on_event("startup")
async def startup_event():
    database.create_tables()

# Add this at the end of the file
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
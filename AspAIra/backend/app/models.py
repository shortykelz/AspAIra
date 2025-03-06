from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    is_active: bool = True

class ProfilePart1(BaseModel):
    country_of_origin: Literal["Filipino", "Kenyan", "Sri Lankan"]
    time_in_uae: Literal["Less than a year", "1-3 years", "3-5 years", "5-10 years", "10+ years"]
    job_title: Literal["Live In maid", "Live out maid", "Cook", "Nanny"]
    housing: Literal["Live In", "Live Out", "Temporary Housing"]
    education_level: Literal["None", "Primary school", "High school", "College"]
    number_of_dependents: Literal["None", "1", "2", "3", "More than 3"]

    class Config:
        populate_by_name = True

class ProfilePart2(BaseModel):
    bank_account: Literal["FAB", "Emirates NBD", "ADCB", "ADIB", "No Bank Account"]
    debt_information: Literal["Debt in Home Country", "Debt in UAE", "No Debt"]
    remittance_information: Literal["Send money with Bank Transfer", "Send money with Exchange House", 
                                  "Send money offline", "Don't Send any money"]
    remittance_amount: Literal["Less than 100 AED", "100-500 AED", "500-1000 AED", "1000-2000 AED", "More than 2000 AED"]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LatencyMetrics(BaseModel):
    total_response_time: float
    dify_api_latency: float
    context_prep_time: float
    database_operation_time: float

class AgentInteraction(BaseModel):
    interaction_id: str
    user_id: str
    timestamp_start: datetime
    timestamp_end: datetime
    session_id: str
    agent_version: str
    
    # Message content
    user_message: str
    agent_response: str
    
    # Learning context
    learning_path: Optional[str]
    current_topic: Optional[str]
    
    # User context
    financial_context: Dict
    
    # Interaction details
    is_question: bool = False
    is_topic_selection: bool = False
    is_quiz: bool = False
    quiz_data: Optional[Dict] = None
    
    # Engagement metrics
    response_length: int
    time_to_respond: float
    depth_requested: bool = False
    
    # Performance metrics
    latency_metrics: LatencyMetrics 
import time
from datetime import datetime
import os
from typing import Dict, Tuple
import uuid
import aiohttp
from models import LatencyMetrics, AgentInteraction
from config import AGENTS, ACTIVE_AGENT

class DifyService:
    def __init__(self):
        # Get agent configuration
        self.agent = AGENTS[ACTIVE_AGENT]
        self.api_key = self.agent["api_key"]
        self.api_endpoint = "http://dify-api:5001"  # Hardcoded for local Docker
        
        if not self.api_key:
            raise ValueError("API key not configured for the selected agent")
    
    def _prepare_context(self, user_profile: Dict) -> Dict:
        """Format user context for Dify API"""
        return {
            "dependents_count": user_profile.get("number_of_dependents"),
            "remittance_amount": user_profile.get("remittance_amount"),
            "bank_account": user_profile.get("bank_account"),
            "debt_status": user_profile.get("debt_information"),
            "remittance_status": user_profile.get("remittance_information")
        }
    
    async def _call_dify_api(self, message: str, context: Dict) -> str:
        """Call Dify API with timing"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": context,
            "query": message,
            "response_mode": "blocking",
            "conversation_id": None
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_endpoint}/chat-messages",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Dify API error: {error_text}")
                    
                    result = await response.json()
                    return result["answer"]
        except Exception as e:
            print(f"Error calling Dify API: {str(e)}")
            raise
    
    def _analyze_interaction(self, message: str, response: str) -> Dict:
        """Analyze interaction type and content"""
        return {
            'is_question': '?' in message,
            'is_topic_selection': any(str(i) in message for i in range(1, 4)),
            'is_quiz': 'quiz' in response.lower(),
            'response_length': len(response.split()),
            'learning_path': self._detect_learning_path(message),
            'current_topic': self._detect_topic(message, response)
        }
    
    def _detect_learning_path(self, message: str) -> str:
        """Detect which learning path the user is on"""
        if any(word in message.lower() for word in ['budget', 'spending', 'income']):
            return 'budgeting'
        elif any(word in message.lower() for word in ['save', 'saving', 'savings']):
            return 'saving'
        elif any(word in message.lower() for word in ['send', 'remit', 'transfer']):
            return 'remittance'
        return 'general'
    
    def _detect_topic(self, message: str, response: str) -> str:
        """Detect current topic of conversation"""
        combined_text = f"{message} {response}".lower()
        if 'budget' in combined_text:
            return 'budgeting'
        elif 'save' in combined_text:
            return 'saving'
        elif 'remit' in combined_text:
            return 'remittance'
        return 'general'
    
    async def chat(
        self, 
        user_id: str, 
        message: str, 
        session_id: str,
        user_profile: Dict
    ) -> Tuple[str, AgentInteraction]:
        # Start timing
        start_time = time.perf_counter()
        timestamp_start = datetime.now()
        
        # Context preparation timing
        context_start = time.perf_counter()
        context = self._prepare_context(user_profile)
        context_time = time.perf_counter() - context_start
        
        # API call timing
        api_start = time.perf_counter()
        response = await self._call_dify_api(message, context)
        api_time = time.perf_counter() - api_start
        
        # Analysis timing
        analysis_start = time.perf_counter()
        analysis = self._analyze_interaction(message, response)
        analysis_time = time.perf_counter() - analysis_start
        
        timestamp_end = datetime.now()
        total_time = time.perf_counter() - start_time
        
        # Create latency metrics
        latency_metrics = LatencyMetrics(
            total_response_time=total_time,
            dify_api_latency=api_time,
            context_prep_time=context_time,
            database_operation_time=analysis_time
        )
        
        # Create interaction record
        interaction = AgentInteraction(
            interaction_id=str(uuid.uuid4()),
            user_id=user_id,
            timestamp_start=timestamp_start,
            timestamp_end=timestamp_end,
            session_id=session_id,
            agent_version="v1",
            user_message=message,
            agent_response=response,
            financial_context=context,
            latency_metrics=latency_metrics,
            **analysis
        )
        
        return response, interaction 
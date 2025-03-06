"""
Configuration for Dify agents and API settings.
"""

AGENTS = {
    "financial_advisor": {
        "name": "Financial Advisor",
        "api_key": "dify_local",  # This will be overridden by the API key in docker-compose
        "description": "Financial planning and advice agent"
    }
}

ACTIVE_AGENT = "financial_advisor"  # Default agent 
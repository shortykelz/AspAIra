import boto3
import os
from botocore.exceptions import ClientError
from botocore.config import Config
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from models import AgentInteraction, LatencyMetrics

# JWT Configuration
SECRET_KEY = "development_secret_key"  # Change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv('DYNAMODB_ENDPOINT', 'http://localhost:8000'),
    region_name=os.getenv('AWS_REGION', 'local'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'dummy'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'dummy')
)

TABLE_NAME = 'AspAIra_Users'

def _create_table_if_not_exists():
    try:
        # Check if table exists
        dynamodb.Table(TABLE_NAME).table_status
        print(f"Table {TABLE_NAME} exists")
    except:
        print(f"Creating table {TABLE_NAME}")
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        print(f"Table {TABLE_NAME} created successfully")

def get_table():
    return dynamodb.Table(TABLE_NAME)

# Create table on module import
_create_table_if_not_exists()

def create_user(username: str, password: str):
    print(f"Attempting to create user: {username}")  # Debug log
    hashed_password = pwd_context.hash(password)
    try:
        table = dynamodb.Table(TABLE_NAME)
        print(f"Got table reference: {TABLE_NAME}")  # Debug log
        
        # First check if user exists
        existing_user = table.get_item(Key={'username': username}).get('Item')
        if existing_user:
            print(f"User {username} already exists")  # Debug log
            return False
            
        # Create new user
        table.put_item(
            Item={
                'username': username,
                'hashed_password': hashed_password,
                'is_active': True,
                'profile_completed': False,
                'created_at': datetime.utcnow().isoformat()
            }
        )
        print(f"Successfully created user: {username}")  # Debug log
        return True
    except ClientError as e:
        print(f"Error creating user: {str(e)}")  # Debug log
        raise
    except Exception as e:
        print(f"Unexpected error creating user: {str(e)}")  # Debug log
        raise

def get_user(username: str):
    try:
        table = dynamodb.Table(TABLE_NAME)
        response = table.get_item(Key={'username': username})
        return response.get('Item')
    except ClientError:
        return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not pwd_context.verify(password, user['hashed_password']):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return get_user(username)
    except JWTError:
        return None

def update_profile_part1(username: str, profile_data: dict):
    try:
        print(f"Attempting to update profile1 for user {username}")
        print(f"Profile data to save: {profile_data}")
        table = dynamodb.Table(TABLE_NAME)
        
        # First check if user exists
        existing_user = table.get_item(Key={'username': username})
        print(f"Existing user data: {existing_user}")
        
        response = table.update_item(
            Key={
                'username': username
            },
            UpdateExpression='SET profile1 = :profile_data, profile1_complete = :complete',
            ExpressionAttributeValues={
                ':profile_data': profile_data,
                ':complete': True
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"DynamoDB response: {response}")
        return True
    except Exception as e:
        print(f"Error updating profile1 for user {username}")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        print(f"Error details: {e.__dict__}")
        return False

def update_profile_part2(username: str, profile_data: dict):
    try:
        table = dynamodb.Table(TABLE_NAME)
        response = table.update_item(
            Key={
                'username': username
            },
            UpdateExpression='SET profile2 = :profile_data, profile2_complete = :complete',
            ExpressionAttributeValues={
                ':profile_data': profile_data,
                ':complete': True
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Updated profile2 for user {username}: {response}")
        return True
    except Exception as e:
        print(f"Error updating profile2 for user {username}: {str(e)}")
        return False

def get_profile_status(username: str):
    try:
        table = dynamodb.Table(TABLE_NAME)
        response = table.get_item(
            Key={
                'username': username
            },
            ProjectionExpression='profile1_complete, profile2_complete'
        )
        if 'Item' in response:
            return {
                'profile1_complete': response['Item'].get('profile1_complete', False),
                'profile2_complete': response['Item'].get('profile2_complete', False)
            }
        return {
            'profile1_complete': False,
            'profile2_complete': False
        }
    except Exception as e:
        print(f"Error getting profile status for user {username}: {str(e)}")
        return {
            'profile1_complete': False,
            'profile2_complete': False
        }

def scan_all_users():
    try:
        table = dynamodb.Table(TABLE_NAME)
        response = table.scan()
        return response.get('Items', [])
    except Exception as e:
        print(f"Error scanning users: {str(e)}")
        return []

def create_tables():
    """Create required DynamoDB tables if they don't exist"""
    try:
        table = dynamodb.create_table(
            TableName='agent_interactions',
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp_start', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp_start', 'AttributeType': 'S'},
                {'AttributeName': 'session_id', 'AttributeType': 'S'},
                {'AttributeName': 'agent_version', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'by_session',
                    'KeySchema': [
                        {'AttributeName': 'session_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'timestamp_start', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
                {
                    'IndexName': 'by_agent',
                    'KeySchema': [
                        {'AttributeName': 'agent_version', 'KeyType': 'HASH'},
                        {'AttributeName': 'timestamp_start', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Table created successfully:", table.table_status)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Table already exists")
        else:
            raise e

async def save_interaction(interaction: AgentInteraction):
    """Save chat interaction to DynamoDB"""
    table = dynamodb.Table('agent_interactions')
    
    # Convert datetime objects to strings
    interaction_dict = interaction.dict()
    interaction_dict['timestamp_start'] = interaction.timestamp_start.isoformat()
    interaction_dict['timestamp_end'] = interaction.timestamp_end.isoformat()
    
    try:
        response = table.put_item(Item=interaction_dict)
        return response
    except ClientError as e:
        print(f"Error saving interaction: {e.response['Error']['Message']}")
        raise e

async def get_user_interactions(user_id: str, limit: int = 10):
    """Retrieve recent interactions for a user"""
    table = dynamodb.Table('agent_interactions')
    
    try:
        response = table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': user_id},
            Limit=limit,
            ScanIndexForward=False  # Get most recent first
        )
        return response['Items']
    except ClientError as e:
        print(f"Error retrieving interactions: {e.response['Error']['Message']}")
        raise e

# End of file - removing reset_database function 
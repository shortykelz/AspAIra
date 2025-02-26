import boto3
from botocore.exceptions import ClientError

class DynamoDBManager:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = 'AispAIra_Users'
        self.table = self.dynamodb.Table(self.table_name)

    def create_user(self, user_data):
        try:
            response = self.table.put_item(Item=user_data)
            return True
        except ClientError as e:
            print(f"Error creating user: {e.response['Error']['Message']}")
            return False

    def get_user(self, email):
        try:
            response = self.table.get_item(Key={'email': email})
            return response.get('Item')
        except ClientError as e:
            print(f"Error retrieving user: {e.response['Error']['Message']}")
            return None

    def update_user(self, email, update_data):
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}
        
        for key, value in update_data.items():
            update_expression += f"#{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value
            expression_attribute_names[f"#{key}"] = key
        
        update_expression = update_expression.rstrip(", ")
        
        try:
            response = self.table.update_item(
                Key={'email': email},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names,
                ReturnValues="UPDATED_NEW"
            )
            return True
        except ClientError as e:
            print(f"Error updating user: {e.response['Error']['Message']}")
            return False

db = DynamoDBManager() 
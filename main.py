import os

import boto3
from botocore.exceptions import ClientError

os.environ['AWS_ACCESS_KEY_ID'] = 'DUMMY_VALUE'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'DUMMY_VALUE'
os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-1'

def get_user(name: str) -> dict:
    client = boto3.client('cognito-idp')

    try:
        user = client.admin_get_user(
            UserPoolId='DUMMY_USER_POOL_ID',
            Username=name,
        )
    except ClientError as error:
        if error.response['Error']['Code'] == 'UserNotFoundException':
            return None
        raise

    return user['UserAttributes']

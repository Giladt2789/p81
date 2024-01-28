import boto3
import json
import os

region = os.getenv('INPUT_REGION')
bucket_name = os.getenv('INPUT_STATE_FILES_BUCKET')
profile_name = os.getenv('INPUT_PROFILE_NAME')
table_name = os.getenv('INPUT_STATEFILE_LOCK_TABLE')
account_number = os.getenv('INPUT_ACCOUNT_NUMBER')
iam_user_name = os.getenv('INPUT_IAM_USER_NAME')
# General attributes for the S3 bucket and the dynamodb table (for the state file)
aws_session = boto3.session.Session(region_name=region, profile_name=profile_name)
s3_client = aws_session.client('s3')
dynamodb_client = aws_session.client('dynamodb')
try:
    s3_client.head_bucket(Bucket=bucket_name)
except Exception as s3_ex:
    bucket_creation_response = s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': region
        }
    )
    bucket_versioning_response = s3_client.put_bucket_versioning(
       Bucket=bucket_name,
       VersioningConfiguration={'Status': 'Enabled'}
    )

    bucket_encryption_response = s3_client.put_bucket_encryption(
        Bucket=bucket_name,
        ServerSideEncryptionConfiguration={
            'Rules': [{
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }]
        }
    )

    bucket_policy_response = s3_client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:ListBucket",
                    "Resource": f"arn:aws:s3:::{bucket_name}",
                    "Principal": { f"AWS": f"arn:aws:iam::{account_number}:user/{iam_user_name}" },
                },
                {
                    "Effect": "Allow",
                    "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
                    "Principal": { f"AWS": f"arn:aws:iam::{account_number}:user/{iam_user_name}" },
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        })
    )
print("Bucket exists or was created")
try:
    dynamodb_client.describe_table(TableName=table_name)
except Exception as ddb_ex:
    dynamodb_table_creation_response = dynamodb_client.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {
                'AttributeName': 'LockID',
                'AttributeType': 'S'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'LockID',
                'KeyType': 'HASH'
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )
print("DynamoDB table exists or was created")


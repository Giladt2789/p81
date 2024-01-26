import boto3
import os

region = os.environ['REGION']
bucket_name = os.environ['BUCKET']
profile_name = os.environ['PROFILE_NAME']
table_name = os.environ['TABLE_NAME']

# General attributes for the S3 bucket and the dynamodb table (for the state file)
aws_session = boto3.session.Session(region_name=region, profile_name=profile_name)
s3_client = aws_session.client('s3')
dynamodb_client = aws_session.client('dynamodb')
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

s3_encryption_response = s3_client.put_bucket_encryption(
    Bucket=bucket_name,
    ServerSideEncryptionConfiguration={
        'Rules': [{
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'AES256'
                }
            }]
    }
)

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
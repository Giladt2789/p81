import boto3
import sys

region = sys.argv[1]
bucket_name = sys.argv[2]
profile_name = sys.argv[3]
table_name = sys.argv[4]

aws_session = boto3.session.Session(region_name=region, profile_name=profile_name)
s3_client = aws_session.client('s3')
dynamodb_client = aws_session.client('dynamodb')
# Get bucket versioning status
versioning = s3_client.get_bucket_versioning(Bucket='testing-remove-bucket-gilad')['Status']

# Empty bucket versions
if versioning == 'Enabled':
    versions = s3_client.list_object_versions(Bucket='testing-remove-bucket-gilad')['Versions']
    while versions:
        # Delete bucket versions
        delete_keys = [{'Key': v['Key'], 'VersionId': v['VersionId']} for v in versions]
        s3_client.delete_objects(Bucket='testing-remove-bucket-gilad', Delete={'Objects': delete_keys})
        versions = s3_client.list_object_versions(Bucket='testing-remove-bucket-gilad')['Versions']

# Empty bucket
objects = [{'Key': obj['Key']} for obj in s3_client.list_objects(Bucket='testing-remove-bucket-gilad')['Contents']]
s3_client.delete_objects(Bucket='testing-remove-bucket-gilad', Delete={'Objects': objects})

# Delete empty bucket
s3_client.delete_bucket(Bucket='testing-remove-bucket-gilad')

# Delete table
dynamodb_client.delete_table(TableName='p81-gilad-statefile-locks-table')

# Wait until the table is deleted
waiter = dynamodb_client.get_waiter('table_not_exists')
waiter.wait(TableName='p81-gilad-statefile-locks-table')
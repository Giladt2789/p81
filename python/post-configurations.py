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
versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)['Status']

# Empty bucket versions
if versioning == 'Enabled':
    versions = s3_client.list_object_versions(Bucket=bucket_name)
    if 'Versions' in versions:
        while versions:
            # Delete bucket versions
            delete_keys = []
            for v in versions['Versions']:
                dict = {}
                dict['Key'] = v['Key']
                dict['VersionId'] = v['VersionId']
                delete_keys.append(dict)
            s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': delete_keys})

# Empty bucket
objects = []
list_objects = s3_client.list_objects_v2(Bucket=bucket_name)
if 'Contents' in list_objects:
    for obj in list_objects['Contents']:
        dict = {}
        dict['Key'] = obj['Key']
        objects.append(dict)
    s3_client.delete_objects(Bucket=bucket_name,
                            Delete={'Objects': objects})

# Delete empty bucket
s3_client.delete_bucket(Bucket=bucket_name)

# Delete table
delete_table = dynamodb_client.delete_table(TableName=table_name)

# Wait until the table is deleted
waiter = dynamodb_client.get_waiter('table_not_exists')
waiter.wait(TableName=table_name)
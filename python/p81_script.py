import json
import boto3
import requests
import argparse


class Assignment:
    def __init__(self, bucket_name, region):
        self.url = "https://dummyjson.com/products"
        self.aws_profile = "default"
        self.bucket_name = bucket_name
        self.region = region
        self.file_name = "final_catalog.json"
        self.aws_session = boto3.session.Session(region_name=self.region, profile_name=self.aws_profile)
        self.client = self.aws_session.client('s3')

    def save_filtered_products_by_price(self):
        raw_data = requests.get(self.url).json()
        new_product_list = []
        for product in raw_data['products']:
            if product['price'] >= 100:
                new_product_list.append(product)
        with open(self.file_name, 'w') as file:
            json.dump(new_product_list, file)

    def upload_filtered_products_to_s3(self):
        with open(self.file_name, 'r') as json_file:
            read_data = json.load(json_file)
        bucket_upload = self.client.put_object(
            Bucket=self.bucket_name,
            Body=json.dumps(read_data),
            Key=self.file_name,
            ContentType='application/json',
            ContentDisposition='attachment; filename='+self.file_name
            )

    def download_filtered_json(self):
        with open('../Terraform/modules/cloudfront/cloudfront_domain.txt' , 'r') as file:
            download_url = "https://" + file.read()
            r = requests.get(download_url, allow_redirects=True)
        with open(self.file_name, 'wb') as file:
            file.write(r.content)
        try:
            json_data = json.load(open(self.file_name))
            print("Valid JSON format")
        except ValueError as ex:
            print("Invalid JSON format")

    def empty_bucket(self):
        # Delete bucket versions
        versions = self.client.list_object_versions(Bucket=self.bucket_name)
        if 'Versions' in versions:
            while versions:
            # Delete bucket versions
                delete_keys = []
                for v in versions['Versions']:
                    dict = {}
                    dict['Key'] = v['Key']
                    dict['VersionId'] = v['VersionId']
                    delete_keys.append(dict)
                self.client.delete_objects(Bucket=self.bucket_name, Delete={'Objects': delete_keys})



parser = argparse.ArgumentParser(description='Operations on the storage bucket ')
parser.add_argument('--bucket', type=str, required=True, help='Name of bucket created in terraform')
parser.add_argument('--region', type=str, required=True, help='AWS region name')
parser.add_argument('--destroy', type=str, required=False, help='Destroy the bucket before complete clean up')
args = parser.parse_args()

obj = Assignment(bucket_name=args.bucket, region=args.region)
if not args.destroy:
    obj.save_filtered_products_by_price()
    obj.upload_filtered_products_to_s3()
    obj.download_filtered_json()
else:
    obj.empty_bucket()
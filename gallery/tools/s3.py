import logging
import boto3
import botocore
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region=None):
	try:
		if region is None:
			s3_client = boto3.client('s3')
			s3_client.create_bucket(Bucket=bucket_name)
		else:
			s3_client = boto3.client('s3', region_name=region)
			location = {'LocationConstraint': region}
			s3_client.create_bucket(Bucket=bucket_name,
									CreateBucketConfiguration=location)
	except ClientError as e:
		logging.error(e)
		return False
	return true

def put_object(bucket_name, key, value):
	try:
		s3_client = boto3.client('s3')
		s3_client.put_object(Bucket=bucket_name, Key=key, Body=value)
	except ClientError as e:
		logging.error(e)
		return False
	return True
	
def get_object(bucket_name, key):
	try:
		s3_resource = boto3.resource('s3')
		obj = s3_resource.Object(bucket_name, key)
		body = obj.get()['Body'].read()
	except ClientError as e:
		logging.error(e)
		return None
	return body
	
def main():
	#create_bucket('edu.au.cc.m6.python-image-gallery','us-west-2')
	put_object('edu.au.cc.m6.python-image-gallery', 'HELLO', 'WORLD')
	print (get_object('edu.au.cc.m6.python-image-gallery', 'HELLO'))
	print (get_object('edu.au.cc.m6.python-image-gallery', 'HELLO')['Body'].read())
if __name__ == '__main__':
	main()


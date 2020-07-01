import logging
import boto3
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
		s3_client = boto3.client('s3')
		result = s3_client.get_object(Bucket=bucket_name, Key=key)
	except ClientError as e:
		logging.error(e)
		return None
	return result

def upload_file(file_name, bucket):
	"""
	Function to upload a file to an S3 bucket
	"""
	try:
		object_name = file_name
		s3_client = boto3.client('s3')
		response = s3_client.upload_file(file_name, bucket, object_name)
	except ClientError as e:
			logging.error(e)
			return None
	return response
	
def download_file(file_name, bucket):
	"""
	Function to download a given file from an S3 bucket
	"""
	try:
		s3 = boto3.resource('s3')
		output = f"/gallery/downloads/{file_name}" # local dir location to store file if we want
		s3.Bucket(bucket).download_file(file_name, output)
		
	except ClientError as e:
			logging.error(e)
			return None
	return output
	
def list_files(bucket):
	"""
	Function to list files in a given s3 bucket
	"""
	try:
		s3 = boto3.client('s3')
		contents = []
		for item in s3.list_object(Bucket=bucket)['Contents']:
			contents.append(item)
	except ClientError as e:
			logging.error(e)
			return None
	return contents
		
		
	
def main():
	#create_bucket('edu.au.cc.m6.python-image-gallery','us-west-2')
	put_object('edu.au.cc.m6.python-image-gallery', 'HELLO', 'WORLD')
	print (get_object('edu.au.cc.m6.python-image-gallery', 'HELLO'))
	print (get_object('edu.au.cc.m6.python-image-gallery', 'HELLO')['Body'].read())
if __name__ == '__main__':
	main()


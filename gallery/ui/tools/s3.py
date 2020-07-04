import logging
import boto3
import botocore
from botocore.exceptions import ClientError

#upload image functionality
def put_object(bucket_name, key, value):
	try:
		s3_client = boto3.client('s3')
		s3_client.put_object(Bucket=bucket_name, Key=key, Body=value)
	except ClientError as e:
		logging.error(e)
		return False
	return True

#showing objects on webpage
def get_object(bucket_name, key):
	try:
		s3_resource = boto3.resource('s3')
		obj = s3_resource.Object(bucket_name, key)
	except ClientError as e:
		logging.error(e)
		return None
	return body

#delete functionality
def delete_object(bucket_name, key):
	try:
		s3_client = boto3.client('s3')
		res = s3_client.delete_object(Bucket=bucket_name, Key=key)
	except ClientError as e:
		logging.error(e)
		return None
	return res

if __name__ == '__main__':
	main()

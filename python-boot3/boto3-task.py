import boto3

file = open("token", "r")

access_key = file.readline().strip("\n")
secret_key = file.readline().strip("\n")
region = "eu-west-1"
bucket = "eng84josebucket"

# S3 authentication setup - with aws configure
s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)

# Create S3 bucket using python-boto3
def create_bucket():
	s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': region})
	print("The bucket with the name " + bucket + " was created.")

# Upload data/file to S3 bucket using python-boto3
def upload_file(file_name):
	s3.upload_file(Filename=file_name, Bucket=bucket, Key=file_name)
	print("The file with the name " + file_name + " was uploaded in the bucket.")

# Retrieve content/file from S3 using python-boto3
def retrieve_file(file_name):
	s3.download_file(Bucket=bucket, Key=file_name, Filename=file_name)
	print("The file with the name " + file_name + " was downloaded from the bucket to your localhost.")

# Delete Content from S3 using python-boto3
def delete_content(file_name):
	s3.delete_object(Bucket=bucket, Key=file_name)
	print("The file with the name " + file_name + " was deleted in the bucket.")

# Delete the bucket using python-boto3.**
def delete_bucket():
	s3.delete_bucket(Bucket=bucket)
	print("The bucket with the name " + bucket + " was deleted.")

# Print the name of all buckets in S3 sever
def print_name_buckets():
	print("Let's print the name of all buckets:")
	for bucket_dict in s3.list_buckets().get('Buckets'):
		print(bucket_dict['Name'])    	

if __name__ == '__main__':
	#create_bucket()
	#upload_file("testing.md")
	#retrieve_file("testing.md")
	#delete_content("testing.md")
	#delete_bucket()
	#print_name_buckets()
	pass

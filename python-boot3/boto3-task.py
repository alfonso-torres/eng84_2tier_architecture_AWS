import boto3

file = open("token", "r")

access_key = file.readline().strip("\n")
secret_key = file.readline().strip("\n")
region = "eu-west-1"
bucket = "eng84josebucket"

s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)

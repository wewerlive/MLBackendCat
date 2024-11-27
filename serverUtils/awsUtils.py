import boto3

from dotenv import load_dotenv
import os

load_dotenv()

# Create an S3 client
access_key = os.getenv("AWS_ACCESS_KEY")
secret_key = os.getenv("AWS_SECRET_KEY")

print("Loaded S3")

s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

def uploadImage(image, bucket_name,filename):
    # filename = image.filename
    print()
    print(filename)
    s3.upload_fileobj(image, bucket_name,filename)
    print("Uploaded"+filename)
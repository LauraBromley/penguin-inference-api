import boto3
import os
from io import BytesIO
from inference.model_inference import init_model

s3 = boto3.client('s3')

# AWS Lambda Environment variables
BUCKET_NAME = os.environ['BUCKET_NAME']
OBJECT_NAME = os.environ['OBJECT_NAME']

# Download file from S3 to tmp folder
def get_model_file():
    print("downloading file from s3")
    print("BUCKET_NAME", BUCKET_NAME)
    print("OBJECT_NAME", OBJECT_NAME)
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_NAME)
    bytestream = BytesIO(obj['Body'].read())
    return bytestream

# Load model from tmp folder
def setup_inf_model():
    bytestream = get_model_file()
    return init_model(bytestream)

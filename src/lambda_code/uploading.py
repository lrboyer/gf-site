import json
import boto3
from botocore.exceptions import ClientError
import base64

s3 = boto3.client('s3')
bucket_name = 'gf-site'

def generate_presigned_url(file_name, group_name):
    try:
        # Combine group name and file name for the S3 key
        key = f"{group_name}/{file_name}"

        # Generate a presigned URL for the S3 object
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': key,
                'ContentType': 'image/*',
            },
            ExpiresIn=60,  # Presigned URL expiration time in seconds
        )
        return presigned_url

    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        raise

def lambda_handler(event, context):
    try:
        query_parameters = event.get('queryStringParameters', {})
        file_name = query_parameters.get('fileName', "")
        group_name = query_parameters.get('groupName', "")

        # Fetch the presigned URL
        presigned_url = generate_presigned_url(file_name, group_name)

        return {
            'statusCode': 200,
            'body': json.dumps({'presignedUrl': presigned_url}),
        }

    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error: ' + e}),
        }
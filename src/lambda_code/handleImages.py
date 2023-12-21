import boto3
import json
import time

table_name = 'gf-img-url'
bucket_name = 'gf-site'

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
dynamo_table = dynamodb.Table(table_name)

def get_unique_folders(bucket_name):
    try:
        folders = set()
        response = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter='/')
        print(response)
        for prefix in response.get('CommonPrefixes', []):
            folder_name = prefix.get('Prefix').rstrip('/')
            folders.add(folder_name)
    
        return list(folders)
    except Exception as e:
        print(f"Error getting folders: {e}")
        return None


def generate_presigned_url(bucket, key):
    try:
        presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=600)
        return presigned_url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None
        
def write_to_dynamodb(file_name, presigned_url):
    current_time = int(time.time())
    expire_ttl = current_time + 6000  # TTL of 100 minutes (6000 seconds)

    # Add TTL attribute to the item to be stored in DynamoDB
    item_to_dynamo = {
        'name': file_name,
        'url': presigned_url,
        'expire': expire_ttl
    }

    # Write the item with TTL to DynamoDB table
    dynamo_table.put_item(Item=item_to_dynamo, ConditionExpression='attribute_not_exists(file_name) OR #expire > :now',
                          ExpressionAttributeNames={'#expire': 'expire'},
                          ExpressionAttributeValues={':now': current_time})


# Generate presigned URLs for each image in the folder
def getGroupUrls(images):
    presigned_urls = []
    
    for image in images:
        key = image['Key']
        
        # Check if the file name exists in DynamoDB and not expired
        file_name = key.split('/')[-1]  # Extracting file name from S3 key
        response = dynamo_table.get_item(Key={'name': file_name})
        
        if 'Item' in response:
            existing_url = response['Item']['url']
            existing_expire = response['Item']['expire']
            current_time = int(time.time())
            
            if existing_expire > current_time: # URL exists and not expired, use the existing URL
                presigned_url = existing_url
            else: # URL expired, generate a new presigned URL
                presigned_url = generate_presigned_url(bucket_name, key)
                write_to_dynamodb(file_name, presigned_url)
                
        else: # No URL found for the file name, generate a new presigned URL
            presigned_url = generate_presigned_url(bucket_name, key)
            write_to_dynamodb(file_name, presigned_url)
        
        presigned_urls.append({'file_name': file_name, 'url': presigned_url})
        
    return presigned_urls

def lambda_handler(event, context):
    try:
        image_groups = get_unique_folders(bucket_name)
        imagesByGroup = []
        
        for group in image_groups:
            folder_path = group
            
            # Fetch the list of objects (images) in the folder
            response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)
            objects = response.get('Contents', [])        
            images = [obj for obj in objects if not obj['Key'].endswith('/')]  # Exclude objects that end with '/'
            print("IMAGES: ")
            print(images)
            urls = getGroupUrls(images)
            print("URLS: ")
            print(urls)
            newGroup = {
                "group": folder_path,
                "images": urls
            }
            
            imagesByGroup.append(newGroup)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(imagesByGroup)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
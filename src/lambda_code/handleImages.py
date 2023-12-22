import boto3
import json
import time

table_name = 'gf-img-url'
bucket_name = 'gf-site'

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
dynamo_table = dynamodb.Table(table_name)

table_groups = 'gf-site-groups'
dynamo_table_groups = dynamodb.Table(table_groups)


def insert_group_name(groupName):
    item = {
        "groupName": groupName,
        "order": 100
    }
    dynamo_table_groups.put_item(Item=item)


def get_folders_from_dynamo():
    dynamodb_response = dynamo_table_groups.scan(TableName=table_groups)
    groups = dynamodb_response.get('Items', [])

    return groups


def get_unique_folders_from_s3():
    try:
        folders = set()
        response = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter='/')

        for prefix in response.get('CommonPrefixes', []):
            folder_name = prefix.get('Prefix').rstrip('/')
            folders.add(folder_name)

        return list(folders)
    except Exception as e:
        print(f"Error getting folders: {e}")
        return None


def getFolders():
    s3Folders = get_unique_folders_from_s3()
    dynamoFolders = get_folders_from_dynamo()

    if len(s3Folders) != len(dynamoFolders):
        for group in s3Folders:
            if group not in [folder['groupName'] for folder in dynamoFolders]:
                insert_group_name(group)
                dynamoFolders.append({"groupName": group, "order": 100})

    sorted_folders = sorted(
        dynamoFolders, key=lambda x: x['order'], reverse=True)

    folders = [item['groupName'] for item in sorted_folders]

    return folders


def generate_presigned_url(bucket, key):
    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=43200)
        return presigned_url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None


def write_to_dynamodb(file_name, presigned_url):
    current_time = int(time.time())
    expire_ttl = current_time + 43200  # TTL of 12 hours

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

            if existing_expire > current_time:  # URL exists and not expired, use the existing URL
                presigned_url = existing_url
            else:  # URL expired, generate a new presigned URL
                presigned_url = generate_presigned_url(bucket_name, key)
                write_to_dynamodb(file_name, presigned_url)

        else:  # No URL found for the file name, generate a new presigned URL
            presigned_url = generate_presigned_url(bucket_name, key)
            write_to_dynamodb(file_name, presigned_url)

        presigned_urls.append({'file_name': file_name, 'url': presigned_url})

    return presigned_urls


def getGroupImages(groupName):
    try:
        folder_path = groupName

        # Fetch the list of objects (images) in the folder
        response = s3_client.list_objects_v2(
            Bucket=bucket_name, Prefix=folder_path)
        objects = response.get('Contents', [])
        # Exclude objects that end with '/'
        images = [obj for obj in objects if not obj['Key'].endswith('/')]

        urls = getGroupUrls(images)

        groupImages = {
            "group": folder_path,
            "images": urls
        }

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(groupImages)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def lambda_handler(event, context):
    pathParam = event.get("pathParameters", {})

    if "groupName" in pathParam:
        groupName = pathParam["groupName"]

        groupImages = getGroupImages(groupName)
        response = groupImages
    else:
        groups = getFolders()
        response = groups

    return response

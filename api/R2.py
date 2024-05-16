import io
import boto3
import botocore

s3 = boto3.client(
    service_name ="s3",
    endpoint_url = 'https://73ecf9da48c64331392d13cc2c07b941.r2.cloudflarestorage.com',
    aws_access_key_id = 'ea2a49bc2774d825e412aa84916213cb',
    aws_secret_access_key = '84eb75887e0fc411496e55b273cc1beab7e918d911ee66aaef79974e16997075',
    region_name="apac", # Must be one of: wnam, enam, weur, eeur, apac, auto
)
Bucket_Name ="test"
# Get object information
# Upload/Update single file
#s3.upload_fileobj(io.BytesIO(file_content), <R2_BUCKET_NAME>, <FILE_KEY_NAME>)
localFilePath='./123456.jpg'
try:
    s3.upload_file(localFilePath, Bucket_Name, '12345600000.jpg')
    print()
except botocore.exceptions.ClientError as e:
    print(e)

# Delete object
#s3.delete_object(Bucket=<R2_BUCKET_NAME>, Key=<FILE_KEY_NAME>)
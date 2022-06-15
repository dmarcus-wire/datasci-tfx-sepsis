import boto3
import os

def downloadDirectoryFromS3(bucketName: str, remoteDirectoryName: str) -> None:
    """
    Download a directory from S3 storage by iterating through
    the bucket objects associated with a remote folder. The
    remote directory structure is preserved.
    Required environment variables that need to be set:
    S3_REGION,
    S3_ACCESS_KEY_ID,
    S3_SECRET_ACCESS_KEY
    Args:
    bucketName: str - The name of the S3 bucket.
    remoteDirectoryName: str - The name of the remote directory (folder) to download.
    """
    s3_resource = boto3.resource(
        's3',
        region_name=os.environ['S3_REGION'],
        aws_access_key_id=os.environ['S3_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['S3_SECRET_ACCESS_KEY']
        )
    bucket = s3_resource.Bucket(bucketName)
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key) # save to same path

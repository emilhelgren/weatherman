import os
import boto3

from dotenv import load_dotenv

load_dotenv()

def load_s3():
    """
    Load the S3 resource.
    """
    try:
        s3 = boto3.resource(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        return s3
    except Exception as e:
        print(f"Error loading S3 resource: {e}")
        return None


def list_files_in_bucket(bucket_name):
    """
    List all files in an S3 bucket.

    Args:
        bucket_name: Name of the S3 bucket.
    """
    try:
        s3 = load_s3()
        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.all():
            print(obj.key)
        return True
    except Exception as e:
        print(f"Error listing files in {bucket_name}: {e}")
        return None


def upload_file_to_bucket(bucket_name, file_name, file_contents):
    """
    Upload a file to an S3 bucket.

    Args:
        bucket_name: Name of the S3 bucket.
        file_name: Name of the file to upload.
        file_contents: Contents of the file to upload.
    """
    try: 
        s3 = load_s3()
        s3.Object(bucket_name, file_name).put(Body=file_contents)
        print(f"File {file_name} uploaded to {bucket_name}")
        return True
    except Exception as e:
        print(f"Error uploading file to {bucket_name}: {e}")
        return False


def get_file_from_bucket(bucket_name, file_name):
    """
    Get a file from an S3 bucket.

    Args:
        bucket_name: Name of the S3 bucket.
        file_name: Name of the file to get.

    Returns:
        str: The contents of the file.
    """
    try:
        s3 = load_s3()
        obj = s3.Object(bucket_name, file_name)
        return obj.get()['Body'].read().decode('utf-8')
    except Exception as e:
        print(f"Error getting file from {bucket_name}: {e}")
        return None


def delete_file_from_bucket(bucket_name, file_name):
    """
    Delete a file from an S3 bucket.

    Args:
        bucket_name: Name of the S3 bucket.
        file_name: Name of the file to delete.
    """
    try:
        s3 = load_s3()
        s3.Object(bucket_name, file_name).delete()
        print(f"File {file_name} deleted from {bucket_name}")
        return True
    except Exception as e:
        print(f"Error deleting file from {bucket_name}: {e}")
        return False
    



# upload_file_to_bucket()
# list_files_in_bucket("weatherman-bucket")
# print(get_file_from_bucket("weatherman-bucket", "test.json"))

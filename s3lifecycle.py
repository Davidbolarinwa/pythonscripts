import boto3

# Set up the AWS S3 client
s3 = boto3.client('s3')

# Define the S3 bucket and prefix (folder) to manage
bucket_name = 'your-bucket-name'
prefix = 'data/'

# Define the transition and deletion policies
transition_to_infrequent_access_after_days = 30
delete_after_days = 90

def manage_data_lifecycle():
    # List objects in the specified bucket and prefix
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    for obj in objects.get('Contents', []):
        key = obj['Key']
        last_modified = obj['LastModified']
        current_date = boto3.client('s3').get_bucket_lifecycle_configuration(Bucket=bucket_name)

        # Calculate the number of days since the object was last modified
        days_since_last_modified = (current_date - last_modified).days

        if days_since_last_modified >= delete_after_days:
            print(f"Deleting object: s3://{bucket_name}/{key}")
            s3.delete_object(Bucket=bucket_name, Key=key)
        elif days_since_last_modified >= transition_to_infrequent_access_after_days:
            print(f"Transitioning object to Infrequent Access: s3://{bucket_name}/{key}")
            s3.copy_object(
                CopySource={'Bucket': bucket_name, 'Key': key},
                Bucket=bucket_name,
                Key=key,
                StorageClass='STANDARD_IA'  # Transition to Infrequent Access storage class
            )

if __name__ == '__main__':
    manage_data_lifecycle()

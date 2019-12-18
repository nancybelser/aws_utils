import boto3
import smtplib
import email.message

session = boto3.Session(
        #pec staging
        region_name='us-west-1',
        profile_name='nbpecstaging'

        #aws dev
        #region_name='us-east-2',
        #profile_name='nbelser'
        )

# Create an S3 client
s3 = session.client('s3')

# Call S3 to list current buckets
response = s3.list_buckets()

noTags = []
noTagList = ""
# Get a list of all bucket names from the response
#print("Bucket List")
for bucket in response['Buckets']:
    print(bucket)
    bucketName = bucket["Name"]
    try:
        bucket_tagging = s3.get_bucket_tagging(Bucket=(bucket['Name']))
        print(bucket_tagging)
    except:
       print("No tags set on bucket: ", bucketName)
       noTagList += bucketName + "\n"
       noTags.append(bucket['Name'])

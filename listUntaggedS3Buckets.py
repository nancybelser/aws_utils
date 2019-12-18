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
    #print(bucket)
    bucketName = bucket["Name"]

    try:
        bucket_tagging = s3.get_bucket_tagging(Bucket=(bucket['Name']))
        #print(bucket_tagging)
    except:
       print("No tags set on bucket: ", bucketName)
       noTagList += bucketName + "\n"
       noTags.append(bucket['Name'])
'''
    try:
        for key in s3.list_objects_v2(Bucket=bucketName)['Contents']:
            print(key['Key'])
    except:
        print("Empty bucket")
'''
sender = "nancy.belser@genesys.com"
receiver = "nancy.belser@genesys.com"
msg = email.message.Message()
msg['Subject'] = "S3 Buckets without Tags in PEC Staging (us-west-1)"
msg['From'] = sender
msg['To'] = receiver
msg.add_header('Content-Type','text/plain')
msg.set_payload(noTagList)

try:
   smtpObj = smtplib.SMTP("exchange.genesyslab.com", 25)
   smtpObj.sendmail(msg['From'], msg['To'], msg.as_string())
   #smtpObj.sendmail(sender, receiver, content)
   print("Successfully sent email")
except Exception:
   print("Error: unable to send email")

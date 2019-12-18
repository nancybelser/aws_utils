import boto3
from pprint import pprint


DATE_STRING = "%Y-%m-%d"


'''
def get_events(instanceid):
	response = cloudtrail.lookup_events (
		LookupAttributes=[
			{
				'AttributeKey': 'ResourceName',
				'AttributeValue': instanceid
			}
		],
	)
	return response


def get_ec2_owner(instanceid):
	events = get_events (instanceid)
	for event in events.get ("Events"):
		if event.get ("EventName") == "RunInstances":
			return event.get ("Username")
        else:
            return "no username found"
'''

session = boto3.Session(
        #pec staging
        region_name='us-west-1',
        profile_name='nbpecstaging'

        #aws dev
        #region_name='us-east-2',
        #profile_name='nbelser'
        )

ec2 = session.client('ec2')
#cloudtrail = session.client('cloudtrail')

response = ec2.describe_instances()
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
		#ip = instance["PrivateIpAddress"]
		#print(ip)
		try:
			platform = instance["InstanceId"]
		except KeyError as e:
			print("error")
        instanceName = instance["InstanceId"]
        user = ""
        launchDate = instance["LaunchTime"].strftime(DATE_STRING)
        try:
            #user = get_ec2_owner(instanceName)
            print(instanceName, launchDate, user)
            for tag in instance["Tags"]:
                value = tag['Value']
                print(tag['Key'], tag['Value'])
        except KeyError as e:
                print("no tag", instanceName, launchDate, user)

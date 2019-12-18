import boto3
import smtplib
import email.message

DATE_STRING = "%Y-%m-%d"

session = boto3.Session(
        #pec staging
        region_name='us-west-1',
        profile_name='nbpecstaging'

        #aws dev
        #region_name='us-east-2',
        #profile_name='nbelser'
        )

ec2 = session.client('ec2')

noTags = []
noServiceTags = []
noTenantTags = []
response = ec2.describe_instances()
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        service = False
        tenant = False
        noTag = False
        responsibleParty = ""
        instanceName = ""
        state = instance["State"]["Name"]
        #print(state)
        launchDate = instance["LaunchTime"].strftime(DATE_STRING)
        try:
            for tag in instance["Tags"]:
                if tag['Key'] == 'Tenant ID':
                    tenant = True
                if tag['Key'] == 'Service':
                    service = True
                if tag['Key'] == 'Responsible Party':
                    responsibleParty = tag['Value']
                if tag['Key'] == 'Name':
                    instanceName = tag['Value']
                #print(tag['Key'], tag['Value'])
        except KeyError as e:
            noTag = True
        #item = instance["InstanceId"] + " " + state + " " + launchDate  + " " + instanceName + " " + responsibleParty
        item = "<td>" + instance["InstanceId"] + "</td>"+ "\n"
        item += "<td>" + state + "</td>" + "\n"
        item += "<td>" + launchDate + "</td>" + "\n"
        item += "<td>" + instanceName + "</td>" + "\n"
        item += "<td>" + responsibleParty + "</td>" + "\n"
        if noTag == False:
            if service == False:
                #print(instance["InstanceId"], "has no Service tags")
                noServiceTags.append(item)
            if tenant == False:
                #print(instance["InstanceId"], "has no Tenant ID tags")
                noTenantTags.append(item)
        else:
            #print(instance["InstanceId"], "has no tags")
            noTags.append(item)

#print(noTags)
#print(noServiceTags)
#print(noTenantTags)
msgBody = "<html>" + "\n"
msgBody += "<body>" + "\n"
msgBody += "<h2>No Tags</h2>" + "\n"
msgBody += "<table>" + "\n"
msgBody += "<tr>" + "\n"
msgBody += "<th>" + "Instance ID" + "</th>"+ "\n"
msgBody += "<th>" + "State" + "</th>" + "\n"
msgBody += "<th>" + "Launch Date" + "</th>" + "\n"
msgBody += "<th>" + "Tag: Instance Name" + "</th>" + "\n"
msgBody += "<th>" + "Tag: Responsible Party" + "</th>" + "\n"
msgBody += "</tr>" + "\n"
msgBody += "<tr>"+ "\n"
for item in noTags:
    msgBody += item + "</tr>"
msgBody += "</table>" + "\n"

msgBody += "<h2>No TenantID Tags</h2>" + "<table>"+ "\n"
msgBody += "<tr>" + "\n"
msgBody += "<th>" + "Instance ID" + "</th>"+ "\n"
msgBody += "<th>" + "State" + "</th>" + "\n"
msgBody += "<th>" + "Launch Date" + "</th>" + "\n"
msgBody += "<th>" + "Tag: Instance Name" + "</th>" + "\n"
msgBody += "<th>" + "Tag: Responsible Party" + "</th>" + "\n"
msgBody += "</tr>" + "\n"
msgBody += "<tr>" + "\n"
for item in noTenantTags:
    msgBody += item +"</tr>"
msgBody += "</table>" + "\n"

msgBody += "<h2>No Service Tags</h2>" + "\n"
msgBody += "<table>" + "\n"
msgBody += "<tr>" + "\n"
msgBody += "<th>" + "Instance ID" + "</th>"+ "\n"
msgBody += "<th>" + "State" + "</th>" + "\n"
msgBody += "<th>" + "Launch Date" + "</th>" + "\n"
msgBody += "<th>" + "Tag: Instance Name" + "</th>" + "\n"
msgBody += "<th>" + "Tag: Responsible Party" + "</th>" + "\n"
msgBody += "</tr>" + "\n"
msgBody += "<tr>" + "\n"
for item in noServiceTags:
    msgBody += item +"</tr>"
msgBody += "</table>" + "\n"

'''
msgBody += "\n" + "<p>" + "No Tenant ID Tags:" + "<br>" + "\n"
for item in noTenantTags:
    msgBody += item + "<br>" + "\n"

msgBody += "\n" + "<p>" + "No Service Tags:" + "<br>" + "\n"
for item in noServiceTags:
    msgBody += item + "<br>" + "\n"
msgBody += "</p" + "\n"
'''

msgBody += "</body>" + "\n"
msgBody += "</html>" + "\n"


#print(msgBody)

sender = "nancy.belser@genesys.com"
receiver = "nancy.belser@genesys.com"
msg = email.message.Message()
msg['Subject'] = "EC2 Instances without Tags in PEC Staging (us-west-1)"
msg['From'] = sender
msg['To'] = receiver
msg.add_header('Content-Type','text/html')
msg.set_payload(msgBody)

try:
   smtpObj = smtplib.SMTP("exchange.genesyslab.com", 25)
   smtpObj.sendmail(msg['From'], msg['To'], msg.as_string())
   print("Successfully sent email")
except Exception:
   print("Error: unable to send email")

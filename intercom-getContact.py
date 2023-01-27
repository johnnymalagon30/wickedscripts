
import csv
import requests
import json
import time

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

session = requests.Session()

session.headers = {'Accept': 'application/json',
                   'Authorization': 'xxxx'
                  }


file_name = 'errorLog.csv'
with open(file_name, 'w', newline='') as csvfile:
    membershipwriter = csv.writer(csvfile, delimiter=',')
    membershipwriter.writerow(['contactId'])

contactFile = 'contactinfo.csv'
with open(contactFile, 'w', newline='') as newfile:
    contactwriter = csv.writer(newfile, delimiter=',')
    contactwriter.writerow(['uniqueID']+['name'])

with open('contactstoget.csv', 'r') as sampleFile:
    reader = csv.reader(sampleFile, delimiter = ',')
    header = next(reader)
    for row in reader:
        contactId = row[0]

        contactUrl = 'https://api.intercom.io/contacts/search'

        query1 = {"query": {
                        "field": "external_id", #"email"
                        "operator": "=",
                        "value": contactId
                        }
                 }

        try:
            contactget = session.post(url = contactUrl,json = query1)

            getContact = contactget.json()
            data = getContact['data']

            if contactget.status_code == 200:


                uniqueID = data[0]['id']

                name = data[0]['name']

                print(color.GREEN + 'Success retrieving {} {}!'.format(uniqueID,name) + color.END)


                with open(contactFile, 'a', newline='') as newfile:
                    contactwriter = csv.writer(newfile, delimiter=',')
                    contactwriter.writerow([uniqueID,name,contactId])

                time.sleep(1)



            elif contactget.status_code != 200:


                raise Exception
                print(contactget)


        except Exception:
            pass
            print(color.RED + 'Failed to get contact {}'.format(contactId) + color.END)
            with open(file_name, 'a', newline='') as csvfile:
                membershipwriter = csv.writer(csvfile, delimiter=',')
                membershipwriter.writerow([contactId])
            print(contactget)
            print(getContact)


exit()

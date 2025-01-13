
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

file_name = 'errorLog.csv'
with open(file_name, 'w', newline='') as csvfile:
    membershipwriter = csv.writer(csvfile, delimiter=',')
    membershipwriter.writerow(['name'])

contactFile = 'orginfo.csv'
with open(contactFile, 'w', newline='') as newfile:
    contactwriter = csv.writer(newfile, delimiter=',')
    contactwriter.writerow(['name']+['website']+['address']+['website']+['zip']+['phone'])


with open('orgstoget.csv', 'r') as sampleFile:
    reader = csv.reader(sampleFile, delimiter = ',')
    header = next(reader)
    for row in reader:
        orgName = row[0]
        #orgAddress = row[1]
        #orgWebsite = row[2]
        orgCity = row[1]
        orgState = row[2]
        orgZip = row[3]
        #orgPhone = row[4]


        orgUrl = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}%20{}%20{}%20{}&key=AIzaSyAh9tAZmzpQAcV0QFymcQeMZ3bCTt7LWRw".format(orgName,orgCity,orgState,orgZip)

        payload = {}
        headers = {}

        try:



            response = requests.request("GET", orgUrl, headers=headers, data=payload)


            getOrg = response.json()

            if response.status_code == 200 and getOrg['results'] != []:



                orgAddressInitial = getOrg['results'][0]['formatted_address']
                chunks = orgAddressInitial.split(',')
                orgAddress = chunks[0]

                site = getOrg['results'][0]['website']


                print(color.GREEN + 'Success retrieving {}!'.format(orgName) + color.END)


                with open(contactFile, 'a', newline='') as newfile:
                    contactwriter = csv.writer(newfile, delimiter=',')
                    contactwriter.writerow([orgName,site,orgAddress,orgCity,orgState,orgZip])


                print(getOrg)



            elif response.status_code != 200:
                pass
                print(color.RED + 'Failed to get org {}'.format(orgName) + color.END)
                with open(file_name, 'a', newline='') as csvfile:
                    membershipwriter = csv.writer(csvfile, delimiter=',')
                    membershipwriter.writerow([orgName])
                    print(response)
                    print(getOrg)





        finally:
            pass



exit()

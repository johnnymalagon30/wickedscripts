#This script reads an appropriately formatted CSV file and creates corresponding Intercom Company records. Edits are always necessary depending on requester's needs. DO NOT run as is.

#Import relevant libraries
import csv
import requests
import json

#Color class for easier reading in terminal output
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
                   'Authorization': 'xxxx' #place the appropriate dev or prod environment API key here
                  }

companyUrl = 'https://api.intercom.io/companies'

#This creates a .csv file where any error information will be placed during runtime
file_name = 'companieserrorLog.csv'
with open(file_name, 'w', newline='') as csvfile:
    membershipwriter = csv.writer(csvfile, delimiter=',')
    membershipwriter.writerow(['companyId']+['status']+['company']+['address']+['city']+['state']+['zip']+['type']+['created']+['number']+['size']+['source'])

#After each new company is created in Intercom, the requested information will be placed in this new .csv file
companyFile = 'newCompanies.csv'
with open(companyFile, 'w', newline='') as newfile:
    contactwriter = csv.writer(newfile, delimiter=',')
    contactwriter.writerow(['uniqueId']+['companyId']+['companyName'])

#Opens the properly formatted .csv file with relevant new company data to be inserted into Intercom
with open('companiestocreate.csv', 'r') as sampleFile:
    reader = csv.reader(sampleFile, delimiter = ',')
    header = next(reader)
    for row in reader:
        companyName = row[2]
        companyId = row[0]

        orgType = row[7]
        city = row[4]
        created = row[8]
        size = row[10]
        state = row[5]
        zip = row[6]
        source = row[11]
        status = row[1]
        number = row[9]
        address1 = row[3]


        data = {'company_id': '{}'.format(companyId),
                'name': '{}'.format(companyName),
                'remote_created_at': '{}'.format(created),
                'size': '{}'.format(size),
                'custom_attributes': {
                    'organizationType': '{}'.format(orgType),

                    'city': '{}'.format(city),
                    'state': '{}'.format(state),
                    'zipCode': '{}'.format(zip),
                    'creation_source': '{}'.format(source),
                    'organizationStatus': '{}'.format(status),
                    'organizationSmsNumber': '{}'.format(number),
                    'Billing Address': '{}'.format(address1)
                    #'exclusionList': 'True'



                }
                }


        try:
            companyCreate = session.post(url = companyUrl, json = data)
            newCompany = companyCreate.json()


            if companyCreate.status_code == 200:


                print(color.GREEN + 'Success! Created or updated company {}'.format(companyId) + color.END)
                uniqueId = newCompany['id']


                print(newCompany)

                with open(companyFile, 'a', newline='') as newfile:
                    contactwriter = csv.writer(newfile, delimiter=',')
                    contactwriter.writerow([uniqueId,companyId,companyName])



            elif companyCreate.status_code != 200:

                print(color.RED + 'Failed to create company {}. Status code does not equal 200'.format(companyId) + color.END)
                raise Exception




        except Exception:
            pass

            print(color.RED + 'Failed to create company {}, it may already exist'.format(companyId) + color.END)
            with open(file_name, 'a', newline='') as csvfile:
                membershipwriter = csv.writer(csvfile, delimiter=',')
                membershipwriter.writerow([companyId,status,companyName,address1,city,state,zip,orgType,created,number,size,source])
            print(companyCreate)
            print(newCompany)
            #print(response)



exit()

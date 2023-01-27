#Import relevant libraries.
import csv
import requests
import json
import stripe

#Class for color logging. Easier reading.
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

#Insert your Stripe API key here. Can be for production or dev.
stripe.api_key = "xxxx"

#This creates and opens a CSV file where errors will be placed during runtime.
file_name = 'errorLog.csv'
with open(file_name, 'w', newline='') as csvfile:
    membershipwriter = csv.writer(csvfile, delimiter=',')
    membershipwriter.writerow(['customer']+['email'])


#Opens the formatted CSV with customer data and assigns variables to them based off the column number in the file, starting with row 0.
with open('customerstoupdate.csv', 'r') as sampleFile:
    reader = csv.reader(sampleFile, delimiter = ',')
    header = next(reader)
    for row in reader:
        cusId = row[0]
        cusName = row[1]
        addressLine = row[2]
        cusCity = row[3]
        cusState = row[4]
        cusZip = row[5]
        platformType = row[7]
        salesforceId = row[8]
        #thryveOrgId = row[3]
        #thryveUserId = row[4]

        try:
            cusUpdate = stripe.Customer.modify(
                '{}'.format(cusId),
                name = '{}'.format(cusName),
                metadata = {
                            #'thryveOrgId': '{}'.format(thryveOrgId),
                            #'thryveUserId': '{}'.format(thryveUserId),
                            'salesforceId': '{}'.format(salesforceId),
                            'platformEntityType': '{}'.format(platformType)
                            },
                address = {
                            'line1': '{}'.format(addressLine),
                            'city': '{}'.format(cusCity),
                            'state': '{}'.format(cusState),
                            'postal_code': '{}'.format(cusZip),
                            'country': 'United States'
                            }
            )

            print(cusUpdate)


        except Exception:
            pass
            print(color.RED + 'Failed to update customer {}'.format(cusId) + color.END)
            with open(file_name, 'a', newline = '') as csvfile:
                membershipwriter = csv.writer(csvfile, delimiter=',')
                membershipwriter.writerow([cusId])

                #This "with open" portion writes to the error log CSV if the call encounteres an exception.



exit()

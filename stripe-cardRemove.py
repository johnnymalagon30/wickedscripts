#This script takes all the associated payment methods attached to a customer account and wipes them from the account. This is necessary because QA has several test a
#accounts with hundreds of payment methods and they eventually reach the limit that Stripe allows.

#Import relevant libraries

import stripe
import csv
import requests
import json

# Color schema for easier reading of terminal output
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

#Place the appropriate dev or prod key here
stripe.api_key = "xxxx"

#Opens .csv file where error information will be placed during runtime.
file_name = 'errorLog.csv'
with open(file_name, 'w', newline='') as csvfile:
    membershipwriter = csv.writer(csvfile, delimiter=',')
    membershipwriter.writerow(['method'])

#Define the recursive function
def real_extract():
    get = stripe.Customer.list_payment_methods(
      "xxxxxxx", #place the unique customer ID of the QA account here===
      type="card",
      limit=500
    )

    getData = get['data']
    print(getData)

    if getData != []:
        for method in getData:

            paymentId = method['id']

            try:
                paymentRemove = stripe.PaymentMethod.detach(
                    "{}".format(paymentId),
                )

                print(color.GREEN + 'Removed card {}'.format(paymentId) + color.END)

            except Exception:
                pass
                print(color.RED + 'Failed to cancel method {}'.format(paymentId) + color.END)
                with open(file_name, 'a', newline='') as csvfile:
                    membershipwriter = csv.writer(csvfile, delimiter=',')
                    membershipwriter.writerow([paymentId]) #If an error is encountered, the payment ID will be placed in the error log file that was
                                                           #created earlier in the script

        real_extract()

    else:
        exit()

real_extract()

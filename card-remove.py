import stripe
import csv
import requests
import json

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

stripe.api_key = "xxxx"

file_name = 'errorLog.csv'
with open(file_name, 'w', newline='') as csvfile:
    membershipwriter = csv.writer(csvfile, delimiter=',')
    membershipwriter.writerow(['method'])

def real_extract():
    get = stripe.Customer.list_payment_methods(
      "cus_M0IIHc2fdgJhXc",
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
                    membershipwriter.writerow([paymentId])

        real_extract()

    else:
        exit()

real_extract()

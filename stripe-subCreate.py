#This script reads an appropriately formatted CSV file and creates corresponding Stripe subscriptions. Edits are always necessary depending on requester's needs. DO NOT run as is.

#Import relevant libraries.
import csv
import requests
import json
import stripe

#Class for color logging. Easier reading in terminal.
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

#Insert your Stripe API key here. Can be for production or dev environment.
stripe.api_key = "xxxx"

#This creates and opens a CSV file where error information will be placed during runtime.
file_name = 'errorLog.csv'
with open(file_name, 'w', newline='') as csvfile:
    membershipwriter = csv.writer(csvfile, delimiter=',')
    membershipwriter.writerow(['customer']+['error'])

#Opens the formatted CSV with subscription data and assigns variables to them based off the column number in the file, starting with row 0.
with open('substocreate.csv', 'r') as sampleFile:
    reader = csv.reader(sampleFile, delimiter = ',')
    header = next(reader)
    for row in reader:
        stripeId = row[0]
        priceId1 = row[1]
        priceId2 = row[2]
        #quantity = row[3]
        #subMeta = row[4]
        #anchor = row[5]
        #backdate = row[6]
        product = row[3]




        if product != '': #if the product field is not empty, that means we're creating a custom priced product.
            try:
                subscriptionCreate = stripe.Subscription.create(
                    customer = '{}'.format(stripeId),
                    #collection_method = 'send_invoice',
                    #days_until_due = '30',
                    items = [

                        {'price_data': {
                            'unit_amount': '{}'.format(customPrice),
                            'currency': 'usd',
                            'product': '{}'.format(product),
                            'recurring': {
                                'interval': '{}'.format(interval)
                            }
                        }}
                    ],
                    trial_period_days = '{}'.format(trialDays),
                    backdate_start_date = '1629028800',
                    trial_from_plan = 'false'
                    )
                print(subscriptionCreate)
            except Exception:
                pass
                print(color.RED + 'Failed to create subscription for customer {}, custom price {}'.format(stripeId, product) + color.END)
                with open(file_name, 'a', newline='') as csvfile:
                    membershipwriter = csv.writer(csvfile, delimiter=',')
                    membershipwriter.writerow([stripeId,product])
                    #This "with open" portion writes to the error log CSV that was previously created if the call encounters an exception.



        elif priceId1 != '' and priceId2 != '': #if both price fields are populated, that means we're creating ONE subscription with multiple items.
            try:
                subscriptionCreate = stripe.Subscription.create(
                    customer = '{}'.format(stripeId),
                    #collection_method = 'charge_automatically',
                    #days_until_due = '5',
                    items = [
                        {'price': '{}'.format(priceId1)},
                        {'price': '{}'.format(priceId2)}
                    ],

                    #backdate_start_date = '{}'.format(backdate),
                    #billing_cycle_anchor = '{}'.format(anchor),
                    #proration_behavior = 'none',
                    #metadata = {'thryvesubid': '{}'.format(subMeta)},

                    coupon = 'Eq6gr93t'
                    #trial_period_days = '{}'.format(trialDays),
                    #trial_from_plan = 'false'

                    )
                print(subscriptionCreate)
            except Exception:
                pass
                print(color.RED + 'Failed to create subscription for customer {}, subscription {}'.format(stripeId,priceId1) + color.END)
                with open(file_name, 'a', newline='') as csvfile:
                    membershipwriter = csv.writer(csvfile, delimiter=',')
                    membershipwriter.writerow([stripeId, priceId1])
                    #This "with open" portion writes to the error log CSV that was previously created if the call encounters an exception.



        else: #if only one price field is populated, that means we're creating a standard subscription with one item included.
            try:
                subscriptionCreate = stripe.Subscription.create(
                    customer = '{}'.format(stripeId),
                    collection_method = 'send_invoice',
                    days_until_due = '30',

                    items = [
                        {'price': '{}'.format(priceId1)}

                    ],
                    #trial_period_days = '{}'.format(trialDays),
                    backdate_start_date = '{}'.format(backdate),
                    billing_cycle_anchor = '{}'.format(anchor),
                    metadata = {'thryvesubid': '{}'.format(subMeta)}
                    #trial_from_plan = 'false',
                    #coupon = '{}'.format(coupon)
                    )
                print(subscriptionCreate)
            except Exception:
                pass
                print(color.RED + 'Failed to create subscription for customer {}, subscription {}'.format(stripeId,priceId1) + color.END)
                with open(file_name, 'a', newline='') as csvfile:
                    membershipwriter = csv.writer(csvfile, delimiter=',')
                    membershipwriter.writerow([stripeId,priceId1])
                    #This "with open" portion writes to the error log CSV that was previously created if the call encounters an exception.







exit()

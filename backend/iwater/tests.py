from django.test import TestCase

# Create your tests here.


# import requests
# # url = "https://www.fast2sms.com/dev/bulk"
# # payload = "sender_id=FTWSMS&message={'test':1234}&language=english&route=p&numbers=9539390191"
# # headers = {'authorization': "O3hiCG2Tz7tcS4HFrsAdmpULKJea0gBjR5Ix6foMYPu1bkvWVE67D2Qj4TUZekadKnYvI9RCiu1hEwpN",
# #            'Content-Type': "application/x-www-form-urlencoded",'Cache-Control': "no-cache",}
# # response = requests.request("POST", url, data=payload, headers=headers)
# url = "https://www.fast2sms.com/dev/bulkV2"
#
# querystring = {
#     "authorization": "O3hiCG2Tz7tcS4HFrsAdmpULKJea0gBjR5Ix6foMYPu1bkvWVE67D2Qj4TUZekadKnYvI9RCiu1hEwpN",
#     "message": "This is test Message sent from \
#          Python Script using REST API.",
#     "language": "english",
#     "route": "q",
#     "numbers": "9539390191"}
#
# headers = {
#     'cache-control': "no-cache"way2sms
# }
# try:
#     response = requests.request("POST", url,
#                                 headers=headers,
#                                 params=querystring)
#     print(response.text)
#     print("SMS Successfully Sent")
# except:
#     print("Oops! Something wrong")


# site_obj_for_getting_count = SitePermission.objects.filter(site_id=site_id)
#             for site_dat in site_obj_for_getting_count.values():
#                 print(site_dat["user_id"])
#
#                 user_dat_for_getting_user_role_count = User.objects.filter(id=site_dat["user_id"])
#                 for user_dat in user_dat_for_getting_user_role_count.values():
#                     if user_dat["is_supervisor"]:
#                         supervisor_count_in_this_site += 1
#                     elif user_dat["is_operator"]:
#                         operator_count_in_this_site += 1
#             print("Site {} has {} supervisors & {} operators".format(site_user["site_name"],
#                                                                      supervisor_count_in_this_site,
#                                                                      operator_count_in_this_site))

# import smtplib
# # from signin import
# emailadress = "tony.joy.tm@gmail.com"
# password = "xhawroxjuxjwgkvz"
# number = "09539390191"
# smtplibserver='smtp.gmail.com'
#
# if __name__=="__main__":
#     server = smtplib.SMTP_SSL(smtplibserver, 465)
#     server.ehlo()
#     server.login(emailadress, password)
#     print("You're logged in!")
#
#     usertext ="What is your message?"
#     server.sendmail(emailadress, number, usertext)
#     print("\nSent!\n")

# import os, vonage
#
# VONAGE_API_KEY = "ef9f7494"
# VONAGE_API_SECRET = "XdMofLWHcs070TDU"
#
# #Create a client instance and then pass the client to the Sms instance
# client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
# sms = vonage.Sms(client)
#
# response = sms.send_message(
#     {
#         "from": "VONAGE_BRAND_NAME",
#         "to": "+919539390191",
#         "text": "Hello there from Vonage SMS API",
#     }
# )
#
# if response["messages"][0]["status"] == "0":
#     print("Message Details: ", response)
#     print("Message sent successfully.")
# else:
#     print(f"Message failed with error: {response['messages'][0]['error-text']}")

import os

# auth_id = "MAZJK4ZTC4ZWM3Y2U0ZW"
# auth_token = "MjE5ZGRlNTY1Mzc4MzFkOGQ0MDkzOTE2MTUwYjll"
#
# import plivo
#
# client = plivo.RestClient(auth_id,auth_token)
# message_created = client.messages.create(
#     src = "+919645578992",
#     dst = "+919539390191",
#     text='Hello there from Plivo SMS API2!'
# )

# pip3 install razorpay
import razorpay
client = razorpay.Client(auth=("rzp_live_xjxfrlgTO5aI1h", "2b07hErDEbXA9VDuqqKm9Orl"))

data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }

# client.payment.all(option)

payment = client.order.create(data=data)
print(payment)

client.payment.capture(payment["id"],{
  "amount" : 500,
  "currency" : "INR"
})
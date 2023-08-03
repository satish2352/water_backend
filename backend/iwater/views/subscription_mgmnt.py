from django.conf import Settings

from datetime import datetime, timedelta
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from django.db import transaction
import razorpay
from iwater.views import subscription_mgmnt
from iwater.models import Site, Subscription, Price, Order, PaymentStatus, Device
from iwater.models import Device
from iwater.iw_logger import logger

#RAZORPAY_KEY_ID = "rzp_test_3QpbuKajQD2BSW"
#RAZORPAY_KEY_SECRET = "t0Fb5NVLtknI4HYZt7vCLEFb"

# ! meeting notes (changes to be done) 


# ! When a new site is registered we will not require any license. Based on the registration date, we will provide a 30 day free access and we will call this Active (Free Trial)

# ! If the device id is found in a deleted device/site then we will not create a new site/device but reactivate the old one (so we want to avoid user using same device to get free trials again and again)

# ! new site => new device (if device id is presetn, don't add the site)

# ! expiray -> order -> site -> status (active(Purchased) ?: order linked , active-free(default), grace-period ( data and warning message, allow to renew), expired(subscrption period is over) )

# ! The site status should be checked daily and updated once - active, active-free, grace, expired

# ! Order History - Show as a timeline the order value, the no. of sites (on hover - show site list in a pop-up), site type

# ! We need to allow the site to be deleted and its order assigned to another site (transferring expiry date of one site to other side)

# ! view as per fornt end table, populated in the view



RAZORPAY_KEY_ID = "rzp_test_3qgfhK1jrmU04Y"
RAZORPAY_KEY_SECRET = "vN9iYR9zYO5VjF0RwdkvBr17"
    #-------------------------- Under code added by Ajim Shaikh on 28/06/2023 for show data ------------------------------
# @api_view(['GET'])
# def showdata(request):

    # # ! High level object to store data after iteration
    # if request.method == 'GET':
    #    #summary_data2 = []
    #     Treatment_Unit_Active = []
    #     Treatment_Unit_Expired = []
    #     Treatment_Unit_Free_Trial = []
    #     Dispensing_Unit_Active = []
    #     Dispensing_Unit_Expired = []
    #     Dispensing_Unit_Free_Trial = []
        
       

        
          
    #     showdata = Site.objects.all().values('id')
    #     print("This is show data:", showdata)
    #     for a in showdata:
    #         print("This is Site List:", a)
    #             ##---------------------Under Implement code with aseem Sir Logic------------------------------------------------------
    #             # sub = Subscription.objects.filter(site_id =a["id"],is_treatment_unit=1).order_by('-days_to_expire').values('site_id','days_to_expire','order_id')
    #             # sub1 = sub[0]
    #             # dte = sub1('days_to_expire')
    #             # o_id = sub1('order_id')
    #             ##---------------------Above Implement code with aseem Sir Logic------------------------------------------------------
    #         obj1= Subscription.objects.filter(site_id = a['id'],is_treatment_unit=1).order_by('-days_to_expire').values('site_id','days_to_expire','order_id')
    #         if len(obj1) !=0:
                
    #             sub1 = obj1[0] 
    #             print("This is treatment Subscription List:",sub1)

    #             if(sub1["days_to_expire"]>0 and sub1["order_id"]!=None):
    #             ##---------------------Under Implement code with aseem Sir Logic------------------------------------------------------
    #                 div1= Device.objects.filter(site= a['id']).update(device2_sub_status="Active")
    #                 print(div1,' ',sub1) 

    #                 Treatment_Unit_Active.append(div1)
        
    #             elif(sub1["days_to_expire"]<=0):
    #                 div2= Device.objects.filter(site= a['id']).update(device2_sub_status="Expired")
    #                 print(div2,' ',sub1)

    #                 Treatment_Unit_Expired.append(div2)

    #             elif(sub1["days_to_expire"]>0 and sub1["order_id"]==None):
    #                 div3= Device.objects.filter(site= a['id']).update(device2_sub_status="Free_Trial")
    #                 print(div3,' ',sub1)
    #                 Treatment_Unit_Free_Trial.append(div3)
    #         else:
    #             ("NO Data found for Treatment Unit")
            


    #         obj2= Subscription.objects.filter(site_id = a['id'],is_dispensing_unit=1).order_by('-days_to_expire').values('site_id','days_to_expire','order_id')
    #         if len(obj2)!=0 :
    #             print("This is dispensing unit Subscription List:",obj2)
    #             sub2 = obj2[0] 
    #             print("This is dispensing unit Subscription List:",sub2)
    #             if(sub2["days_to_expire"]>0 and sub2["order_id"]!=None):
    #             ##---------------------Under Implement code with aseem Sir Logic------------------------------------------------------
    #                 div4= Device.objects.filter(site= a['id']).update(device3_sub_status="Active")
    #                 print(div4,' ',sub2)
    #                 Dispensing_Unit_Active.append(div4) 
        
    #             elif(sub2["days_to_expire"]<=0):
    #                 div5= Device.objects.filter(site= a['id']).update(device3_sub_status="Expired")
    #                 print(div5,' ',sub2)
    #                 Dispensing_Unit_Expired.append(div5)
                    

    #             # elif(sub1.filter(days_to_expire__gt=0).filter(days_to_expire__lte=30).filter(order_id__isnull=True)):
    #             elif(sub2["days_to_expire"]>0 and sub2["order_id"]==None):
    #                 div6= Device.objects.filter(site= a['id']).update(device3_sub_status="Free_Trial")
    #                 print(div6,' ',sub2)
    #                 Dispensing_Unit_Free_Trial.append(div6)
    #         else:
    #             ("NO Data found for Dispensing Unit")

        
    # else:
    #     print("no site id found")
    
    # context = { 
    #             'Treatment_Unit_Active':Treatment_Unit_Active,
    #             'Treatment_Unit_Expired':Treatment_Unit_Expired,
    #             'Treatment_Unit_Free_Trial':Treatment_Unit_Free_Trial,
    #             'Dispensing_Unit_Active':Dispensing_Unit_Active,      
    #             'Dispensing_Unit_Expired':Dispensing_Unit_Expired,         
    #             'Dispensing_Unit_Free_Trial':Dispensing_Unit_Free_Trial,
    #             }

    # return JsonResponse(
    #     {"Response": {
    #         "Status": "success"
    #         },
    #         "Data": context
    #     }, safe=False, status=status.HTTP_200_OK)
    
      
 #-------------------------- Above code added by Ajim Shaikh on 28/06/2023 for show data ------------------------------

@api_view(['GET'])
def list_sub(request):
    summary_data = []

    # ! High level object to store data after iteration

    total_treatment_sites = 0
    free_treatment_trials = 0
    treatment_expired_free_trials = 0
    active_treatment_sites = 0
    expired_treatment_sites = 0
    active_treatment_licenses = 0
    expired_treatment_licenses = 0

    # ! treatment data array
    free_treatment_data = []
    free_expired_treatment_data = []
    active_treatment_data = []
    expired_treatment_data = []

    treatment_last_paid = 0
    treatment_total_paid = 0

    total_dispensing_sites = 0
    free_dispensing_trials = 0
    dispensing_expired_free_trials = 0
    active_dispensing_sites = 0
    expired_dispensing_sites = 0
    active_dispensing_licenses = 0
    expired_dispensing_licenses = 0

    #  ! dispensing data array
    free_dispensing_data = []
    free_expired_dispensing_data = []
    active_dispensing_data = []
    expired_dispensing_data = []

    dispensing_last_paid = 0
    dispensing_total_paid = 0

    total_treatment_subscriptions = []
    total_dispensing_subscriptions = []

    # ! set expiry for all company subscriptions
    all_subscription = Subscription.objects.all().order_by('-id')  # .order_by('-created')
    for subs in all_subscription.values(): # ! creates an object which we can interate through

        single_subscription = Subscription.objects.get(id=subs["id"])  # ! stores one subscription
        valid_till = datetime.strptime(str(subs["valid_till"]), "%Y-%m-%d")
        present_date = datetime.now()
        # logger.info("present_date - {}".format(present_date))
        # logger.info("valid_till - {}".format(valid_till))

        days_left = (valid_till - present_date).days + 1 # ! checks validity in days
        # logger.info("days left {}".format(days_left))
        single_subscription.days_to_expire = days_left # ! sets days to expire values. Loads on every fetch from frontend, changes dynamically
        if days_left <= 0:
            single_subscription.expired = True
        single_subscription.save() # ! updates database with lates infromation 

    # get all subs associated with site
    # check whether the site has 2 subs expired
    # if both are expired set site as expired
    # else keep as active
    # if site has only one sub then expire the site

    all_expired_subscription = Subscription.objects.filter(expired=True).order_by('-id')
    # ! Collects expired sites from subscription table

    for subs in all_expired_subscription.values():
  
        # ! iterates over each expired subscriptions

        subscriptions = Subscription.objects.filter(site_id=subs["site_id"])  
        # ! assigns subscriptions 
        expired_count = 0

        # ! Following is the code to iterate over the subscriptions and to set the site to expired
        if subscriptions.count() > 1:
            logger.info("Found 2 subscriptions for this site")
            for single_subscription in subscriptions.values():
                if single_subscription["expired"]:
                    expired_count += 1

            if expired_count > 1:
                logger.info("And these 2 subscriptions are expired, hence setting the associated site as expired")
                single_site = Site.objects.get(id=subs["site_id"])
                single_site.status = False
                single_site.save()
        else:
            logger.info("Found 1 subscription for this site")
            for single_subscription in subscriptions.values():
                if single_subscription["expired"]:
                    expired_count += 1

            if expired_count > 0:
                logger.info("And this subscription is expired, hence setting the associated site as expired")
                single_site = Site.objects.get(id=subs["site_id"])
                single_site.status = False
                single_site.save()

    if request.method == 'GET':

        # ! access validation
        if request.user.is_supervisor or request.user.is_operator:
            response = {"Response": {
                "Status": "error"},
                "message": "You({user}) are not authorized to view this page".format(user=request.user)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)

        treatment_subscription = Subscription.objects.filter(company_id=request.user.company_id, is_treatment_unit=True).\
            order_by('-created')
        # ! assigns subscriptions for a particular company by company id
        
        logger.info("Treatment Units")

        for subs in treatment_subscription.values():
            
            logger.info("\nsubscription - {}".format(subs["id"]))
            logger.info("subscription_code - {}".format(subs["subscription_code"]))

            treatment_total_paid += subs["total_paid"]
            # ! calculates value of paid subscriptions for treatment

            try:
                site_obj = Site.objects.get(id=subs["site_id"])
                site_name = site_obj.site_name
                if site_obj.is_treatment_unit:
                    total_treatment_sites += 1
                    if site_obj.status is True:
                        active_treatment_sites += 1
                    elif site_obj.status is False:
                        expired_treatment_sites += 1
            except Exception as e:
                site_name = ""

            license_status = ""

            # ! following code populates data based on subscription_code and expiration status
            if subs["subscription_code"] is None and not subs["expired"]:
                license_status = "active_free_license" 
                # ! setting active free liscence here
                
                free_treatment_trials += 1
                logger.info("subscription code is none and hence its free site")
                logger.info("site_id {}".format(subs["site_id"]))
                logger.info("site_name {}".format(site_name))
                free_treatment_resp = {
                    'subscription_id': subs["id"],
                    'site_id': subs["site_id"] if subs["site_id"] else None,
                    'site_name': site_name if site_name else "",
                    'subscription_type': "Treatment Unit",
                    'start_date': subs["created"],
                    "valid_till": subs["valid_till"],
                    "days_to_expire": subs["days_to_expire"],
                }
                free_treatment_data.append(free_treatment_resp)
            elif subs["subscription_code"] is None and subs["expired"]:
                logger.info("subscription code is none and its expired and hence its expired free trial")
                logger.info("site_id {}".format(subs["site_id"]))
                logger.info("site_name {}".format(site_name))
                treatment_expired_free_trials += 1
                license_status = "expired_free_license"
                expired_treatment_resp = {
                    'subscription_id': subs["id"],
                    'site_id': subs["site_id"] if subs["site_id"] else None,
                    'site_name': site_name if site_name else "",
                    'subscription_type': "Treatment Unit",
                    'start_date': subs["created"],
                    "valid_till": subs["valid_till"],
                    "days_to_expire": subs["days_to_expire"],
                }
                free_expired_treatment_data.append(expired_treatment_resp)
            elif subs["subscription_code"] is not None and not subs["expired"]:
                logger.info("subscription is valid and hence its assigned site")
                logger.info("site_id {}".format(subs["site_id"]))
                logger.info("site_name {}".format(site_name))
                active_treatment_licenses += 1
                license_status = "active_license"
                active_treatment_resp = {
                    'subscription_id': subs["id"],
                    'site_id': subs["site_id"] if subs["site_id"] else None,
                    'site_name': site_name if site_name else "",
                    'subscription_type': "Treatment Unit",
                    'start_date': subs["created"],
                    "valid_till": subs["valid_till"],
                    "days_to_expire": subs["days_to_expire"],
                }
                active_treatment_data.append(active_treatment_resp)
            elif subs["subscription_code"] is not None and subs["expired"]:
                logger.info("subscription code is not none but expired and hence its expired license")
                logger.info("site_id {}".format(subs["site_id"]))
                logger.info("site_name {}".format(site_name))
                expired_treatment_licenses += 1
                license_status = "expired_license"
                inactive_treatment_resp = {
                    'subscription_id': subs["id"],
                    'site_id': subs["site_id"] if subs["site_id"] else None,
                    'site_name': site_name if site_name else "",
                    'subscription_type': "Treatment Unit",
                    'start_date': subs["created"],
                    "valid_till": subs["valid_till"],
                    "days_to_expire": subs["days_to_expire"],
                }
                expired_treatment_data.append(inactive_treatment_resp)

            total_treatment_subscriptions_resp = {
                'subscription_id': subs["id"],
                'site_id': subs["site_id"] if subs["site_id"] else None,
                'site_name': site_name if site_name else "",
                'subscription_type': "Treatment Unit",
                'start_date': subs["created"],
                "valid_till": subs["valid_till"],
                "license_status": license_status, # ! liscence / subscription status based on above data population
                "status": license_status,
                "days_to_expire": subs["days_to_expire"],
            }

            price = Price.objects.all()
            if price:
                for per_rate in price.values():
                    treatment_per_price = per_rate["treatment_price"]
                    treatment_per_tax = per_rate["treatment_tax"]
                    dispensing_per_price = per_rate["dispensing_price"]
                    dispensing_per_tax = per_rate["dispensing_tax"]
                    total_treatment_subscriptions_resp.update({ "treatment_per_price": treatment_per_price, # ! updates price in total_treatment_subscriptions_resp
            "treatment_per_tax": treatment_per_tax,
            'last_paid': subs["last_paid"],
            'total_paid': subs["total_paid"]})
            total_treatment_subscriptions.append(total_treatment_subscriptions_resp)

        logger.info("Dispensing Units")
        # ! same logic as above only for dispensing unit
        dispensing_subscription = Subscription.objects.filter(company_id=request.user.company_id, is_dispensing_unit=True).order_by('-created')
        for subs in dispensing_subscription.values():
            logger.info("\nsubscription - {}".format(subs["id"]))
            logger.info("subscription_code - {}".format(subs["subscription_code"]))

            dispensing_total_paid += subs["total_paid"]

            try:
                site_obj = Site.objects.get(id=subs["site_id"])
                site_name = site_obj.site_name
                if site_obj.is_dispensing_unit:
                    total_dispensing_sites += 1
                    if site_obj.status is True:
                        active_dispensing_sites += 1
                    elif site_obj.status is False:
                        expired_dispensing_sites += 1
            except Exception as e:
                site_name = ""

            license_status = ""
            # valid_till = datetime.strptime(str(subs["valid_till"]), "%Y-%m-%d")
            # present_date = datetime.now()
            # logger.info("present_date - {}".format(present_date))
            # logger.info("valid_till - {}".format(valid_till))

            if subs["subscription_code"] is None and not subs["expired"]:
                free_dispensing_trials += 1
                license_status = "active_free_license"
                free_dispensing_resp = {
                    'subscription_id': subs["id"],
                    'site_id': subs["site_id"],
                    'site_name': site_name,
                    'subscription_type': "Dispensing Unit",
                    'start_date': subs["created"],
                    "valid_till": subs["valid_till"],
                    "days_to_expire": subs["days_to_expire"],
                }
                free_dispensing_data.append(free_dispensing_resp)
            elif subs["subscription_code"] is None and subs["expired"]:
                logger.info("subscription code is none and its expired and hence its expired free trial")
                dispensing_expired_free_trials += 1
                license_status = "expired_free_license"
                inactive_dispensing_resp = {
                    'subscription_id': subs["id"],
                    'site_id': subs["site_id"],
                    'site_name': site_name,
                    'subscription_type': "Dispensing Unit",
                    'start_date': subs["created"],
                    "valid_till": subs["valid_till"],
                    "days_to_expire": subs["days_to_expire"],
                }
                free_expired_dispensing_data.append(inactive_dispensing_resp)
            elif subs["subscription_code"] is not None and not subs["expired"]:
                logger.info("subscription is valid and hence its assigned site")
                active_dispensing_licenses += 1
                license_status = "active_license"
                active_dispensing_resp = {
                    'subscription_id': subs["id"],
                    'site_id': subs["site_id"],
                    'site_name': site_name,
                    'subscription_type': "Dispensing Unit",
                    'start_date': subs["created"],
                    "valid_till": subs["valid_till"],
                    "days_to_expire": subs["days_to_expire"],
                }
                active_dispensing_data.append(active_dispensing_resp)
            elif subs["subscription_code"] is not None and subs["expired"]:
                logger.info("subscription is expired and hence its unassigned site")
                expired_dispensing_licenses += 1
                license_status = "expired_license"
                inactive_dispensing_resp = {
                    'subscription_id': subs["id"],
                    'site_id': subs["site_id"],
                    'site_name': site_name,
                    'subscription_type': "Dispensing Unit",
                    'start_date': subs["created"],
                    "valid_till": subs["valid_till"],
                    "days_to_expire": subs["days_to_expire"],
                }
                expired_dispensing_data.append(inactive_dispensing_resp)

            total_dispensing_subscriptions_resp = {
                'subscription_id': subs["id"],
                'site_id': subs["site_id"] if subs["site_id"] else None,
                'site_name': site_name if site_name else "",
                'subscription_type': "Treatment Unit",
                'start_date': subs["created"],
                "valid_till": subs["valid_till"],
                "license_status": license_status,
                "status": license_status,
                "days_to_expire": subs["days_to_expire"],
            }

            price = Price.objects.all()
            if price:
                for per_rate in price.values():
                    treatment_per_price = per_rate["treatment_price"]
                    treatment_per_tax = per_rate["treatment_tax"]
                    dispensing_per_price = per_rate["dispensing_price"]
                    dispensing_per_tax = per_rate["dispensing_tax"]
                    total_dispensing_subscriptions_resp.update({"treatment_per_price": dispensing_per_price,
                                                               "treatment_per_tax": dispensing_per_tax,
                                                               'last_paid': subs["last_paid"],
                                                               'total_paid': subs["total_paid"]})

            total_dispensing_subscriptions.append(total_dispensing_subscriptions_resp)

        treatment_per_price = 0
        treatment_per_tax = 0
        dispensing_per_price = 0
        dispensing_per_tax = 0

        price = Price.objects.all()
        if price:
            for per_rate in price.values():
                treatment_per_price = per_rate["treatment_price"]
                treatment_per_tax = per_rate["treatment_tax"]
                dispensing_per_price = per_rate["dispensing_price"]
                dispensing_per_tax = per_rate["dispensing_tax"]

        resp = {
            'serial_no': 1,
            'subscription_category': "Treatment Unit",
            'no_of_total_sites': total_treatment_sites,
            'no_of_active_sites': active_treatment_sites,
            'no_of_expired_sites': expired_treatment_sites,
            'no_of_active_free_trials': free_treatment_trials,
            'no_of_expired_free_trials': treatment_expired_free_trials,
            'no_of_active_licenses': active_treatment_licenses,
            'no_of_expired_licenses': expired_treatment_licenses,
            "total_licenses": total_treatment_subscriptions,
            "free_trials": free_treatment_data,
            "expired_free_trials": free_expired_treatment_data,
            "active_licenses": active_treatment_data,
            "expired_licenses": expired_treatment_data,
            "treatment_per_price": treatment_per_price,
            "treatment_per_tax": treatment_per_tax,
            'last_paid': treatment_last_paid,
            'total_paid': treatment_total_paid
        }
        summary_data.append(resp)
        resp = {
            'serial_no': 2,
            'subscription_category': "Dispensing Unit",
            'no_of_total_sites': total_dispensing_sites,
            'no_of_active_sites': active_dispensing_sites,
            'no_of_expired_sites': expired_dispensing_sites,
            'no_of_active_free_trials': free_dispensing_trials,
            'no_of_expired_free_trials': dispensing_expired_free_trials,
            'no_of_active_licenses': active_dispensing_licenses,
            'no_of_expired_licenses': expired_dispensing_licenses,
            "total_licenses": total_dispensing_subscriptions,
            "free_trials": free_dispensing_data,
            "expired_free_trials": free_expired_dispensing_data,
            "active_licenses": active_dispensing_data,
            "expired_licenses": expired_dispensing_data,
            "treatment_per_price": dispensing_per_price,  # TODO
            "treatment_per_tax": dispensing_per_tax,  # TODO
            'last_paid': dispensing_last_paid,
            'total_paid': dispensing_total_paid,
        }
        summary_data.append(resp)

        order_summary_data = []
        order_summary = Order.objects.filter(company_id=request.user.company_id)
        # ! Order summary model instance is specified by company id

        for order in order_summary.values():
            paid_sites = []
            paid_subscriptions = Subscription.objects.filter(order_id=order["id"])
            # ! model instance of paid_Subscriptions

            for subscription in paid_subscriptions.values():
                site_name = Site.objects.get(id=subscription["site_id"]).site_name
                paid_sites.append(site_name)
            no_of_paid_sites = len(paid_sites)

            amount_paid = order["amount"]/100  
            # ! multiplied by 100 on razorpay api for converting rs into paisa
            # ! payment history of site
            paid_on = order["paid_on"]
            paid_on_str = str(paid_on)
            date = paid_on_str.split(" ")[0]
            time = paid_on_str.split(" ")[1].split(".")[0]
            
            ## print(date)
            print(time)
     
            #print(time)
            # date = datetime.strptime(paid_on, "%d %b %Y  %H:%M:%S.%f")
            # print(date)


            single_order_data = {
                "paid_on_date": date,
                "paid_on_time": time,
                "paid_sites": paid_sites,
                "no_of_paid_sites": no_of_paid_sites,
                "amount_paid": amount_paid,
            }
            order_summary_data.append(single_order_data)
            # ! appending individual data

        logger.debug(order_summary_data)

        logger.info("Data\n\n{}".format(summary_data))
        context = {
            "subscription_summary": summary_data,
            "order_summary": order_summary_data
        }
        return JsonResponse(
            {"Response": {
                "Status": "success"
            },
                "Data": context
            }, safe=False, status=status.HTTP_200_OK)

    


@api_view(['GET'])
def sites_under_subscription(request, id):
    data = []
    if request.method == 'GET':
        
        # ! id collected from frontend and the sites under that particular company id are listed here
        if id == 1: 
            subscription = Subscription.objects.filter(company_id=request.user.company_id).\
                filter(is_treatment_unit=True)
        elif id == 2:
            subscription = Subscription.objects.filter(company_id=request.user.company_id).\
                filter(is_dispensing_unit=True)
        else:
            return JsonResponse(
                {"Response": {
                    "Status": "error"
                },
                    "message": "Invalid subscription type"
                }, safe=False, status=status.HTTP_200_OK)

        free_dispensing_data = []
        free_expired_dispensing_data = []
        expired_dispensing_data = []
        active_dispensing_data = []
        individual_subscription_type = ""

        for subs in subscription.values():

            site_dat = Site.objects.get(id=subs["site_id"])
            subscription_status = ""
            try:
                site_obj = Site.objects.get(id=subs["site_id"])
                site_name = site_obj.site_name
                # if site_obj.is_dispensing_unit:
                #     total_dispensing_sites += 1
                #     if site_obj.status is True:
                #         active_dispensing_sites += 1
                #     elif site_obj.status is False:
                #         expired_dispensing_sites += 1
            except Exception as e:
                site_name = ""

            if subs["subscription_code"] is None and not subs["expired"]:
                subscription_status = "free"
                free_dispensing_resp = {
                    'subscription_id': subs["id"],
                    'site_id': subs["site_id"],
                    'site_name': site_name,
                    'subscription_type': individual_subscription_type,
                    'start_date': subs["created"],
                    "valid_till": subs["valid_till"],
                    "days_to_expire": subs["days_to_expire"],
                }
                free_dispensing_data.append(free_dispensing_resp)
            elif subs["subscription_code"] is None and subs["expired"]:
                logger.info("subscription code is none and its expired and hence its expired free trial")
                # dispensing_expired_free_trials += 1
                subscription_status = "expired_free_license"
                inactive_dispensing_resp = {
                    'subscription_id': subs["id"],
                    'site_id': subs["site_id"],
                    'site_name': site_name,
                    'subscription_type': individual_subscription_type,
                    'start_date': subs["created"],
                    "valid_till": subs["valid_till"],
                    "days_to_expire": subs["days_to_expire"],
                }
                free_expired_dispensing_data.append(inactive_dispensing_resp)
            elif subs["subscription_code"] is not None and not subs["expired"]:
                subscription_status = "active"
                active_dispensing_resp = {
                    'subscription_id': subs["id"],
                    'site_id': subs["site_id"],
                    'site_name': site_name,
                    'subscription_type': individual_subscription_type,
                    'start_date': subs["created"],
                    "valid_till": subs["valid_till"],
                    "days_to_expire": subs["days_to_expire"],
                }
                active_dispensing_data.append(active_dispensing_resp)
            elif subs["subscription_code"] is not None and subs["expired"]:
                subscription_status = "expired"
                inactive_dispensing_resp = {
                    'subscription_id': subs["id"],
                    'site_id': subs["site_id"],
                    'site_name': site_name,
                    'subscription_type': individual_subscription_type,
                    'start_date': subs["created"],
                    "valid_till": subs["valid_till"],
                    "days_to_expire": subs["days_to_expire"],
                }
                expired_dispensing_data.append(inactive_dispensing_resp)

            subscription_type = ""
            per_price = 0
            per_tax = 0
            if subs["is_treatment_unit"]:
                subscription_type = "Treatment Unit"
                price = Price.objects.all()
                if price:
                    for per_rate in price.values():
                        per_price = per_rate["treatment_price"]
                        per_tax = per_rate["treatment_tax"]
            elif subs["is_dispensing_unit"]:
                subscription_type = "Dispensing Unit"
                price = Price.objects.all()
                if price:
                    for per_rate in price.values():
                        per_price = per_rate["dispensing_price"]
                        per_tax = per_rate["dispensing_tax"]

            resp = {"site_license": {
                'serial_no': subs["id"],
                "subscription_type": subscription_type,
                'site_name': site_dat.site_name,
                'start_date': subs["created"],
                "valid_till": subs["valid_till"],
                "days_to_expire": subs["days_to_expire"],
                "data_transfer_volume": subs["data_transfer_volume"],
                "no_of_actions": subs["no_of_actions"],
                "status": subscription_status,
                "free_trials": free_dispensing_data,
                "expired_free_trials": free_expired_dispensing_data,
                "active_licenses": active_dispensing_data,
                "expired_licenses": expired_dispensing_data,
                "per_price": per_price,
                "per_tax": per_tax
            },  # TODO payment summary
                "payment_details": {
                    "date_time": datetime.now(),
                    "amount": subs["total_paid"],
                    "subscription_confirmation": "success"
                }
            }

            logger.info(resp)
            data.append(resp)

        return JsonResponse(
            {"Response": {
                "Status": "success"
            },
                "Data": data
            }, safe=False, status=status.HTTP_200_OK)



@api_view(['POST'])
def razorpay_callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        logger.info(client.utility.verify_payment_signature(response_data)) # ! added to check response. REMOVE BEFORE PUSHING TO PROD
        return client.utility.verify_payment_signature(response_data)
    # ! Razorpay client verification

    if request.method == "POST":
        # ! populating as per request
        payment_id = request.data["razorpayPaymentId"]
        provider_order_id = request.data["razorpayOrderId"]
        signature_id = request.data["razorpaySignature"]

        no_of_sites = int(request.data['no_of_sites'])
        sub_sites = request.data['sub_sites']
        subscription_type = str(request.data['subscription_type']).lower()
        total_cost = request.data['total_cost']
        tax_amount = request.data['tax_amount']
        total_amount = request.data['total_amount']

        amount = total_amount * 100

        sites_array_type = type(sub_sites)
        logger.debug(sub_sites)
        logger.debug(sites_array_type)

        new_sites_array = []
        if sites_array_type is str:
            new_sites_array.append({"sitename": sub_sites})
        elif sites_array_type is list:
            new_sites_array = sub_sites

        logger.debug(new_sites_array)
        with transaction.atomic():
            try:
                
                # ! creating purchase order and creating it promptly!!!

                order = Order.objects.get(provider_order_id=provider_order_id)
                order.payment_id = payment_id
                order.signature_id = signature_id
                order.company_id = request.user.company_id
                order.save()
                order_pk = order.id
                logger.info("order id {}".format(order_pk))
                params_dict = {
                    'razorpay_order_id': provider_order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature_id
                }
                logger.info(params_dict)
                result = verify_signature(params_dict)
                # result = True
                logger.info("payment signature response {}".format(result))
                if result is not None:  # not verify_signature(params_dict)
                    try:
                        # capture the payment
                        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
                        razorpay_client.payment.capture(payment_id, amount)

                        order.payment_status = PaymentStatus.SUCCESS
                        order.save()

                        for sub_site in new_sites_array:
                            site_obj = Site.objects.get(site_name=sub_site["sitename"], 
                                                        company_id=request.user.company_id)
                            site_id = site_obj.id
                            site_obj.status = True
                            site_obj.save()
                            logger.info(site_id)
                            if subscription_type == "treatment unit":
                                existing_sub = Subscription.objects.get(site_id=site_id, is_treatment_unit=True)
                            elif subscription_type == "dispensing unit":
                                existing_sub = Subscription.objects.get(site_id=site_id, is_dispensing_unit=True)
                            else:
                                return JsonResponse(
                                    {"Response": {
                                        "Status": "error"
                                    },
                                        "message": "Invalid subscription type"
                                    }, safe=False, status=status.HTTP_200_OK)

                            start_date = datetime.today().date()
                            end_date = start_date + timedelta(days=3)
                            subscription_code = "{}_{}_{}_{}".format(request.user.company.id, site_id,
                                                                     start_date, end_date)
                            # ! subscription code is set here
                            logger.info(subscription_code)
                            existing_sub.subscription_code = subscription_code
                            existing_sub.created = start_date
                            existing_sub.valid_till = end_date
                            existing_sub.days_to_expire = 3
                            existing_sub.site_id = site_id
                            existing_sub.expired = False
                            existing_sub.total_paid = total_cost/no_of_sites
                            existing_sub.order_id = order_pk   
                            existing_sub.save()

                        logger.info("razorpay payment completed successfully")
                        return JsonResponse(
                            {"Response": {
                                "Status": "success"
                            },
                                "message": "Payment successfully completed",
                                "Data": {"payment_status": order.payment_status}
                            }, safe=False, status=status.HTTP_200_OK)
                    except Exception as err:
                        transaction.set_rollback(True)
                        logger.error("Razorpay payment failed due to error in capturing payment. {}".format(err))
                        order.payment_status = PaymentStatus.FAILURE
                        order.save()
                        return JsonResponse(
                            {"Response": {
                                "Status": "error"
                            },
                                "message": "Razorpay payment failed while capturing payment",
                                "Data": {"payment_status": order.payment_status}
                            }, safe=False, status=status.HTTP_200_OK)
                else:
                    logger.error("Razorpay payment failed due to signature verification error")
                    order.payment_status = PaymentStatus.FAILURE
                    order.save()
                    return JsonResponse(
                        {"Response": {
                            "Status": "error"
                        },
                            "message": "Razorpay payment failed due to signature verification error",
                            "Data": {"payment_status": order.payment_status}
                        }, safe=False, status=status.HTTP_200_OK)
            except Exception as err:
                transaction.set_rollback(True)
                logger.error("Error in razorpay payment, {}".format(err))
                return JsonResponse(
                    {"Response": {
                        "Status": "error"
                    },
                        "message": "Error in payment"
                    }, safe=False, status=status.HTTP_200_OK)
    else:
        # import json
        # payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        # provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
        #     "order_id"
        # )
        # order = Order.objects.get(provider_order_id=provider_order_id)
        # order.payment_id = payment_id
        # order.payment_status = PaymentStatus.FAILURE
        # order.save()
        return JsonResponse(
            {"Response": {
                "Status": "error"
            },
                "message": "Invalid method"
            }, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_sub(request):
    # ! collects data from frontEnd

    if request.method == 'POST':
        no_of_sites = int(request.data['no_of_sites'])
        sub_sites = request.data['sub_sites']
        subscription_type = str(request.data['subscription_type']).lower()
        total_cost = request.data['total_cost']
        tax_amount = request.data['tax_amount']
        total_amount = request.data['total_amount']

        amount = total_amount*100 # ! converted for the sake of razorpay

        logger.info(no_of_sites)
        logger.info(sub_sites)
        logger.info(subscription_type)

        with transaction.atomic():
            try:

                client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
                currency = "INR"
                razorpay_order = client.order.create(
                    {"amount": amount, "currency": currency, "payment_capture": "0"}
                )
                logger.debug("{}".format(razorpay_order))
                paid_user = request.user.id

                # ! creates a payment order here

                payment_order = Order.objects.create(
                    paid_user_id=paid_user, amount=amount,
                    provider_order_id=razorpay_order["id"]
                )
                payment_order.save()

                order_details = str(payment_order)
                payment_order_id = order_details.split("--")[1]
                logger.debug("payment_order_id: {}".format(payment_order_id))
                order_pk = order_details.split("--")[0]
                logger.debug("order_pk: {}".format(order_pk))

                context = {
                    "key": RAZORPAY_KEY_ID,
                    "amount": amount,
                    "currency": currency,
                    "name": request.user.username,
                    "email": request.user.email,
                    "contact": request.user.phone,
                    "description": "Test Transaction",
                    "order_id": payment_order_id,

                }
                logger.info(context)

                # for sub_site in sub_sites:
                #     site_id = Site.objects.get(site_name=sub_site["sitename"], company_id=request.user.company_id).id
                #     logger.info(site_id)
                #     if subscription_type == "treatment unit":
                #         existing_sub = Subscription.objects.get(site_id=site_id, is_treatment_unit=True)
                #     elif subscription_type == "dispensing unit":
                #         existing_sub = Subscription.objects.get(site_id=site_id, is_dispensing_unit=True)
                #     else:
                #         return JsonResponse(
                #             {"Response": {
                #                 "Status": "error"
                #             },
                #                 "message": "Invalid subscription type"
                #             }, safe=False, status=status.HTTP_200_OK)
                #
                #     start_date = datetime.today().date()
                #     end_date = start_date + timedelta(days=365)
                #     subscription_code = "{}_{}_{}_{}".format(request.user.company.id, site_id,
                #                                              start_date, end_date)
                #     logger.info(subscription_code)
                #     existing_sub.subscription_code = subscription_code
                #     existing_sub.created = start_date
                #     existing_sub.valid_till = end_date
                #     existing_sub.days_to_expire = 365
                #     existing_sub.site_id = site_id
                #     existing_sub.expired = False
                #     existing_sub.total_paid = total_cost/no_of_sites
                #     existing_sub.order_id = order_pk
                #     existing_sub.save()

                return JsonResponse(
                    {"Response": {
                        "Status": "success"
                    },
                        "Data": context
                    }, safe=False, status=status.HTTP_200_OK)
            except Exception as err:
                transaction.set_rollback(True)
                logger.error("Error in renewing subscription; {}".format(err))
                return JsonResponse(
                    {"Response": {
                        "Status": "error"
                    },
                        "message": "Error in renewing subscription"
                    }, safe=False, status=status.HTTP_200_OK)

    return JsonResponse(
        {"Response": {
            "Status": "error"
        },
            "message": "Method not allowed"
        }, safe=False, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def renew_sub(request, sub_id):
    logger.info("Subscription renew request came for subscription id {}".format(sub_id))
    if request.method == 'POST':
        no_of_sites = request.data['no_of_sites']
        site_name = request.data['site_name']
        subscription_type = request.data['sub_type']
        total_cost = request.data['total_cost']
        tax_amount = request.data['tax_amount']
        total_amount = request.data['total_amount']

        logger.info("no_of_sites {}".format(no_of_sites))
        logger.info("site_name {}".format(site_name))
        logger.info("subscription_type {}".format(subscription_type))

        existing_sub = Subscription.objects.get(id=sub_id)  # ! id from frontend
        if existing_sub.expired:
            logger.info("Selected subscription expired hence renewing")
            # print(existing_sub)
            start_date = datetime.today().date()
            end_date = start_date + timedelta(days=3)
            subscription_code = "{}_{}_{}_{}".format(request.user.company.id, sub_id,
                                                     start_date, end_date)
            logger.info("New subscription code {}".format(subscription_code))
            existing_sub.subscription_code = subscription_code
            existing_sub.created = start_date
            existing_sub.valid_till = end_date
            existing_sub.days_to_expire = 3
            existing_sub.expired = False
            existing_sub.site_id = Site.objects.get(company_id=request.user.company_id, site_name=site_name)
            existing_sub.total_paid = total_amount
            existing_sub.save()

            return JsonResponse(
                                {"Response": {
                                    "Status": "success"
                                },
                                    "message": "Subscription renewed successfully"
                                }, safe=False, status=status.HTTP_200_OK)
        else:
            logger.info("Selected subscription didn't expire hence not renewing")
            return JsonResponse(
                {"Response": {
                    "Status": "error"
                },
                    "message": "Selected subscription didn't expire"
                }, safe=False, status=status.HTTP_200_OK)
    return JsonResponse(
        {"Response": {
            "Status": "error"
        },
            "message": "Invalid request"
        }, safe=False, status=status.HTTP_400_BAD_REQUEST)


# TODO list sites and subscriptions that has free subscription or unassigned subscriptions inorder to assign from
#  frontend
@api_view(['GET'])
def list_free_or_unassigned_sites(request):
    data = []
    if request.method == 'GET':
        # TODO if null subs available & not have any free subs then create new subs to null subs with
        #  expiry date set to 365 days
        #  if null subs available & found 1 ore more free subs then ask for transfer of subs and return a flag

        if Subscription.objects.filter(subscription_code__isnull=True).count() >= 1:
            if Subscription.objects.filter(subscription_code__isnull=False).filter(days_to_expire__gte=1).count() >= 1:
                logger.info("Found one ore more valid(available) subscriptions so ask user for subscription transfer "
                      "and send null subscription list and valid subscription list")
                single_subscription = Subscription.objects.filter(Q(days_to_expire__lt=0) | Q(subscription_code__isnull=True))
                for subs in single_subscription.values():
                    # single_subscription = Subscription.objects.get(id=subs["id"])
                    site_dat = Site.objects.get(id=subs["site_id"])
                    subscription_type = "Treatment unit" if site_dat.is_treatment_unit else "Dispensing unit"
                    resp = {
                        'subscription_serial_no': subs["id"],
                        'site_serial_no': site_dat.id,
                        'site_name': site_dat.site_name,
                        'subscription_type': subscription_type,
                        'start_date': subs["created"],
                        "valid_till": subs["valid_till"],
                        "days_to_expire": subs["days_to_expire"],
                    }
                    logger.info(resp)
                    data.append(resp)
                # TODO add list of valid subs
                # single_subscription = Subscription.objects.filter(Q(days_to_expire__lt=0) | Q(subscription_code__isnull=True))
                # for subs in single_subscription.values():
                #     # single_subscription = Subscription.objects.get(id=subs["id"])
                #     site_dat = Site.objects.get(id=subs["site_id"])
                #     subscription_type = "Treatment unit" if site_dat.is_treatment_unit else "Dispensing unit"
                #     resp = {
                #         'subscription_serial_no': subs["id"],
                #         'site_serial_no': site_dat.id,
                #         'site_name': site_dat.site_name,
                #         'subscription_type': subscription_type,
                #         'start_date': subs["created"],
                #         "valid_till": subs["valid_till"],
                #         "days_to_expire": subs["days_to_expire"],
                #     }
                #     logger.info(resp)
                #     data.append(resp)
                #  set transfer flag true
                context = {"free_sites": data, "transfer": True}
                return JsonResponse(
                    {"Response": {
                        "Status": "success"
                    },
                        "Data": context
                    }, safe=False, status=status.HTTP_200_OK)
            else:
                logger.info("Couldn't find any valid(available) subscription so create new subscription for "
                      "the given free sites")
                single_subscription = Subscription.objects.filter(
                    Q(days_to_expire__lt=0) | Q(subscription_code__isnull=True))
                for subs in single_subscription.values():
                    # single_subscription = Subscription.objects.get(id=subs["id"])
                    site_dat = Site.objects.get(id=subs["site_id"])
                    subscription_type = "Treatment unit" if site_dat.is_treatment_unit else "Dispensing unit"
                    resp = {
                        'subscription_serial_no': subs["id"],
                        'site_serial_no': site_dat.id,
                        'site_name': site_dat.site_name,
                        'subscription_type': subscription_type,
                        'start_date': subs["created"],
                        "valid_till": subs["valid_till"],
                        "days_to_expire": subs["days_to_expire"],
                    }
                    # logger.info(resp)
                    data.append(resp)
                logger.info(data)
                # TODO set transfer flag false
                context = {"free_sites": data, "transfer": False}
                return JsonResponse(
                    {"Response": {
                        "Status": "success"
                    },
                        "Data": context
                    }, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse(
                {"Response": {
                    "Status": "error"
                },
                    "message": "Couldn't find any free sites"
                }, safe=False, status=status.HTTP_200_OK)

    else:
        return JsonResponse(
            {"Response": {"Status": "error"}, "message": "Invalid request"},
            safe=False, status=status.HTTP_400_BAD_REQUEST)
    






# @api_view(['POST'])
# def add_sub(request):
#     if request.method == 'POST':
#         no_of_sites = request.data['no_of_sites']
#         sub_sites = request.data['sub_sites']
#         subscription_type = request.data['subscription_type']
#         total_cost = request.data['total_cost']
#         tax_amount = request.data['tax_amount']
#         total_amount = request.data['total_amount']
#
#         logger.info(no_of_sites)
#         logger.info(sub_sites)
#         logger.info(subscription_type)
#         for sub_site in sub_sites:
#             sub_detail = sub_site.split(",")
#             logger.info(sub_detail)
#             existing_sub = Subscription.objects.get(id=sub_detail[1])
#             # print(existing_sub)
#             start_date = datetime.today().date()
#             end_date = start_date + timedelta(days=365)
#             subscription_code = "{}_{}_{}_{}".format(request.user.company.id, sub_detail[1],
#                                                      start_date, end_date)
#             logger.info(subscription_code)
#             existing_sub.subscription_code = subscription_code
#             existing_sub.created = start_date
#             existing_sub.valid_till = end_date
#             existing_sub.days_to_expire = 365
#             existing_sub.site_id = sub_detail[0]
#             existing_sub.expired = False
#             existing_sub.total_paid = total_cost/no_of_sites
#             existing_sub.save()
#
#         # if request.method == "POST":
#         #     name = request.POST.get("name")
#         #     amount = request.POST.get("amount")
#         #     client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
#         #     razorpay_order = client.order.create(
#         #         {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
#         #     )
#         #     order = Order.objects.create(
#         #         subscription_id=sub_detail[1], amount=amount, provider_order_id=razorpay_order["id"]
#         #     )
#         #     order.save()
#         #     return render(
#         #         request,
#         #         "payment.html",
#         #         {
#         #             "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
#         #             "razorpay_key": RAZORPAY_KEY_ID,
#         #             "order": order,
#         #         },
#         #     )
#         # return render(request, "payment.html")
#
#
#                 # existing_sub.subscription_code = "{}_{}_{}".format(request.user.company.id, start_date, end_date)
#             # no_of_sites = request.data['no_of_sites']
#             # total_cost = request.data['total_cost']
#             # tax_amount = request.data['tax_amount']
#             # total_amount = request.data['total_amount']
#             #
#             # subscription = Subscription()
#             # if str(subscription_type).lower() == "treatment unit":
#             #     subscription.is_treatment_unit = True
#             # elif str(subscription_type).lower() == "dispensing unit":
#             #     subscription.is_dispensing_unit = True
#             #
#             # subscription.no_of_sites = no_of_sites
#             # subscription.total_cost = total_cost
#             # # subscription.tax_amount = tax_amount
#             # subscription.total_paid = total_amount
#             # subscription.save()
#
#             # TODO get site type from mqtt after authentication
#             # site_type = "Treatment"
#             # subscription_type = site_type
#             #
#             # if site_type == "Dispensing":
#             #     site_dat.is_dispensing_unit = True
#             # elif site_type == "Treatment":
#             #     site_dat.is_treatment_unit = True
#             #
#             # site_dat.save()
#             #
#             # site_obj = Site.objects.get(site_name=site_name)
#             #
#             # subscription_data = Subscription()
#             # subscription_data.site = site_obj
#             # if str(subscription_type).lower() == "treatment":
#             #     subscription_data.is_treatment_unit = True
#             # elif str(subscription_type).lower() == "dispensing":
#             #     subscription_data.is_dispensing_unit = True
#             #
#             # subscription_data.save()
#
#         # no_of_sites = request.data['no_of_sites']
#         # no_of_sites = request.data['no_of_sites']
#
#         # TODO check no of sites == no of subs else return cannot add subs more than sites
#         # TODO check if the subscription category and sites types match
#         # TODO if true then add a unique subscription code with format companyname_startdate_enddate
#         # free_subscription = request.data['free_subs']
#         # for subs in free_subscription:
#         #     logger.info(subs)
#         #     existing_sub = Subscription.objects.get(id=subs["subscription_serial_no"])
#         #     start_date = datetime.today().date()
#         #     end_date = start_date + timedelta(days=365)
#         #     subscription_code = "{}_{}_{}_{}".format(request.user.company.id, subs["subscription_serial_no"],
#         #                                              start_date, end_date)
#         #     logger.info(subscription_code)
#         #     existing_sub.subscription_code = subscription_code
#         #     existing_sub.created = start_date
#         #     existing_sub.valid_till = end_date
#         #     existing_sub.days_to_expire = 365
#         #     # existing_sub.site_id = site_id
#         #     existing_sub.save()
#         #     # existing_sub.subscription_code = "{}_{}_{}".format(request.user.company.id, start_date, end_date)
#         # # no_of_sites = request.data['no_of_sites']
#         # # total_cost = request.data['total_cost']
#         # # tax_amount = request.data['tax_amount']
#         # # total_amount = request.data['total_amount']
#         # #
#         # # subscription = Subscription()
#         # # if str(subscription_type).lower() == "treatment unit":
#         # #     subscription.is_treatment_unit = True
#         # # elif str(subscription_type).lower() == "dispensing unit":
#         # #     subscription.is_dispensing_unit = True
#         # #
#         # # subscription.no_of_sites = no_of_sites
#         # # subscription.total_cost = total_cost
#         # # # subscription.tax_amount = tax_amount
#         # # subscription.total_paid = total_amount
#         # # subscription.save()
#         #
#         # # TODO get site type from mqtt after authentication
#         # # site_type = "Treatment"
#         # # subscription_type = site_type
#         # #
#         # # if site_type == "Dispensing":
#         # #     site_dat.is_dispensing_unit = True
#         # # elif site_type == "Treatment":
#         # #     site_dat.is_treatment_unit = True
#         # #
#         # # site_dat.save()
#         # #
#         # # site_obj = Site.objects.get(site_name=site_name)
#         # #
#         # # subscription_data = Subscription()
#         # # subscription_data.site = site_obj
#         # # if str(subscription_type).lower() == "treatment":
#         # #     subscription_data.is_treatment_unit = True
#         # # elif str(subscription_type).lower() == "dispensing":
#         # #     subscription_data.is_dispensing_unit = True
#         # #
#         # # subscription_data.save()
#
#         return JsonResponse(
#                             {"Response": {
#                                 "Status": "success"
#                             },
#                                 "message": "added subscription details"
#                             }, safe=False, status=status.HTTP_200_OK)
#     return JsonResponse(
#         {"Response": {
#             "Status": "error"
#         },
#             "message": "Invalid request"
#         }, safe=False, status=status.HTTP_400_BAD_REQUEST)


# {"free_subs": [
#                 {
#                     "subscription_serial_no": 20,
#                     "site_serial_no": 14,
#                     "site_name": "Site5",
#                     "subscription_type": "Dispensing unit",
#                     "start_date": "2022-09-05",
#                     "valid_till": "2022-10-05",
#                     "days_to_expire": 28
#                 },
#                 {
#                     "subscription_serial_no": 21,
#                     "site_serial_no": 15,
#                     "site_name": "Site6",
#                     "subscription_type": "Treatment unit",
#                     "start_date": "2022-09-05",
#                     "valid_till": "2022-10-05",
#                     "days_to_expire": 28
#                 }
#             ]}


# @api_view(['POST'])
# def add_sub(request):
#     if request.method == 'POST':
#         # TODO check if the subscription category and sites types match
#         # TODO if true then add a unique subscription code with format companyname_startdate_enddate
#         subscription_type = request.data['subscription_type']
#         no_of_sites = request.data['no_of_sites']
#         total_cost = request.data['total_cost']
#         tax_amount = request.data['tax_amount']
#         total_amount = request.data['total_amount']
#
#         subscription = Subscription()
#         if str(subscription_type).lower() == "treatment unit":
#             subscription.is_treatment_unit = True
#         elif str(subscription_type).lower() == "dispensing unit":
#             subscription.is_dispensing_unit = True
#
#         subscription.no_of_sites = no_of_sites
#         subscription.total_cost = total_cost
#         # subscription.tax_amount = tax_amount
#         subscription.total_paid = total_amount
#         subscription.save()
#
#         # TODO get site type from mqtt after authentication
#         # site_type = "Treatment"
#         # subscription_type = site_type
#         #
#         # if site_type == "Dispensing":
#         #     site_dat.is_dispensing_unit = True
#         # elif site_type == "Treatment":
#         #     site_dat.is_treatment_unit = True
#         #
#         # site_dat.save()
#         #
#         # site_obj = Site.objects.get(site_name=site_name)
#         #
#         # subscription_data = Subscription()
#         # subscription_data.site = site_obj
#         # if str(subscription_type).lower() == "treatment":
#         #     subscription_data.is_treatment_unit = True
#         # elif str(subscription_type).lower() == "dispensing":
#         #     subscription_data.is_dispensing_unit = True
#         #
#         # subscription_data.save()
#
#         return JsonResponse(
#                             {"Response": {
#                                 "Status": "success"
#                             },
#                                 "message": "added subscription details"
#                             }, safe=False, status=status.HTTP_200_OK)
#     return JsonResponse(
#         {"Response": {
#             "Status": "error"
#         },
#             "message": "Invalid request"
#         }, safe=False, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def add_sub(request):
#     if request.method == 'POST':
#         no_of_sites = request.data['no_of_sites']
#         sub_sites = request.data['sub_sites']
#         subscription_type = request.data['subscription_type']
#         total_cost = request.data['total_cost']
#         tax_amount = request.data['tax_amount']
#         total_amount = request.data['total_amount']
#
#         amount = total_amount
#
#         logger.info(no_of_sites)
#         logger.info(sub_sites)
#         logger.info(subscription_type)
#         with transaction.atomic():
#             try:
#
#                 client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
#                 currency = "INR"
#                 razorpay_order = client.order.create(
#                     {"amount": amount, "currency": currency, "payment_capture": "1"}
#                 )
#                 logger.debug("{}".format(razorpay_order))
#                 paid_user = request.user.id
#                 payment_order = Order.objects.create(
#                     paid_user_id=paid_user, amount=amount,
#                     provider_order_id=razorpay_order["id"]
#                 )
#                 payment_order.save()
#
#                 order_details = str(payment_order)
#                 payment_order_id = order_details.split("--")[1]
#                 logger.debug("payment_order_id: {}".format(payment_order_id))
#                 order_pk = order_details.split("--")[0]
#                 logger.debug("order_pk: {}".format(order_pk))
#
#                 context = {
#                     "key": RAZORPAY_KEY_ID,
#                     "amount": amount,
#                     "currency": currency,
#                     "name": request.user.username,
#                     "email": request.user.email,
#                     "contact": request.user.phone,
#                     "description": "Test Transaction",
#                     "order_id": payment_order_id,
#
#                 }
#                 logger.info(context)
#
#                 for sub_site in sub_sites:
#                     sub_detail = sub_site.split(",")
#                     logger.info(sub_detail)
#                     existing_sub = Subscription.objects.get(id=sub_detail[1])
#                     start_date = datetime.today().date()
#                     end_date = start_date + timedelta(days=365)
#                     subscription_code = "{}_{}_{}_{}".format(request.user.company.id, sub_detail[1],
#                                                              start_date, end_date)
#                     logger.info(subscription_code)
#                     existing_sub.subscription_code = subscription_code
#                     existing_sub.created = start_date
#                     existing_sub.valid_till = end_date
#                     existing_sub.days_to_expire = 365
#                     existing_sub.site_id = sub_detail[0]
#                     existing_sub.expired = False
#                     existing_sub.total_paid = total_cost/no_of_sites
#                     existing_sub.order_id = order_pk
#                     existing_sub.save()
#
#                 return JsonResponse(
#                     {"Response": {
#                         "Status": "success"
#                     },
#                         "Data": context
#                     }, safe=False, status=status.HTTP_200_OK)
#             except Exception as err:
#                 transaction.set_rollback(True)
#                 logger.error("Error in renewing subscription; {}".format(err))
#                 return JsonResponse(
#                     {"Response": {
#                         "Status": "error"
#                     },
#                         "message": "Error in renewing subscription"
#                     }, safe=False, status=status.HTTP_200_OK)
#
#     return JsonResponse(
#         {"Response": {
#             "Status": "error"
#         },
#             "message": "Method not allowed"
#         }, safe=False, status=status.HTTP_403_FORBIDDEN)


















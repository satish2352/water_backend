import re
import os
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.authtoken.models import Token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from iwater.models import User, Company,Site,SitePermission

from iwater.iw_logger import logger
from init_water_app.settings import OTP_VALID_FOR

from django.shortcuts import redirect
from django.urls import reverse
email=''
# email=''

@api_view(['POST'])
def user_login(request):
    logger.info("Login request")
    logger.info("User before  login {}".format(request.user))
    if request.method == 'POST':

        login_type = request.data['login_type']
        if login_type == "email":
            global email
            logger.info("Email based login")
            email = request.data['email']

            password = request.data['password']
            logger.info("Email: {},".format(email))
            user = authenticate(request, email=email, password=password)
            logger.info("Logged in user is {}".format(user))
            
          
            
            if user is not None:

                

                if user.is_active:
                    login(request, user)
                    logged_user = User.objects.get(email=email)
                    sitefinder=logged_user.company_id
                    sits=Site.objects.filter(company_id=sitefinder)
                    company_name = Company.objects.get(id=logged_user.company_id)
                    userfinder=logged_user.id
                    # user_id=SitePermission.objects.get(id=
                    if sits:
                        for site in sits:
                            sitename=site.site_name
                    else:
                        sitename=''
                        # company_id_new=''
                    if user.is_blocked:
                        if request.path != reverse('blocked'):
                            return redirect('blocked')
            
                    # Block ends

                    role = ""
                    if logged_user.is_super_admin:
                        role = "super_admin"
                    elif logged_user.is_admin:
                        role = "administrator"
                    elif logged_user.is_supervisor:
                        role = "supervisor"
                    elif logged_user.is_operator:
                        role = "operator"

                    user_data = {
                        "user": {
                            'serial_no': logged_user.id,
                            'creation_date': logged_user.date_joined,
                            'username': logged_user.username,
                            'user_role': role,
                            'email': logged_user.email,
                            'contact_no': logged_user.phone,
                            'site_name':sitename,
                            'company_name':company_name.company_name,
                            'company_id':company_name[0].id,
                            'user_id':userfinder
                        }
                    }
                    if role == "super_admin":
                        company_details = Company.objects.get(id=logged_user.company_id)
                        user_data["user"]["company_name"] = company_details.company_name
                        user_data["user"]["company_id"] = company_name[0].id,
                        user_data["user"]["gst_no"] = company_details.gst_no
                        user_data["user"]["address1"] = company_details.address1
                        user_data["user"]["address2"] = company_details.address2
                        user_data["user"]["city"] = company_details.city
                        user_data["user"]["state"] = company_details.state
                        user_data["user"]["pincode"] = company_details.pincode
                    logger.info(user_data)
                    token, created = Token.objects.get_or_create(user=user)
                    token = {'token': token.key}
                    logger.info(token)
                    user_data.update(token)
                    logger.info(user_data)
                    return JsonResponse({"Response": {
                        "Status": "status"},
                        "Data": user_data
                    }, safe=False, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"Response": {
                        "Status": "error"},
                        "message": "The company account is deleted or the user is blocked. Please contact admin"
                    }, safe=False, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"Response": {
                    "Status": "error"},
                    "message": "Invalid mail id or password"
                }, safe=False, status=status.HTTP_200_OK)
        elif login_type == "phone":
            logger.info("OTP based login")
            phone_country = "+91"
            mob = re.sub(r"\D", "", request.data['phone'])
            phone = phone_country + str(mob)
            logger.info("phone {}".format(phone))
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                user = None
            # print(user)
            logger.info("User with phone {}".format(user))
            if user is not None:
                user = User.objects.get(phone=phone)
                sent = user.send_login_sms()
                # logger.info(sent)
                if sent["status"]:
                    logger.info("Sent otp")
                    return JsonResponse({"Response": {"Status": "success"},
                                         "message": "OTP sent to the registered number",
                                         "valid_for": OTP_VALID_FOR,
                                         "otp": "{}".format(sent["otp"]),
                                         "Data": {'uid': urlsafe_base64_encode(force_bytes(user.id))}
                                         # TODO remove
                                         },
                                        safe=False, status=status.HTTP_200_OK)

                elif sent["status"] is False:
                    response = {"Response": {
                        "Status": "success"},
                        "message": "Phone number is not verified. Please accept the invitation sent to your mobile number",
                    }
                    logger.info(response)
                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
                else:
                    response = {"Response": {
                        "Status": "error"},
                        "message": "Error in sending OTP",
                    }
                    logger.info(response)
                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            else:
                response = {"Response": {
                    "Status": "error"},
                    "message": "You are not registered with this phone number",
                }
                logger.info(response)
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"Response": {
                "Status": "error"},
                "message": "Invalid login type"
            }, safe=False, status=status.HTTP_200_OK)

    response = {"Response": {"Status": "error"}, "message": "Method {} not allowed".format(request.method)}
    return JsonResponse(response, safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def otp_login(request, uidb64):
    logger.info("OTP based login request")
    if request.method == 'POST':
        code = request.data['otpnumber']

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            logger.info("Got user id as {}".format(uid))
        except (TypeError, ValueError, OverflowError):
            logger.info("OTP Login: invalid user id")
            response = {"Response": {"Status": "error"}, "message": "Login failed. Invalid OTP"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        try:
            logger.info("Getting user details")
            user_obj = User.objects.get(id=uid)
            if not user_obj.phone:
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "Login failed. No phone number is provided"},
                                    safe=False, status=status.HTTP_200_OK)

            if user_obj.verify_otp(code)["status"]:
                if user_obj is not None:
                    if user_obj.is_active:
                        login(request, user_obj)
                        logged_user = User.objects.get(id=uid)
                        logger.info("User after logged in {}".format(logged_user.username))
                        role = ""
                        if logged_user.is_super_admin:
                            role = "super_admin"
                        elif logged_user.is_admin:
                            role = "administrator"
                        elif logged_user.is_supervisor:
                            role = "supervisor"
                        elif logged_user.is_operator:
                            role = "operator"

                        user_data = {
                            "user": {
                                'serial_no': logged_user.id,
                                'creation_date': logged_user.date_joined,
                                'username': logged_user.username,
                                'user_role': role,
                                'email': logged_user.email,
                                'contact_no': logged_user.phone
                            }
                        }
                        if role == "super_admin":
                            company_details = Company.objects.get(id=logged_user.company_id)
                            user_data["user"]["company_name"] = company_details.company_name
                            user_data["user"]["gst_no"] = company_details.gst_no
                            user_data["user"]["address1"] = company_details.address1
                            user_data["user"]["address2"] = company_details.address2
                            user_data["user"]["city"] = company_details.city
                            user_data["user"]["state"] = company_details.state
                            user_data["user"]["pincode"] = company_details.pincode
                        logger.info(user_data)
                        token, created = Token.objects.get_or_create(user=user_obj)
                        token = {'token': token.key}
                        logger.info(token)
                        user_data.update(token)
                        return JsonResponse({"Response": {
                            "Status": "status"},
                            "message": "OTP verified successfully",
                            "Data": user_data
                        }, safe=False, status=status.HTTP_200_OK)
                    else:
                        return JsonResponse({"Response": {
                            "Status": "error"},
                            "message": "Login failed. The company account is deleted or the user is blocked. "
                                       "Please contact admin"
                        }, safe=False, status=status.HTTP_200_OK)

            logger.info("Login failed. Invalid otp or otp expired")
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Login failed. Invalid or expired OTP"},
                                safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist as err:
            logger.error("Login failed. Couldn't find the requested User, {}".format(err))
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Login failed. Couldn't find the requested user"},
                                safe=False, status=status.HTTP_200_OK)

    response = {"Response": {"Status": "error"}, "message": "Method {} not allowed".format(request.method)}
    return JsonResponse(response, safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def user_logout(request):
    logger.info("Logged in user is {}".format(request.user))
    logout(request)
    logger.info("Logged out and now user is {}".format(request.user))

    return JsonResponse({"Response": {
        "Status": "success"},
        "message": "User logged out successfully"
    }, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def user_registration(request):
    logger.info("-----------------")
    logger.info("user signup")
    if request.method == 'POST':
        email_signup = False
        email = None
        phone = None
        try:
            username = request.data['username']
            try:
                email = request.data['email'] if request.data['email'] else None
                logger.info("email {}".format(email))
                if email is not None:
                    email_signup = True
                try:
                    if User.objects.get(email=email) and email is not None:
                        response = {"Response": {"Status": "error"},
                                    "message": "The email address is already used for registration"}
                        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    pass
            except:
                pass

            try:
                phone_country = "+91"
                mob = re.sub(r"\D", "", request.data['phone'])
                phone = phone_country + str(mob)
                logger.info("mob {}".format(mob))
                try:
                    User.objects.get(phone=phone)
                    response = {"Response": {"Status": "error"},
                                "message": "The phone number is already used for registration"}
                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    pass
            except:
                pass

            company_name = request.data['company']
            address1 = request.data['address1']
            address2 = request.data['address2']
            city = request.data['city']
            pincode = request.data['pincode']
            if len(str(pincode)) > 6:
                response = {"Response": {"Status": "error"}, "message": "Invalid pincode, "
                                                                        "Pincode length should be 6"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            state = request.data['state']
            gst_no = request.data['gstno']
        except Exception as e:
            logger.error("Signup: Error in getting user info: {}".format(e))
            response = {"Response": {"Status": "error"}, "message": "Error in getting user info; {}".format(e)}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        if username.startswith('__'):
            response = {"Response": {"Status": "error"}, "message": "Username not allowed"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        try:
            User.objects.get(username=username)
            response = {"Response": {"Status": "error"}, "message": "The username is already taken"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        with transaction.atomic():
            try:
                company = Company.objects.get(company_name=company_name, gst_no=gst_no, pincode=pincode)
                admin_count_in_company = User.objects.filter(company_id=company, is_super_admin=True).count()
                logger.info("Admin count in company is {}".format(admin_count_in_company))
                if admin_count_in_company > 0:
                    logger.info("Signup: Already a super admin is registered in the company \"{}\". "
                                "Only one super admin per company is allowed".format(company_name))
                    response = {"Response": {"Status": "error"},
                                "message": "Only one super admin per company is allowed"}
                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            except Company.DoesNotExist:
                try:
                    company = Company()
                    company.company_name = company_name
                    company.address1 = address1
                    company.address2 = address2
                    company.city = city
                    company.pincode = pincode
                    company.state = state
                    company.gst_no = gst_no
                    company.save()
                    logger.info("Signup: successfully added company info to db")
                except Exception as err:
                    transaction.set_rollback(True)
                    logger.info("Signup: Error in adding company info to db: {}".format(err))
                    response = {"Response": {"Status": "error"}, "message": "Error in adding "
                                                                            "company info to db: {}".format(err)}
                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            try:
                # Add admin user to database
                super_admin_user = User()
                super_admin_user.username = username
                if email_signup:
                    logger.info("email signup")
                    super_admin_user.email = email
                else:
                    logger.info("sms signup")
                    super_admin_user.phone = phone  # phone_country + phone

                super_admin_user.is_super_admin = True
                super_admin_user.company = company
                super_admin_user.save()


                # Send welcome and verification email  # TODO get from env file
                brand_name = "Initiative Water"
                # support_email = "support@initiative.com"
                support_email = "dotnet_dev@initiativewater.com"
                # support_phone = "+919569690292"
                support_phone = "+919607007015"

                if email is not None:
                    logger.info("sending mail to the registered email")
                    #super_admin_user.send_set_password_email(get_current_site(request).domain, brand_name, support_email,
                    #                                     support_phone)          #commented by bharti
                    super_admin_user.send_set_password_email(os.environ.get("SITE_DOMAIN"), brand_name, support_email,
                                                         support_phone)           #added by bharti 
                if phone is not None:
                    logger.info("sending sms to the registered phone")
#below three lines commented by bharti 
#                   super_admin_user.send_invite_sms(get_current_site(request).domain, brand_name, 
#                                                             support_email,
#                                                           support_phone)
 #below three lines added by bharti                   
                    ##############This comment for stop registering by using sms.########################
                    #####################################################################################
                    # super_admin_user.send_invite_sms(get_current_site(request).domain, brand_name,support_email, support_phone)
                    ####################################################################################
                    
                    
                    # super_admin_user.send_invite_sms(os.environ.get("SITE_DOMAIN"), brand_name,support_email, support_phone)
                    #super_admin_user.send_invite_sms()

                response = {"Response": {"Status": "success"}, "message": "User created successfully"}

                logger.info("Signup: successfully added user info to db")
            except Exception as e:
                transaction.set_rollback(True)
                logger.info("Signup: Error in adding user info to db: {}".format(e))
                response = {"Response": {"Status": "error"}, "message": "Error in adding user info to db: {}".format(e)}
                return JsonResponse(response, safe=False, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def update_user_registration(request, pk):
    if not request.user.is_super_admin:
        response = {"Response": {
                    "Status": "error"},
                    "message": "You are not authorized to update user details"}
        return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        try:
            address1 = request.data['address1']
            address2 = request.data['address2']
            city = request.data['city']
            pincode = request.data['pincode']
            if len(str(pincode)) > 6:
                response = {"Response": {"Status": "error"}, "message": "Invalid pincode, "
                                                                        "Pincode length should be 6"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            state = request.data['state']
            gst_no = request.data['gstno']
        except Exception as e:
            logger.error("Super admin update: Error in getting company info: {}".format(e))
            response = {"Response": {"Status": "error"}, "message": "Error in getting company info; {}".format(e)}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        with transaction.atomic():
            try:
                user = User.objects.get(id=pk)
                company = Company.objects.get(id=user.company_id)
                company.address1 = address1
                company.address2 = address2
                company.city = city
                company.pincode = pincode
                company.state = state
                company.gst_no = gst_no
                company.save()
                logger.info("Super admin update: successfully updated company info")

            except Exception as err:
                transaction.set_rollback(True)
                logger.info("Super admin update: Error in updating company info: {}".format(err))
                response = {"Response": {"Status": "error"}, "message": "Error in updating "
                                                                        "company info"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        new_user = User.objects.get(id=pk)

        role = ""
        if new_user.is_super_admin:
            role = "super_admin"

        company_details = Company.objects.get(id=new_user.company_id)

        user_data = {
            "user": {
                "serial_no": new_user.id,
                "creation_date": new_user.date_joined,
                "username": new_user.username,
                "user_role": role,
                "email": new_user.email,
                "contact_no": new_user.phone,
                "company_name": company_details.gst_no,
                "gst_no": company_details.gst_no,
                "address1": company_details.address1,
                "address2": company_details.address2,
                "city": company_details.city,
                "state": company_details.state,
                "pincode": company_details.pincode,
                }
        }

        logger.info(user_data)

        response = {"Response": {
            "Status": "success"},
            "message": "Company details updated successfully",
            "Data": user_data
        }
        return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)

    response = {"Response": {"Status": "error"}, "message": "Method {} not allowed".format(request.method)}
    return JsonResponse(response, safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_user_to_verify(request, uidb64, token):
    logger.info("User is {}".format(request.user))
    logger.info("Verifying user")

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        logger.info(uid)
    except (TypeError, ValueError, OverflowError):
        logger.info("User verification: invalid user id")
        response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    if request.method == 'GET':

        try:
            user = User.objects.get(pk=uid)
            if user is not None and not user.is_link_expired():
                data = {"username": user.username, "email": user.email, "company_name": user.company.company_name,
                        "phone": user.phone}
                # logger.info("User verification: was success")
                response = {"Response": {"Status": "success"}, "Data": data}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            else:
                response = {"Response": {"Status": "error"}, "message": "Invalid verification link or link expired"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.info("User verification: couldn't find the user")
            response = {"Response": {"Status": "error"}, "message": "Invalid verification link or link expired"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    response = {"Response": {"Status": "error"}, "message": "Method {} not allowed".format(request.method)}
    return JsonResponse(response, safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def forgot_password(request,):
    logger.info("User is {}".format(request.user))
    logger.info("forgot password")

    if request.method == 'POST':
        username = request.data['username']
        email = request.data['email']
        try:
            user = User.objects.get(username=username)
            logger.info(user.email)
            if user.email_verified is False:
                response = {"Response": {"Status": "error"}, "message": "User email is not verified"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            if user is not None and user.email == email and user.email_verified is True:
                super_user = User.objects.get(company_id=user.company_id, is_super_admin=True)
                logger.info(super_user)
                brand_name = Company.objects.get(id=user.company_id).company_name
                support_email = super_user.email
                support_phone = super_user.phone
                #print(os.environ.get("SITE_DOMAIN"))           
                #print("This is for testing site domain")      
                user.set_password_email(os.environ.get("SITE_DOMAIN"), brand_name, support_email, support_phone)
                response = {"Response": {"Status": "success"}, "message": "Email sent to the user"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

            response = {"Response": {"Status": "error"}, "message": "Invalid user"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except Exception as err:
            logger.error("Forgot password: Error; {}".format(err))
            response = {"Response": {"Status": "error"}, "message": "Error in getting user details"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def change_password(request, uidb64, token):
    logger.info("User is {}".format(request.user))
    logger.info("Verifying user")

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError):
        logger.info("User verification: invalid user id")
        response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    if request.method == 'POST':
        password = request.data['password']
        password2 = request.data['confirmpassword']

        if password != password2:
            response = {"Response": {"Status": "error"}, "message": "Password mismatch"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        try:
            logger.info(uid)
            user = User.objects.get(pk=uid)
            logger.info(user)
            if user is not None and user.verify_email(token):
                user.set_password(password)
                user.email_verified = True
                user.save()
            else:
                response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.info("User verification: couldn't find the user")
            response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        logger.info("User verification: was success")
        response = {"Response": {"Status": "success"}, "message": "User verification and password update done"}
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    response = {"Response": {"Status": "error"}, "message": "Method {} not allowed".format(request.method)}
    return JsonResponse(response, safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def user_invite(request, uidb64, token):
    logger.info("User is {}".format(request.user))
    logger.info("Verifying user")

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError):
        logger.info("User verification: invalid user id")
        response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    if request.method == 'POST':
        invitation = request.data["invitation"]

        if invitation == "accept":
            # send otp
            logger.info("User accepted invite")
            try:
                logger.info(uid)
                user = User.objects.get(pk=uid)
                user.invite_rejected = False
                user.is_active = True
                # user.phone_verified = True --- for later1808_l
                user.save()
                logger.info(user)
                if user is not None:
                    sent = user.send_verification_sms()
                    if sent["status"]:
                        return JsonResponse({"Response": {"Status": "success"},
                                             "message": "OTP sent to the registered number",
                                             "valid_for": OTP_VALID_FOR,
                                             "uidb64": uidb64,
                                             "token": token,
                                             "otp": sent["otp"]
                                             },
                                            safe=False, status=status.HTTP_200_OK)
                    else:
                        response = {"Response": {"Status": "success"}, "message": "Phone number is already verified"}
                        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
                else:
                    response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                logger.info("User verification: couldn't find the user")
                response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        elif invitation == "reject":
            # user status as rejected
            logger.info("User rejected invite")

            try:
                logger.info(uid)
                user = User.objects.get(pk=uid)
                logger.info(user)
                if user is not None:
                    user.invite_rejected = True
                    user.is_active = False
                    user.save()
                    response = {"Response": {"Status": "success"}, "message": "Rejected your invite"}
                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
                logger.info("User verification: couldn't find the user")
                response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                logger.info("User verification: couldn't find the user")
                response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        else:
            logger.info("User verification: Invalid invitation type")
            response = {"Response": {"Status": "error"}, "message": "Invalid verification type"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    else:
        response = {"Response": {"Status": "error"}, "message": "Method {} not allowed".format(request.method)}
        return JsonResponse(response, safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def verify_user_otp(request, uidb64, token):

    if request.method == 'POST':
        code = request.data['otpnumber']
        # uid = request.data['uid']

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
        except (TypeError, ValueError, OverflowError):
            logger.info("User verification: invalid user id")
            response = {"Response": {"Status": "error"}, "message": "Invalid verification link"}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        try:
            user_obj = User.objects.get(id=uid)
            if not user_obj.phone:
                return JsonResponse({"Response": {"Status": "error"},
                                     "message": "Verification failed. No phone number is provided"},
                                    safe=False, status=status.HTTP_200_OK)

            if user_obj.verify_phone(code)["status"]:
                super_user = User.objects.get(company_id=user_obj.company_id, is_super_admin=True)
                logger.info(super_user)
                brand_name = Company.objects.get(id=user_obj.company_id).company_name
                support_email = super_user.email
                support_phone = super_user.phone
                user_obj.set_password_email(get_current_site(request).domain, brand_name, support_email, support_phone)
                return JsonResponse({"Response": {"Status": "success"},
                                     "message": "OTP verified successfully",
                                     "Data": {"uidb64": uidb64, "token": token}},
                                    safe=False, status=status.HTTP_200_OK)

            logger.info("Verification failed. Invalid otp or otp expired")
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Verification failed. Invalid or expired OTP"},
                                safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist as err:
            return JsonResponse({"Response": {"Status": "error"},
                                 "message": "Couldn't find the requested user, {}".format(err)},
                                safe=False, status=status.HTTP_200_OK)


# @api_view(['POST'])  latest
# def user_login(request):
#     logger.info("Login request")
#     logger.info("User before  login {}".format(request.user))
#     if request.method == 'POST':
#
#         login_type = request.data['login_type']
#         if login_type == "email":
#             logger.info("Email based login")
#             email = request.data['email']
#             password = request.data['password']
#             logger.info("Email: {},".format(email))
#             user = authenticate(request, email=email, password=password)
#             logger.info("Logged in user is {}".format(user))
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     logged_user = User.objects.get(email=email)
#
#                     role = ""
#                     if logged_user.is_super_admin:
#                         role = "super_admin"
#                     elif logged_user.is_admin:
#                         role = "administrator"
#                     elif logged_user.is_supervisor:
#                         role = "supervisor"
#                     elif logged_user.is_operator:
#                         role = "operator"
#
#                     user_data = {
#                         "user": {
#                             'serial_no': logged_user.id,
#                             'creation_date': logged_user.date_joined,
#                             'username': logged_user.username,
#                             'user_role': role,
#                             'email': logged_user.email,
#                             'contact_no': logged_user.phone
#                         }
#                     }
#                     if role == "super_admin":
#                         company_details = Company.objects.get(id=logged_user.company_id)
#                         user_data["user"]["company_name"] = company_details.company_name
#                         user_data["user"]["gst_no"] = company_details.gst_no
#                         user_data["user"]["address1"] = company_details.address1
#                         user_data["user"]["address2"] = company_details.address2
#                         user_data["user"]["city"] = company_details.city
#                         user_data["user"]["state"] = company_details.state
#                         user_data["user"]["pincode"] = company_details.pincode
#                     logger.info(user_data)
#                     token, created = Token.objects.get_or_create(user=user)
#                     token = {'token': token.key}
#                     logger.info(token)
#                     user_data.update(token)
#                     logger.info(user_data)
#                     return JsonResponse({"Response": {
#                         "Status": "status"},
#                         "Data": user_data
#                     }, safe=False, status=status.HTTP_200_OK)
#                 else:
#                     return JsonResponse({"Response": {
#                         "Status": "error"},
#                         "message": "The company account is deleted or the user is blocked. Please contact admin"
#                     }, safe=False, status=status.HTTP_200_OK)
#             else:
#                 return JsonResponse({"Response": {
#                     "Status": "error"},
#                     "message": "Invalid mail id or password"
#                 }, safe=False, status=status.HTTP_200_OK)
#         elif login_type == "phone":
#             logger.info("OTP based login")
#             phone_country = "+91"
#             mob = re.sub(r"\D", "", request.data['phone'])
#             phone = phone_country + str(mob)
#             logger.info("phone {}".format(phone))
#             try:
#                 user = User.objects.get(phone=phone)
#             except User.DoesNotExist:
#                 user = None
#             # print(user)
#             logger.info("User with phone {}".format(user))
#             if user is not None:
#                 user = User.objects.get(phone=phone)
#                 sent = user.send_login_sms()
#                 # logger.info(sent)
#                 if sent["status"]:
#                     logger.info("Sent otp")
#                     return JsonResponse({"Response": {"Status": "success"},
#                                          "message": "OTP sent to the registered number",
#                                          "valid_for": OTP_VALID_FOR,
#                                          "otp": "{}".format(sent["otp"]),
#                                          "Data": {'uid': urlsafe_base64_encode(force_bytes(user.id))}
#                                          # TODO remove
#                                          },
#                                         safe=False, status=status.HTTP_200_OK)
#
#                 elif sent["status"] is False:
#                     response = {"Response": {
#                         "Status": "success"},
#                         "message": "Phone number is not verified. Please accept the invitation sent to your email",
#                     }
#                     logger.info(response)
#                     return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
#                 else:
#                     response = {"Response": {
#                         "Status": "error"},
#                         "message": "Error in sending OTP",
#                     }
#                     logger.info(response)
#                     return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
#             else:
#                 response = {"Response": {
#                     "Status": "error"},
#                     "message": "User not registered",
#                 }
#                 logger.info(response)
#                 return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
#         else:
#             return JsonResponse({"Response": {
#                 "Status": "error"},
#                 "message": "Invalid login type"
#             }, safe=False, status=status.HTTP_200_OK)
#
#     response = {"Response": {"Status": "error"}, "message": "Method {} not allowed".format(request.method)}
#     return JsonResponse(response, safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# @api_view(['POST'])
# def user_login(request):
#     if request.method == 'POST':
#         email = request.data['email']
#         password = request.data['password']
#
#         user = authenticate(request, email=email, password=password)
#         logger.info("Logged in user is {}".format(user))
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 logged_user = User.objects.get(email=email)
#
#                 role = ""
#                 if logged_user.is_super_admin:
#                     role = "super_admin"
#                 elif logged_user.is_admin:
#                     role = "administrator"
#                 elif logged_user.is_supervisor:
#                     role = "supervisor"
#                 elif logged_user.is_operator:
#                     role = "operator"
#
#                 user_data = {
#                     "user": {
#                         'serial_no': logged_user.id,
#                         'creation_date': logged_user.date_joined,
#                         'username': logged_user.username,
#                         'user_role': role,
#                         'email': logged_user.email,
#                         'contact_no': logged_user.phone
#                     }
#                 }
#                 if role == "super_admin":
#                     company_details = Company.objects.get(id=logged_user.company_id)
#                     user_data["user"]["company_name"] = company_details.company_name
#                     user_data["user"]["gst_no"] = company_details.gst_no
#                     user_data["user"]["address1"] = company_details.address1
#                     user_data["user"]["address2"] = company_details.address2
#                     user_data["user"]["city"] = company_details.city
#                     user_data["user"]["state"] = company_details.state
#                     user_data["user"]["pincode"] = company_details.pincode
#                 logger.info(user_data)
#                 token, created = Token.objects.get_or_create(user=user)
#                 token = {'token': token.key}
#                 logger.info(token)
#                 user_data.update(token)
#                 return JsonResponse({"Response": {
#                     "Status": "status"},
#                     "Data": user_data
#                 }, safe=False, status=status.HTTP_200_OK)
#             else:
#                 return JsonResponse({"Response": {
#                     "Status": "error"},
#                     "message": "The company account is deleted. Please contact Super admin"
#                 }, safe=False, status=status.HTTP_200_OK)
#         else:
#             return JsonResponse({"Response": {
#                 "Status": "error"},
#                 "message": "Invalid mail id or password"
#             }, safe=False, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def otp_login(request, uidb64):
#     logger.info("OTP based login request")
#     if request.method == 'POST':
#         code = request.data['otpnumber']
#
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             logger.info("Got user id as {}".format(uid))
#         except (TypeError, ValueError, OverflowError):
#             logger.info("OTP Login: invalid user id")
#             response = {"Response": {"Status": "error"}, "message": "Login failed. Invalid OTP"}
#             return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
#
#         try:
#             logger.info("Getting user details")
#             user_obj = User.objects.get(id=uid)
#             if not user_obj.phone:
#                 return JsonResponse({"Response": {"Status": "error"},
#                                      "message": "Login failed. No phone number is provided"},
#                                     safe=False, status=status.HTTP_200_OK)
#
#             if user_obj.verify_otp(code)["status"]:
#                 if user_obj is not None:
#                     if user_obj.is_active:
#                         login(request, user_obj)
#                         logged_user = User.objects.get(id=uid)
#
#                         role = ""
#                         if logged_user.is_super_admin:
#                             role = "super_admin"
#                         elif logged_user.is_admin:
#                             role = "administrator"
#                         elif logged_user.is_supervisor:
#                             role = "supervisor"
#                         elif logged_user.is_operator:
#                             role = "operator"
#
#                         user_data = {
#                             "user": {
#                                 'serial_no': logged_user.id,
#                                 'creation_date': logged_user.date_joined,
#                                 'username': logged_user.username,
#                                 'user_role': role,
#                                 'email': logged_user.email,
#                                 'contact_no': logged_user.phone
#                             }
#                         }
#                         if role == "super_admin":
#                             company_details = Company.objects.get(id=logged_user.company_id)
#                             user_data["user"]["company_name"] = company_details.company_name
#                             user_data["user"]["gst_no"] = company_details.gst_no
#                             user_data["user"]["address1"] = company_details.address1
#                             user_data["user"]["address2"] = company_details.address2
#                             user_data["user"]["city"] = company_details.city
#                             user_data["user"]["state"] = company_details.state
#                             user_data["user"]["pincode"] = company_details.pincode
#                         logger.info(user_data)
#                         token, created = Token.objects.get_or_create(user=user_obj)
#                         token = {'token': token.key}
#                         logger.info(token)
#                         user_data.update(token)
#                         return JsonResponse({"Response": {
#                             "Status": "status"},
#                             "message": "OTP verified successfully",
#                             "Data": user_data
#                         }, safe=False, status=status.HTTP_200_OK)
#                     else:
#                         return JsonResponse({"Response": {
#                             "Status": "error"},
#                             "message": "Login failed. The company account is deleted or the user is blocked. "
#                                        "Please contact admin"
#                         }, safe=False, status=status.HTTP_200_OK)
#
#             logger.info("Login failed. Invalid otp or otp expired")
#             return JsonResponse({"Response": {"Status": "error"},
#                                  "message": "Login failed. Invalid or expired OTP"},
#                                 safe=False, status=status.HTTP_200_OK)
#         except User.DoesNotExist as err:
#             logger.error("Login failed. Couldn't find the requested User, {}".format(err))
#             return JsonResponse({"Response": {"Status": "error"},
#                                  "message": "Login failed. Couldn't find the requested user"},
#                                 safe=False, status=status.HTTP_200_OK)
#
#     response = {"Response": {"Status": "error"}, "message": "Method {} not allowed".format(request.method)}
#     return JsonResponse(response, safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# @api_view(['POST'])
# def user_registration(request):
#     if request.method == 'POST':
#         try:
#             username = request.data['username']
#             email = request.data['email']
#             phone_country = "+91"
#             mob = re.sub(r"\D", "", request.data['phone'])
#             phone = phone_country + str(mob)
#             company_name = request.data['company']
#             address1 = request.data['address1']
#             address2 = request.data['address2']
#             city = request.data['city']
#             pincode = request.data['pincode']
#             state = request.data['state']
#             gst_no = request.data['gstno']
#         except Exception as e:
#             logger.error("Signup: Error in getting user info: {}".format(e))
#             response = {"Response": {"Status": "error"}, "message": "Error in getting user info; {}".format(e)}
#             return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
#
#         if username.startswith('__'):
#             response = {"Response": {"Status": "error"}, "message": "Username not allowed"}
#             return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
#
#         try:
#             User.objects.get(username=username)
#             response = {"Response": {"Status": "error"}, "message": "The username is already taken"}
#             return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             pass
#
#         try:
#             User.objects.get(email=email)
#             response = {"Response": {"Status": "error"}, "message": "The email address is already used for registration"}
#             return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             pass
#
#         try:
#             User.objects.get(phone=phone)
#             response = {"Response": {"Status": "error"}, "message": "The phone number is already used for registration"}
#             return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             pass
#
#         with transaction.atomic():
#             try:
#                 company = Company.objects.get(company_name=company_name, gst_no=gst_no, pincode=pincode)
#                 admin_count_in_company = User.objects.filter(company_id=company, is_super_admin=True).count()
#                 logger.info("Admin count in company is {}".format(admin_count_in_company))
#                 if admin_count_in_company > 0:
#                     logger.info("Signup: Already a super admin is registered in the company \"{}\". "
#                                 "Only one super admin per company is allowed".format(company_name))
#                     response = {"Response": {"Status": "error"},
#                                 "message": "Only one super admin per company is allowed"}
#                     return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
#
#             except Company.DoesNotExist:
#                 try:
#                     company = Company()
#                     company.company_name = company_name
#                     company.address1 = address1
#                     company.address2 = address2
#                     company.city = city
#                     company.pincode = pincode
#                     company.state = state
#                     company.gst_no = gst_no
#                     company.save()
#                     logger.info("Signup: successfully added company info to db")
#                 except Exception as err:
#                     transaction.set_rollback(True)
#                     logger.info("Signup: Error in adding company info to db: {}".format(err))
#                     response = {"Response": {"Status": "error"}, "message": "Error in adding "
#                                                                             "company info to db: {}".format(err)}
#                     return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
#
#             try:
#                 # Add admin user to database
#                 super_admin_user = User.objects.create_user(username, email=email)
#                 super_admin_user.phone = phone  # phone_country + phone
#                 super_admin_user.is_super_admin = True
#                 super_admin_user.company = company
#                 super_admin_user.save()
#
#                 # Send welcome and verification email  # TODO get from env file
#                 brand_name = "Initiative Water"
#                 support_email = "support@initiative.com"
#                 support_phone = "+919569690292"
#                 super_admin_user.send_verification_email(get_current_site(request).domain, brand_name, support_email,
#                                                          support_phone)
#
#                 # super_admin_user.send_invite_sms()
#
#                 response = {"Response": {"Status": "success"}, "message": "User created successfully"}
#                 logger.info("Signup: successfully added user info to db")
#             except Exception as e:
#                 transaction.set_rollback(True)
#                 logger.info("Signup: Error in adding user info to db: {}".format(e))
#                 response = {"Response": {"Status": "error"}, "message": "Error in adding user info to db: {}".format(e)}
#                 return JsonResponse(response, safe=False, status=status.HTTP_400_BAD_REQUEST)
#             return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)
#     elif request.user and request.user.is_authenticated:
#         request.user.await_verification = True
#         return HttpResponseRedirect(reverse('user_not_verified'))
#     else:
#         return render(request, 'signup.html')
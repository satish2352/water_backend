import re
import os
from django.shortcuts import render
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from iwater.models import Site, User, SitePermission, Company
from init_water_app import settings
from iwater.iw_logger import logger


# Sourabh imported follwiing to debug user_blocking error
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect
from rest_framework.renderers import JSONRenderer




@api_view(['GET'])
def list_users(request):
    logger.info("User is {}".format(request.user))
    data = []

    all_users = User.objects.filter(email_verified=False).order_by('-id')
    for single_user in all_users.values():
        user_obj = User.objects.get(id=single_user["id"])
        if user_obj.is_link_expired():
            user_obj.invite_link_expired = True
            user_obj.save()
        else:
            user_obj.invite_link_expired = False
            user_obj.save()

    # ! operators cannot see user management
    if request.user.is_operator:
        return JsonResponse({"Response": {"Status": "error"}, "message": "Requested user not authorized to see users"},
                            safe=False, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        company = Company.objects.get(id=request.user.company_id)
        # !supervisors can only see the users they add
        if request.user.is_supervisor:
            users = User.objects.filter(company_id=company).filter(added_by_id=request.user).order_by('-id')
        else:
            # admins can see all invitations
            users = User.objects.filter(company_id=company).order_by('-id')

        # users = User.objects.all()

        for user_info in users.values():
            perm_obj = SitePermission.objects.filter(user_id=user_info["id"]).order_by('-id')
            count = 0
            for userid in perm_obj.values("user_id"):
                count += 1
            role = ""
            if not user_info["is_super_admin"]:
                if user_info["is_admin"]:
                    role = "administrator"
                elif user_info["is_supervisor"]:
                    role = "supervisor"
                elif user_info["is_operator"]:
                    role = "operator"

                user_status = -1
                # user_status = 0 invite sent
                # user_status = 1 invite accepted and active
                # user_status = 2 invite expired
                # user_status = 3 invite rejected
                if user_info["invite_rejected"]:
                    user_status = 3
                else:
                    if not user_info["email_verified"] and not user_info["invite_link_expired"]:
                        user_status = 0
                    elif user_info["email_verified"] and user_info["is_active"]:  # TODO check if is_active is needed
                        user_status = 1
                    elif user_info["invite_link_expired"]:
                        user_status = 2

                response_data = {
                    'serial_no': user_info["id"],
                    'creation_date': user_info["date_joined"],
                    'username': user_info["username"],
                    'avatar': 'http://{}{}{}'
                    .format(get_current_site(request).domain, settings.MEDIA_URL, user_info["avatar"])
                    if user_info["avatar"] else "",
                    'user_role': role,
                    'email': user_info["email"],
                    'contact_no': user_info["phone"],
                    "status": user_status,
                    'no_of_sites': count

                }
                data.append(response_data)

        logger.debug("users array length {}".format(len(data)))
        return JsonResponse({"Response": {
            "Status": "success"},
            "Data": data
        }, safe=False, status=status.HTTP_200_OK)


# @login_required
@api_view(['GET'])
def user(request, pk):

    data = []
    if request.method == 'GET':
        user_dat = User.objects.filter(id=pk) # ! pk from frontend
        if user_dat.count() < 1:
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_200_OK)

        for user_info in user_dat.values():
            perm_obj = SitePermission.objects.filter(user_id=user_info["id"])
            count = 0
            for userid in perm_obj.values("user_id"):
                count += 1
            role = "" # ! Role defination
            if not user_info["is_super_admin"]:
                if user_info["is_admin"]:
                    role = "administrator"
                elif user_info["is_supervisor"]:
                    role = "supervisor"
                elif user_info["is_operator"]:
                    role = "operator"

                # ! user invitation status
                user_status = -1
                # user_status = 0 invite sent
                # user_status = 1 invite accepted and active
                # user_status = 2 invite expired
                # user_status = 3 invite rejected
                if user_info["invite_rejected"]:
                    user_status = 3
                else:
                    if not user_info["email_verified"] and not user_info["invite_link_expired"]:
                        user_status = 0
                    elif user_info["email_verified"] and user_info["is_active"]:  # TODO check if is_active is needed
                        user_status = 1
                    elif user_info["invite_link_expired"]:
                        user_status = 2

                response_data = {
                    'serial_no': user_info["id"],
                    'creation_date': user_info["date_joined"],
                    'username': user_info["username"],
                    'avatar': 'http://{}{}{}'
                    .format(get_current_site(request).domain, settings.MEDIA_URL, user_info["avatar"])
                    if user_info["avatar"] else "",
                    'user_role': role,
                    'email': user_info["email"],
                    'contact_no': user_info["phone"],
                    # 'site_limit': user_info["site_limit"],
                    "status": user_status,
                    'no_of_sites': count

                }
                data.append(response_data)

        return JsonResponse({"Response": {
            "Status": "success"},
            "Data": data
        }, safe=False, status=status.HTTP_200_OK)


# TODO
# @login_required
@api_view(['POST'])
def add_user(request):
    logger.info("-----------------")
    logger.info("add user request")
    if request.method == 'POST':
        logger.info("Current user is {}".format(request.user))
        email = None
        phone = None
        mob = None
        try:
            username = request.POST.get('user_name')
            role = str(request.POST.get('user_role')).lower()
            try:
                # ! login via email
                email = request.POST.get('email_id')
                logger.info("email {}".format(email))
                try:
                    # ! user exists
                    if User.objects.get(email=email) and email != "":
                        response = {"Response": {"Status": "error"},
                                    "message": "The email address is already used for registration"}
                        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    pass
            except Exception as err:
                logger.error("error in getting mail details {}".format(err))
                return JsonResponse({"Response": {"Status": "error"}, "message": "Error in getting mail info"},
                                    safe=False, status=status.HTTP_200_OK)

            try:
                # ! login via phone
                phone_country = "+91"
                mob = re.sub(r"\D", "", request.POST.get('contact_number'))
                logger.info("phone from ui {}".format(mob))
                if mob is not "":
                    phone = phone_country + str(mob)
                    logger.debug("phone in if {}".format(phone))
                    try:
                        User.objects.get(phone=phone)
                        response = {"Response": {"Status": "error"},
                                    "message": "The phone number is already used for registration"}
                        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
                    except User.DoesNotExist:
                        pass
                logger.info("phone {}".format(mob))
            except Exception as err:
                logger.error("error in getting phone details {}".format(err))
                return JsonResponse({"Response": {"Status": "error"}, "message": "Error in getting phone info"},
                                    safe=False, status=status.HTTP_200_OK)
            image = request.FILES.get("user_picture")
            logger.debug("got user info successfully")
        except Exception as err:
            logger.error("Signup: Error in getting user info: {}".format(err))
            response = {"Response": {"Status": "error"}, "message": "Error in getting user info; {}".format(err)}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        # site_limit = request.POST.get("site_limit") if request.POST.get("site_limit") else 0
        logger.debug("after getting user info")
        company = Company.objects.get(id=request.user.company_id)

        if role not in ["administrator", "supervisor", 'operator']:
            response = {"Response": {
                "Status": "error"},
                "message": "Invalid user role"
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        logger.debug("after role check")
        # if request.user.is_operator or (request.user.is_supervisor and (role == "administrator" or role == "supervisor")):
        if ((request.user.is_super_admin and (role == "administrator" or role =="supervisor" or role == "operator" )) or
                (request.user.is_admin and (role == "administrator" or role == "supervisor" or role == "operator")
                 or request.user.is_supervisor and (role == "operator" or role == "supervisor"))):
        # if ((role == "administrator" or role == "supervisor" or role == "operator")
        #          or request.user.is_supervisor and (role == "operator")):

            logger.debug("user check")
            if username.startswith('__'):
                response = {"Response": {
                    "Status": "error"},
                    "message": "Username not allowed"
                }
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            logger.debug("user name check")

            try:
                User.objects.get(username=username)
                response = {"Response": {
                    "Status": "error"},
                    "message": "The username is already taken"
                }
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                pass
            # logger.debug("email check")

            # try:
            #     User.objects.get(email=email)
            #     response = {"Response": {
            #         "Status": "error"},
            #         "message": "The email address is already used for registration"
            #     }
            #     return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            # except User.DoesNotExist:
            #     pass
            # logger.debug("phone check 2")

            # try:
            #     User.objects.get(phone=phone)
            #     response = {"Response": {"Status": "error"}, "message": "The phone number is already used for registration"}
            #     return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            # except User.DoesNotExist:
            #     pass

            logger.debug("checks completed")

            with transaction.atomic():
                # ! saving user to databse

                try:
                    # Add user to database
                    # user = User.objects.create_user(username, email=email)
                    logger.info("creating user")
                    user = User()
                    user.username = username
                    # if email:
                    #     print("email signup")
                    #     user.email = email
                    # else:
                    #     print("sms signup")
                    #     user.phone = phone  # phone_country + phone

                    if role == "administrator":
                        user.is_admin = True
                    elif role == "supervisor":
                        user.is_supervisor = True
                    elif role == "operator":
                        user.is_operator = True

                    logger.info("checking email and phone")
                    if email is not "":
                        user.email = email
                    if phone:
                        user.phone = phone  # phone_country + phone
                    user.avatar = image
                    # user.site_limit = site_limit
                    user.company = company
                    user.added_by = request.user
                    site_obj = Site.objects.get(company_id=request.user.company_id)
                    if not site_obj:
                        if  role=="operator":
                            logger.error("user are try to add operator before adding site")
                            response = {"Response": {
                                "Status": "error"},
                                "message": "You are try to add operator before adding site"
                            }
                            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
                        else:
                            user.save()
                    else:
                        user.save()

                    logger.info("saved user details")
                    # Send welcome and verification email
                    super_user = User.objects.get(company_id=request.user.company_id, is_super_admin=True)
                    brand_name = Company.objects.get(id=request.user.company_id).company_name
                    support_email = super_user.email
                    support_phone = super_user.phone
                    logger.info("email and phone before sending {} {}".format(user.phone, user.email))

                    if user.phone is None and user.email is None:
                        logger.error("Both email and phone came as None")
                        transaction.set_rollback(True)
                        response = {"Response": {
                            "Status": "error"},
                            "message": "Either contact number or email id is required"
                        }
                        


                 ####################################################################################### 
                 # this comment for stop add user registation by using mobile number       
#                     if user.phone is not None:
#                         logger.info("invite user using phone")
#  #below two lines are commented by bharti                       
#  #                       user.send_invite_sms(get_current_site(request).domain, brand_name, support_email, support_phone,
#  #                                                request.user.username)
#  #below two lines added by bharti                       
#                         user.send_invite_sms(os.environ.get("SITE_DOMAIN"), brand_name, support_email, support_phone,
#                                                  request.user.username)                        
#                         response = {"Response": {
#                             "Status": "success"},
#                             "message": "User registered successfully.Please check the provided "
#                                        "phone for further instruction"
#                         }
                    ############################################################################################
                    if user.email is not None:
                        logger.info("invite user using mail")
                        
#below three lines commented by bharti

 #                       user.send_set_password_email(get_current_site(request).domain, brand_name, support_email,
 #                                                        support_phone,
 #                                                       request.user.username)

 #below three lines added by bharti

                        user.send_set_password_email(os.environ.get("SITE_DOMAIN"), brand_name, support_email,
                                                         support_phone,
                                                         request.user.username)
                        
                    # user.send_verification_email(get_current_site(request).domain, brand_name, support_email,
                    #                              support_phone, request.user.username)

                        response = {"Response": {
                            "Status": "success"},
                            "message": "User registered successfully.Please check the provided "
                                       "email inbox for further instruction"
                        }
                    return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)
                except Exception as e:
                    transaction.set_rollback(True)
                    logger.error("Error in saving user data; {}".format(e))
                    response = {"Response": {
                        "Status": "error"},
                        "message": "Error in saving user datas; {}".format(e)
                    }
                    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            # return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)
        else:
            response = {"Response": {
                "Status": "error"},
                "message": "You({user}) are not authorized to create any {role} account".format(user=request.user,
                                                                                                role=role)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
    # elif request.user and request.user.is_authenticated:
    #     request.user.await_verification = True
    #     return HttpResponseRedirect(reverse('user_not_verified'))
    # else:
    #     return render(request, 'signup.html')


@api_view(['GET'])
def resend_invite(request, pk):

    if request.method == 'GET':
        logger.info("Current user is {}".format(request.user))

        # user_id = request.data['user_id']

        user_obj = User.objects.get(id=pk)
        role = ""
        if user_obj.is_admin:
            role = "administrator"
        elif user_obj.is_supervisor:
            role = "supervisor"
        elif user_obj.is_operator:
            role = "operator"

        if request.user.is_operator or (request.user.is_supervisor and (role == "administrator" or role == "supervisor")):
            # TODO check if condition
            response = {"Response": {
                "Status": "error"},
                "message": "You({user}) are not authorized to create any {role} account".format(user=request.user,
                                                                                              role=role)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)

        try:
            # ! Send welcome and verification email
            super_user = User.objects.get(company_id=request.user.company_id, is_super_admin=True)
            brand_name = Company.objects.get(id=request.user.company_id).company_name
            support_email = super_user.email
            support_phone = super_user.phone
            if user_obj.phone is not None:
#below 2 lines are commented by bharti               
#               user_obj.send_invite_sms(get_current_site(request).domain, brand_name, support_email, support_phone,
#                                           request.user.username)
#below two lines are added by bharti              
                user_obj.send_invite_sms(os.environ.get("SITE_DOMAIN"), brand_name, support_email, support_phone,
                                             request.user.username)
 #below lines are commented by bharti               

 #           elif user_obj.email is not None:
 #               user_obj.send_set_password_email(get_current_site(request).domain, brand_name, support_email, support_phone,
 #                                            request.user.username)

 #below three lines are added by bharti

            elif user_obj.email is not None:
                user_obj.send_set_password_email(os.environ.get("SITE_DOMAIN"), brand_name, support_email, support_phone,
                                             request.user.username)
            user_obj.invite_link_expired = False
            user_obj.save()

            response = {"Response": {
                "Status": "success"},
                "message": "User invitation resent"
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            response = {"Response": {
                "Status": "error"},
                "message": "Error in sending user invite; {}".format(e)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

    return JsonResponse({"Response": {
                "Status": "error"},
                "message": "Invalid request"
            }, safe=False, status=status.HTTP_400_BAD_REQUEST)


# @login_required()
@api_view(['PUT'])
def edit_user(request, pk):

    if request.method == 'PUT':
        try:
            user_obj = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        username = request.POST.get('user_name')
        role = str(request.POST.get('user_role')).lower()
        image = request.FILES.get("user_picture")

        logger.info(request.user)

        if role not in ["administrator", "supervisor", 'operator']:
            response = {"Response": {
                "Status": "error"},
                "message": "Invalid user role"
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)

        if request.user.is_operator or (request.user.is_supervisor and role != "operator"):
            response = {
                "created": False,
                "error": "You({user}) are not authorized to create any {role} account".format(user=request.user,
                                                                                              role=role)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)

        try:
            # edit user to database
            user_obj = User.objects.get(id=pk)
            user_obj.username = username
            if role == "administrator":
                user.is_admin = True
            elif role == "supervisor":
                user_obj.is_supervisor = True
                # user_obj.is_operator = False
            elif role == "operator":
                user_obj.is_operator = True
                # user_obj.is_supervisor = False
            user_obj.avatar = image
            user_obj.save()

            response = {"Response": {
                "Status": "success"},
                "message": "User edited successfully"
            }
        except Exception as e:
            response = {"Response": {
                "Status": "error"},
                "message": "Error in saving user data; {}".format(e)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(response, safe=False, status=status.HTTP_201_CREATED)
    return JsonResponse({"Response": {
                "Status": "error"},
                "message": "Invalid request"
            }, safe=False, status=status.HTTP_400_BAD_REQUEST)


# ! block and unblock functionality
@api_view(['POST'])
def block_user(request, email):
    user = get_object_or_404(User, email=email)
    # user_profile = UserProfile.objects.get(user=user)
    user.is_blocked = True
    user.save()
    return Response({'message': f'{user.email} has been blocked.'})

@api_view(['POST'])

def unblock_user(request, email):
    user = get_object_or_404(User, email=email)
    # user_profile = UserProfile.objects.get(user=user)
    user.is_blocked = False
    user.save()
    return Response({'message': f'{user.email} has been unblocked.'})

def blocked_view(request):
    return render(request, "blocked.html")
    # return Response({'message': 'You are blocked.'})
    # return Response({'message': 'Ypu have been blocked.'}, status=403)
    # return Response({'message': 'You are blocked.'}, status=status.HTTP_403_FORBIDDEN, renderer_classes=[JSONRenderer])
    # return Response({'message': 'You are blocked.'}, status=status.HTTP_403_FORBIDDEN, content_type='text/html')




# @api_view(['GET'])
# def get_available_users(request, pk):
#     site_ids = []
#     available_users = []
#     logger.info("Got request to list available users before delete")
#     if request.method == 'GET':
#         try:
#             requested_user = User.objects.get(id=pk)
#         except ObjectDoesNotExist:
#             return JsonResponse({"Response": {
#                     "Status": "error"},
#                     'message': 'The user does not exist'
#                 }, status=status.HTTP_200_OK)
#
#         role = ""
#         user_obj = User.objects.filter(id=pk)
#         response_data = {}
#         for user_info in user_obj.values():
#             if not user_info["is_admin"]:
#                 logger.debug("About to delete user is not admin")
#                 if user_info["is_supervisor"]:
#                     role = "supervisor"
#                 elif user_info["is_operator"]:
#                     role = "operator"
#                 logger.debug("About to delete user is {}".format(role))
#
#         logger.debug("assigned_sites {}".format(site_ids))
#         logger.debug("About to delete user after loop is {}".format(role))
#         if role == "supervisor":
#             logger.debug("supervisor")
#             user_obj = User.objects.exclude(id=pk).filter(is_supervisor=True).\
#                 filter(company_id=request.user.company_id).filter(email_verified=True)
#             logger.debug(user_obj)
#         elif role == "operator":
#             logger.debug("operator")
#             user_obj = User.objects.filter(is_operator=True).filter(company_id=request.user.company_id).filter(email_verified=True).exclude(id=pk)
#             logger.debug(user_obj)
#
#         for user_dat in user_obj.values():
#             logger.info(user_dat)
#         # for site_id in site_ids:
#             assigned_site_count = 0
#             # logger.info("--------------")
#             # logger.info(user_dat)
#             # TODO exclude the users that are already assigned to the assigned_sites
#             perm_obj = SitePermission.objects.filter(user_id=user_dat["id"])  # .exclude(site_id=site_id["serial_no"])
#             for perm in perm_obj.values():
#                 assigned_site_count += 1
#                 # logger.info(perm)
#             if assigned_site_count < 4:
#                 dat = {
#                     'serial_no': user_dat["id"],
#                     'creation_date': user_dat["date_joined"],
#                     'username': user_dat["username"],
#                     'user_role': role,
#                     'email': user_dat["email"],
#                     'contact_no': user_dat["phone"],
#                     'site_limit': user_dat["site_limit"],
#                     'no_of_sites': assigned_site_count
#
#                 }
#                 available_users.append(dat)
#                 # logger.info(user_dat)
#                 # logger.info(assigned_site_count)
#
#         logger.debug("available_users {}".format(available_users))
#         response_data.update({"available_users": available_users})
#         return JsonResponse({"Response": {
#                 "Status": "success"},
#                 "Data": response_data
#             }, safe=False, status=status.HTTP_200_OK)
@api_view(['GET'])
def get_available_users(request, pk):
    site_ids = []
    available_users = []
    logger.info("Got request to list available users before delete")
    if request.method == 'GET':
        try:
            requested_user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return JsonResponse({"Response": {
                    "Status": "error"},
                    'message': 'The user does not exist'
                }, status=status.HTTP_200_OK)

        role = ""
        user_obj = User.objects.filter(id=pk)
        response_data = {}
        for user_info in user_obj.values():
            if not user_info["is_super_admin"]:
                logger.debug("About to delete user is not super admin")
                if user_info["is_supervisor"]:
                    role = "supervisor"
                elif user_info["is_operator"]:
                    role = "operator"
                elif user_info["is_admin"]:
                    role = "admin"
                logger.debug("About to delete user is {}".format(role))
            perm_obj = SitePermission.objects.filter(user_id=user_info["id"])
            count = 0
            for perm_info in perm_obj.values():
                count += 1
                site_obj = Site.objects.filter(id=perm_info["site_id"])
                for site_info in site_obj.values():
                    site_data = {
                        'serial_no': site_info["id"],
                        'creation_date': site_info["created"],
                        'site_name': site_info["site_name"],
                        'address': site_info["address"],
                        'city': site_info["city"],
                        'state': site_info["state"],
                        'device_mobile_number': site_info["phone"],
                        'status': site_info["status"],
                        'no_of_alerts': site_info["alerts"]

                    }
                    site_ids.append(site_data)

            # response_data = {
            #     "assigned_sites": site_ids,
            # }

            # logger.info(response_data)
            # logger.info(role)
        # print(site_ids)
        if site_ids:
            logger.debug("assigned_sites {}".format(site_ids))
            logger.debug("About to delete user after loop is {}".format(role))
            if role == "supervisor":
                logger.debug("supervisor")
                user_obj2 = User.objects.exclude(id=pk).filter(is_supervisor=True).\
                    filter(company_id=request.user.company_id).filter(email_verified=True)
                logger.debug(user_obj2)
            elif role == "operator":
                logger.debug("operator")
                user_obj2 = User.objects.exclude(id=pk).filter(is_operator=True).\
                    filter(company_id=request.user.company_id).filter(email_verified=True)
                logger.debug(user_obj2)
            elif role == "admin":
                logger.debug("admin")
                user_obj2 = User.objects.exclude(id=pk).filter(is_admin=True).\
                    filter(company_id=request.user.company_id).filter(email_verified=True)
                logger.debug(user_obj2)
            else:
                logger.debug(role)
                return JsonResponse({"Response": {
                    "Status": "error"},
                    "message": "Invalid user role"
                }, safe=False, status=status.HTTP_200_OK)

            for user_dat in user_obj2.values():
                logger.info(user_dat)
            # for site_id in site_ids:
                assigned_site_count = 0
                # logger.info("--------------")
                # logger.info(user_dat)
                # TODO exclude the users that are already assigned to the assigned_sites
                perm_obj = SitePermission.objects.filter(user_id=user_dat["id"])  # .exclude(site_id=site_id["serial_no"])
                for perm in perm_obj.values():
                    assigned_site_count += 1
                    # logger.info(perm)
                # if assigned_site_count < 100:
                dat = {
                    'serial_no': user_dat["id"],
                    'creation_date': user_dat["date_joined"],
                    'username': user_dat["username"],
                    'user_role': role,
                    'email': user_dat["email"],
                    'contact_no': user_dat["phone"],
                    'site_limit': user_dat["site_limit"],
                    'no_of_sites': assigned_site_count

                }
                available_users.append(dat)
                # logger.info(user_dat)
                # logger.info(assigned_site_count)

            logger.debug("available_users {}".format(available_users))
            response_data.update({"available_users": available_users})
            return JsonResponse({"Response": {
                    "Status": "success"},
                    "Data": response_data
                }, safe=False, status=status.HTTP_200_OK)
        else:
            response_data.update({"available_users": available_users})
            return JsonResponse({"Response": {
                "Status": "success"},
                "Data": response_data
            }, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def save_and_delete_user(request, pk):
    site_ids = []

    if request.method == 'POST':
        try:
            user_obj = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return JsonResponse(
                {
                    "Response": {
                        "Status": "error"
                    },
                    'message': 'The user does not exist'
                }, status=status.HTTP_200_OK)

        # TODO get site id and users then add user to site_permission table
        new_user = request.data['newuser']
        option = request.data['option']
        logger.info(new_user)

        role = ""
        site_datas = []
        user_obj = User.objects.filter(id=pk)
        response_data = {}
        for user_info in user_obj.values():
            if not user_info["is_super_admin"]:
                logger.debug("About to delete user is not super admin")
                if user_info["is_admin"]:
                    role = "administrator"
                elif user_info["is_supervisor"]:
                    role = "supervisor"
                elif user_info["is_operator"]:
                    role = "operator"
                logger.debug("About to delete user is {}".format(role))
            perm_obj = SitePermission.objects.filter(user_id=user_info["id"])
            count = 0
            for perm_info in perm_obj.values():
                count += 1
                site_obj = Site.objects.filter(id=perm_info["site_id"])
                for site_info in site_obj.values():
                    site_datas = {
                        'id': site_info["id"],
                        'creation_date': site_info["created"],
                        'site_name': site_info["site_name"],
                        'address': site_info["address"],
                        'city': site_info["city"],
                        'state': site_info["state"],
                        'device_mobile_number': site_info["phone"],
                        'status': site_info["status"],
                        'no_of_alerts': site_info["alerts"]

                    }
                    site_ids.append(site_datas)

            # response_data = {
            #     "assigned_sites": site_ids,
            # }

            # logger.info(response_data)
            # logger.info(role)
        logger.debug("sites assigned to user {} is:\n {}".format(pk, site_ids))
        # print("sites assigned to user {} is:\n {}".format(pk, site_ids))

        for site_user in site_ids:
            # print(site_user)
            supervisor_count_in_this_site = 0
            operator_count_in_this_site = 0

            site_data = Site.objects.filter(company_id=request.user.company_id, site_name=site_user["site_name"])

            for site_info in site_data.values():
                site_id = site_info["id"]

            # for users in site_user["user"]:
            logger.info("{}".format(new_user))
            user_data = User.objects.filter(username=new_user)

            # for site_info in site_data.values():
            #     site_id = site_info["id"]

            for user_info in user_data.values():
                user_id = user_info["id"]
                role = ""
                if user_info["is_supervisor"]:
                    role = "supervisor"
                elif user_info["is_operator"]:
                    role = "operator"
                logger.info(role)
                # get no. of supervisors and operators in a given site(max 3 supervisors and 2 operators)
                # if maximum reached before adding and deletion then return error with max count reached
                site_obj_for_getting_count = SitePermission.objects.filter(site_id=site_id)
                for site_dat in site_obj_for_getting_count.values():
                    logger.info(site_dat["user_id"])

                    user_dat_for_getting_user_role_count = User.objects.filter(id=site_dat["user_id"])
                    for user_dat in user_dat_for_getting_user_role_count.values():
                        if role == "supervisor" and user_dat["is_supervisor"]:
                            supervisor_count_in_this_site += 1
                            logger.info("Site {} has {} supervisors before deletion".format(
                                site_user["site_name"],
                                supervisor_count_in_this_site,
                                ))
                        elif role == "operator" and user_dat["is_operator"]:
                            operator_count_in_this_site += 1

                if role == "supervisor":
                    logger.info("Site {} has {} supervisors before deletion".format(
                        site_user["site_name"],
                        supervisor_count_in_this_site,
                    ))
                    if supervisor_count_in_this_site > 4:  # 3 plus 1 = 4 to add new user and delete old
                        return JsonResponse(
                            {
                                "Response": {
                                    "Status": "error"
                                },
                                'message': 'Save and delete failed because only 3 supervisors are permitted for Site {}'
                                .format(site_user["site_name"])
                            },
                            status=status.HTTP_200_OK)

                elif role == "operator":
                    logger.info("Site {} has {} operators before deletion".format(site_user["site_name"],
                                                                                  operator_count_in_this_site))
                    if operator_count_in_this_site > 3:  # 2 plus 1 = 3 to add new user and delete old
                        return JsonResponse(
                            {
                                "Response": {
                                    "Status": "error"
                                },
                                'message': 'Save and delete failed because only 2 operators are permitted for Site {}'
                                .format(site_user["site_name"])
                            },
                            status=status.HTTP_200_OK)

                existing_permission = SitePermission.objects.filter(user_id=user_id, site_id=site_id)
                if existing_permission:
                    logger.info("Skipping since, user {} already assigned to {} site".format(new_user,
                                                                                             site_user["site_name"]))
                    continue
                else:
                    with transaction.atomic():
                        try:
                            perm_obj = SitePermission()
                            perm_obj.user_id = user_id
                            perm_obj.site_id = site_id
                            perm_obj.save()
                            # User.objects.filter(pk=pk).delete()
                        except Exception as err:
                            transaction.set_rollback(True)
                            return JsonResponse(
                                {
                                    "Response": {
                                        "Status": "error"
                                    },
                                    'message': 'Save and delete failed, {}'.format(err)
                                },
                                status=status.HTTP_200_OK)

                logger.info(site_user)
        if option == "delete":
            try:
                User.objects.filter(pk=pk).delete()
                # print("deleting user")
            except Exception as err:
                return JsonResponse(
                    {
                        "Response": {
                            "Status": "error"
                        },
                        'message': 'Save and delete failed, {}'.format(err)
                    },
                    status=status.HTTP_200_OK)

            return JsonResponse(
                {
                    "Response": {
                        "Status": "success"
                    },
                    'message': 'user deleted successfully!'
                },
                status=status.HTTP_200_OK)
        elif option == "block":  # old code for blocking
            try:
                block_user = User.objects.get(pk=pk)
                block_user.is_active = False
                block_user.save()
                # print("deleting user")
            except Exception as err:
                return JsonResponse(
                    {
                        "Response": {
                            "Status": "error"
                        },
                        'message': 'Save and block failed, {}'.format(err)
                    },
                    status=status.HTTP_200_OK)

            return JsonResponse(
                {
                    "Response": {
                        "Status": "success"
                    },
                    'message': 'user blocked successfully!'
                },
                status=status.HTTP_200_OK)
        else:
            return JsonResponse(
                {
                    "Response": {
                        "Status": "error"
                    },
                    'message': 'Invalid option'
                },
                status=status.HTTP_200_OK)


@api_view(['GET'])
def delete_company_account(request):

    if not request.user.is_super_admin:
        response = {"Response": {
            "Status": "error"},
            "message": "You ({user}) are not authorized to delete account".format(user=request.user)
        }
        return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        try:
            company_users = User.objects.filter(company_id=request.user.company_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                {
                    "Response": {
                        "Status": "error"
                    },
                    'message': 'The user does not exist'
                }, status=status.HTTP_200_OK)

        try:
            for company_user in company_users.values():
                single_user = User.objects.get(id=company_user["id"])
                single_user.is_active = False
                single_user.save()
        except Exception as err:
            return JsonResponse(
                {
                    "Response": {
                        "Status": "error"
                    },
                    'message': 'Account deletion failed {}'.format(err)
                },
                status=status.HTTP_200_OK)

        return JsonResponse(
            {
                "Response": {
                    "Status": "success"
                },
                'message': 'Account deleted successfully'
            },
            status=status.HTTP_200_OK)

    response = {"Response": {
        "Status": "error"},
        "message": "Method not allowed"
    }
    return JsonResponse(response, safe=False, status=status.HTTP_405_METHOD_NOT_ALLOWED)

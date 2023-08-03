from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.sites.shortcuts import get_current_site


from iwater.models import ArchiveSite, ArchiveDevice, ArchiveSitePermission, User, SitePermission, Device, Subscription
from init_water_app import settings
from iwater.iw_logger import logger


@api_view(['GET'])
def list_archive_sites(request):
    city_state = []
    data = []
    unverified_data = []
    supervisors_data = []
    operators_data = []
    if request.method == 'GET':

        if request.user.is_operator:
            response = {"Response": {
                "Status": "error"},
                "message": "You({user}) are not authorized to view this page".format(user=request.user)
            }
            return JsonResponse(response, safe=False, status=status.HTTP_403_FORBIDDEN)

        site_obj = ArchiveSite.objects.filter(company_id=request.user.company_id).filter(phone_verified=1)
        for site_info in site_obj.values():
            perm_obj = ArchiveSitePermission.objects.filter(site_id=site_info["id"])
            supervisor = []
            operator = []
            for userid in perm_obj.values("user_id"):
                user_obj = User.objects.filter(id=userid["user_id"]).filter(is_supervisor=True).\
                    filter(is_operator=False)
                # user_obj = user_obj.filter(is_supervisor=True).filter(is_operator=False)  # TODO Set to True
                if user_obj:
                    supervisor.append([i for i in user_obj.values("username")])

                user_obj = User.objects.filter(id=userid["user_id"]).filter(is_operator=True).\
                    filter(is_supervisor=False)
                # user_obj = user_obj.filter(is_operator=False).filter(is_supervisor=False)  # TODO Set operator to True
                if user_obj:
                    operator.append([i for i in user_obj.values("username")])

            supervisors = []
            for j in supervisor:
                for k in j:
                    supervisors.append(k["username"])
                    # supervisors_data.append(k)

            operators = []
            for n in operator:
                for m in n:
                    operators.append(m["username"])
                    # operators_data.append(m)

            # logger.info("----------------------")
            users = {
                "supervisors": supervisors,
                "operators": operators
            }
            # logger.info(users)

            devices = {}
            device_obj = ArchiveDevice.objects.filter(site_id=site_info["id"])
            for dev in device_obj.values():
                devices = {
                    "device_name": [
                        "Device 1",
                        "Device 2",
                        "Device 3"
                    ],
                    "device_serial_number": [
                        dev["serial_no1"],
                        dev["serial_no2"],
                        dev["serial_no3"]
                    ],
                }
                # logger.info(devices)
            # logger.info("----------------------")
            response_data = {}
            if users["supervisors"] or users["operators"]:
                response_data = {
                    'serial_no': site_info["id"],
                    'creation_date': site_info["created"],
                    'site_name': site_info["site_name"],
                    'address': site_info["address"],
                    'city': site_info["city"],
                    'state': site_info["state"],
                    "supervisors": users["supervisors"],
                    "operators": users["operators"],
                    'device_mobile_number': site_info["phone"],
                    'status': site_info["status"],
                    'no_of_alerts': site_info["alerts"]

                }
                data.append(response_data)
                response_data.update(devices)
            else:
                unverified_response_data = {
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
                unverified_data.append(unverified_response_data)
                unverified_response_data.update(devices)

            city_state.append(site_info["city"])
            city_state.append(site_info["state"])

        logger.info('Response:')
        supervisor = []
        supervisrs = User.objects.filter(is_supervisor=True).filter(is_operator=False).filter(email_verified=1)\
            .filter(company_id=request.user.company_id)
        for userid in supervisrs.values():
            perm_obj = ArchiveSitePermission.objects.filter(user_id=userid["id"])
            count = 0
            for perm in perm_obj.values():
                count += 1
            supervisor.append({
                'serial_no': userid["id"],
                'creation_date': userid["date_joined"],
                'username': userid["username"],
                'avatar': 'http://{}{}{}'
                .format(get_current_site(request).domain, settings.MEDIA_URL, userid["avatar"])
                if userid["avatar"] else "",
                'user_role': "Supervisor",
                'email': userid["email"],
                'contact_no': userid["phone"],
                # 'site_limit': userid["site_limit"],
                'no_of_sites': count

            })
        logger.info("++++++++++++++===")
        # logger.info(supervisor)

        operator = []
        operatrs = User.objects.filter(is_supervisor=False).filter(is_operator=True).filter(email_verified=1).\
            filter(company_id=request.user.company_id)
        for userid in operatrs.values():
            perm_obj = ArchiveSitePermission.objects.filter(user_id=userid["id"])
            count = 0
            for perm in perm_obj.values():
                count += 1
            operator.append({
                'serial_no': userid["id"],
                'creation_date': userid["date_joined"],
                'username': userid["username"],
                'avatar': 'http://{}{}{}'
                .format(get_current_site(request).domain, settings.MEDIA_URL, userid["avatar"])
                if userid["avatar"] else "",
                'user_role': "Operator",
                'email': userid["email"],
                'contact_no': userid["phone"],
                # 'site_limit': userid["site_limit"],
                'no_of_sites': count

            })

        # context = {"sites": data, "unverified_sites": unverified_data, "city_state": list(set(city_state)), "supervisors": supervisor,
        #            "operators": operator}
        context = {"sites": data,  "supervisors": supervisor, "operators": operator}
        # logger.info(context)

        # logger.info(len(data))

        return JsonResponse({"Response": {"Status": "success"}, "Data": context},
                            safe=False, status=status.HTTP_200_OK)

    return JsonResponse({"Response": {"Status": "success"}, "Data": "Bad request"},
                        safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_archive_site(request, pk):

    if request.method == 'GET':

        site_dat = ArchiveSite.objects.filter(id=pk)
        if site_dat.count() < 1:
            return JsonResponse({
                "Response":
                    {
                        "Status": "error"
                     },
                "Data": "The requested site does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

        context = []
        site_obj = ArchiveSite.objects.filter(id=pk)
        for site_info in site_obj.values():
            perm_obj = ArchiveSitePermission.objects.filter(site_id=site_info["id"])
            supervisor = []
            operator = []
            for userid in perm_obj.values("user_id"):
                user_obj = User.objects.filter(id=userid["user_id"]).filter(is_supervisor=True). \
                    filter(is_operator=False)
                # user_obj = user_obj.filter(is_supervisor=True).filter(is_operator=False)  # TODO Set to True
                if user_obj:
                    supervisor.append([i for i in user_obj.values("username")])

                user_obj = User.objects.filter(id=userid["user_id"]).filter(is_operator=True). \
                    filter(is_supervisor=False)
                # user_obj = user_obj.filter(is_operator=False).filter(is_supervisor=False)  # TODO Set operator to True
                if user_obj:
                    operator.append([i for i in user_obj.values("username")])

            supervisors = []
            for j in supervisor:
                for k in j:
                    supervisors.append(k["username"])

            operators = []
            for n in operator:
                for m in n:
                    operators.append(m["username"])

            # logger.info("----------------------")
            users = {
                "supervisors": supervisors,
                "operators": operators
            }
            # logger.info(users)

            devices = {}
            device_obj = ArchiveDevice.objects.filter(site_id=site_info["id"])
            for dev in device_obj.values():
                devices = {
                    "device_name": [
                        "Device 1",
                        "Device 2",
                        "Device 3"
                    ],
                    "device_serial_number": [
                        dev["serial_no1"],
                        dev["serial_no2"],
                        dev["serial_no3"]
                    ],
                }
                # logger.info(devices)
            # logger.info("----------------------")
            response_data = {
                'serial_no': site_info["id"],
                'creation_date': site_info["created"],
                'site_name': site_info["site_name"],
                'address': site_info["address"],
                'city': site_info["city"],
                'state': site_info["state"],
                "supervisors": users["supervisors"],
                "operators": users["operators"],
                'device_mobile_number': site_info["phone"],
                'status': site_info["status"],
                'no_of_alerts': site_info["alerts"]
            }
            response_data.update(devices)
            # logger.info(response_data)
            context.append(response_data)

        logger.info('Response:')
        logger.info(context)

        logger.info(len(context))
        return JsonResponse({"Response": {"Status": "success"}, "Data": context},
                            safe=False, status=status.HTTP_200_OK)
    return JsonResponse({"Response": {"Status": "success"}, "Data": "Bad request"},
                        safe=False, status=status.HTTP_400_BAD_REQUEST)

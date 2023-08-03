from datetime import datetime

from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from iwater.models import Subscription
from iwater.iw_logger import logger

# ! Sending data to dashboard
@api_view(['GET'])
def dashboard(request):
    data = []
    total_sites = 0
    free_sites = 0
    assigned_sites = 0
    unassigned_sites = 0

    if request.method == 'GET':

        subscription = Subscription.objects.all()
        for subs in subscription.values():
            logger.info("\nsubscription - {}".format(subs["id"]))

            total_sites += 1

            logger.info("subscription_code - {}".format(subs["subscription_code"]))
            valid_till = datetime.strptime(str(subs["valid_till"]), "%Y-%m-%d")
            present_date = datetime.now()
            logger.info("present_date - {}".format(present_date))
            logger.info("valid_till - {}".format(valid_till))

            if subs["subscription_code"] is None:
                free_sites += 1
            elif valid_till.date() > present_date.date():  # TODO check if and subs["subscription_code"] is not None
                # is needed
                assigned_sites += 1
            elif valid_till.date() < present_date.date():  # TODO and subs["subscription_code"] is not None
                unassigned_sites += 1

        resp = {
            'no_of_sites': total_sites,
            'free_sites': free_sites,
            'assigned_sites': assigned_sites,
            'unassigned_sites': unassigned_sites,
        }
        data.append(resp)

        return JsonResponse(
            {"Response": {
                "Status": "success"
            },
                "Data": data
            }, safe=False, status=status.HTTP_200_OK)

    return JsonResponse({"Response": {
        "Status": "error"},
        "message": "Invalid request"
    }, safe=False, status=status.HTTP_400_BAD_REQUEST)

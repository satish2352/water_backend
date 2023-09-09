from iwater.models import User
from iwater import models as mo
from django.db import DatabaseError
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status

@api_view(['GET','POST'])
def sites_user_count(request):

    if request.method == 'POST':
        
        try:
            valid_sites=mo.Site.objects.filter(company=request.user.company_id).filter(phone_verified=1,token_verified=1).order_by('-id')
            valid_sites_count = valid_sites.count()
            logged_user = User.objects.get(request.user.id)
            role = ""

            if logged_user.is_admin:
                logged_user = User.objects.filter(company_id = request.user.company_id).filter(is_admin=True).all()
                total_count_user = logged_user.count()
                total_count = 1 + valid_sites_count
                if total_count_user < total_count:
                    return JsonResponse({"Response": {"Status": True}, "Data": "You can add User"},
                            safe=False, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"Response": {"Status": "unable to add user as limit over"}, "Data": total_count_user},
                            safe=False, status=status.HTTP_400_BAD_REQUEST)
                
            elif logged_user.is_supervisor:
                logged_user = User.objects.filter(company_id = request.user.company_id).filter(is_supervisor=True).all()
                total_count_user = logged_user.count()
                total_count = 1 + (valid_sites_count * 2)
                if total_count_user < total_count:
                    return JsonResponse({"Response": {"Status": True}, "Data": "You can add User"},
                            safe=False, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"Response": {"Status": "unable to add user as limit over"}, "Data": total_count_user},
                            safe=False, status=status.HTTP_400_BAD_REQUEST)
            elif logged_user.is_staff:
                logged_user = User.objects.filter(company_id = request.user.company_id).filter(is_staff=True).all()
                total_count_user = logged_user.count()
                total_count = valid_sites_count * 2
                if total_count_user < valid_sites_count:
                    return JsonResponse({"Response": {"Status": True}, "Data": "You can add User"},
                            safe=False, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"Response": {"Status": "unable to add user as limit over"}, "Data": total_count_user},
                            safe=False, status=status.HTTP_400_BAD_REQUEST)


            else:
                return JsonResponse({"Response": {"Status": "success"}, "Data": total_count},
                            safe=False, status=status.HTTP_200_OK)
        
        except DatabaseError as e:
            print("Custom Exception:",e)
                
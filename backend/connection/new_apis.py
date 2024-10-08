from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from .models import *
from datetime import datetime
from connection.views import mqttc
from datetime import datetime
from django.db import DatabaseError
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http import HttpRequest


def dateandtime():
    year=datetime.today().strftime('%Y')
    month=datetime.today().strftime('%m')
    day=datetime.today().strftime('%d')
    hour=datetime.now().strftime('%H')
    minit=datetime.now().strftime('%M')
    second=datetime.now().strftime('%S')
    return year,month,day,hour,minit,second

@api_view(['POST'])
def newtap1settingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            value_list = data_dict
           
            dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            if dinfo is not None:

                device_final_data = {}
                if 'p1' in value_list:
                    device_final_data['p1'] = value_list['p1']
                else:
                    device_final_data['p1'] = ''
                if 'p2' in value_list:
                    device_final_data['p2'] = value_list['p2']
                else:
                    device_final_data['p2']=''
                if 'p3' in value_list:
                    device_final_data['p3'] = value_list['p3']
                else:
                    device_final_data['p3']=''
                if 'p4' in value_list:
                    device_final_data['p4'] = value_list['p4']
                else:
                    device_final_data['p4']=''

                for key, value in device_final_data.items():
                    value = str(value)
                    temp = value.isalnum()
                    if  temp is not False:
                        value.replace('"', "'")
                        value.replace(' ','')
                        device_final_data[key] = value
                    else:
                        device_final_data[key] = ''

                deviceid = None
                deviceid = dinfo.Device_id

                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/tap1',str(device_final_data).replace(' ',''))
                    # dd=dateandtime()
                    # print("dd dd ",dd)
                    # e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap1 settings change has been requested - pulse1:{value_list['p1']}, pulse2:{value_list['p2']}, pulse3:{value_list['p3']}, pulse4:{value_list['p4']}"
                    # erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    # # erro.save()
                    try:
                        value_list_final = {}
                        if 'p1' in value_list:
                            value_list_final['p1'] = value_list['p1']
                        if 'p2' in value_list:
                            value_list_final['p2'] = value_list['p2']
                        if 'p3' in value_list:
                            value_list_final['p3'] = value_list['p3']
                        if 'p4' in value_list:
                            value_list_final['p4'] = value_list['p4']
                        value_list_final['componant_name'] = 'tap1'
                        value_list_final['unit_type'] = 'water_dispense'
                        value_list_final['device_id'] = deviceid
                        value_list_final['company_id'] = request.user.company_id
                        tap1_setting.objects.create(**value_list_final)
                        return Response({"message": "NEW TAP-1 API 200"})
                    except Exception as e:
                        print("Error in tap1setting ",e) 
        except Exception as e:
            print("Error in tap1setting ",e)    



    # if request.method == 'POST':
    #     try:
    #         print("request  ",request)
    #         print("request body  ",request.user)
    #         print("request.user.company_id ",request.user.company_id)
    #         data_dict = json.loads(request.body)
    #         unwanted_keys = ["unit_type", "water_treatment","componant_name","site_name","device_id"]
    #         value_list=list(data_dict.values())
    #         print("value_list value_list",value_list)
    #         print("value_list[0] ",value_list[0])
    #         dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
    #         if dinfo is not None:
    #             print("dinfo dinfo",dinfo)
    #             obj = tap1_setting.objects.create(**data_dict)
    #             for key in unwanted_keys:
    #                         if key in data_dict.keys():
    #                             del data_dict[key]
                
    #             deviceid = None
    #             deviceid=dinfo.Device_id
    #             print("deviceid ",deviceid)
    #             if deviceid:
    #                 mqttc.publish(f'wc1/{deviceid}/chgset/tap1',str(data_dict).replace(' ',''))
    #                 dd=dateandtime()
    #                 print("dd dd ",dd)
    #                 e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap1 settings change has been requested - pulse1:{value_list[2]}, pulse2:{value_list[3]}, pulse3:{value_list[4]}, pulse4:{value_list[5]}"
    #                 erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
    #                 erro.save()

    #                 obj.unit_type = value_list[0]
    #                 obj.componant_name = value_list[1]
    #                 obj.device_id = deviceid
    #                 obj.company_id = request.user.company_id
    #                 obj.save()
    #             return Response({"message": "NEW TAP-1 API 200"})
    #     except Exception as e:
    #         print("Error in tap1setting ",e)    

@api_view(['POST'])
def newtap2settingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            value_list = data_dict
           
            dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            if dinfo is not None:

                device_final_data = {}
                if 'p1' in value_list:
                    device_final_data['p1'] = value_list['p1']
                else:
                    device_final_data['p1'] = ''
                if 'p2' in value_list:
                    device_final_data['p2'] = value_list['p2']
                else:
                    device_final_data['p2']=''
                if 'p3' in value_list:
                    device_final_data['p3'] = value_list['p3']
                else:
                    device_final_data['p3']=''
                if 'p4' in value_list:
                    device_final_data['p4'] = value_list['p4']
                else:
                    device_final_data['p4']=''

                for key, value in device_final_data.items():
                    value = str(value)
                    temp = value.isalnum()
                    if  temp is not False:
                        value.replace('"', "'")
                        value.replace(' ','')
                        device_final_data[key] = value
                    else:
                        device_final_data[key] = ''

                deviceid = None
                deviceid = dinfo.Device_id

                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/tap2',str(device_final_data).replace(' ',''))
                    # dd=dateandtime()
                    # print("dd dd ",dd)
                    # e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap2 settings change has been requested - pulse1:{value_list['p1']}, pulse2:{value_list['p2']}, pulse3:{value_list['p3']}, pulse4:{value_list['p4']}"
                    # erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap2',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    # erro.save()
                    try:
                        value_list_final = {}
                        if 'p1' in value_list:
                            value_list_final['p1'] = value_list['p1']
                        if 'p2' in value_list:
                            value_list_final['p2'] = value_list['p2']
                        if 'p3' in value_list:
                            value_list_final['p3'] = value_list['p3']
                        if 'p4' in value_list:
                            value_list_final['p4'] = value_list['p4']
                        value_list_final['componant_name'] = 'tap2'
                        value_list_final['unit_type'] = 'water_dispense'
                        value_list_final['device_id'] = deviceid
                        value_list_final['company_id'] = request.user.company_id
                        tap2_setting.objects.create(**value_list_final)
                        return Response({"message": "NEW TAP-2 API 200"})
                    except Exception as e:
                        print("Error in tap2setting ",e) 
        except Exception as e:
            print("Error in tap2setting ",e)    


@api_view(['POST'])
def newtap3settingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            value_list = data_dict
           
            dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            if dinfo is not None:

                device_final_data = {}
                if 'p1' in value_list:
                    device_final_data['p1'] = value_list['p1']
                else:
                    device_final_data['p1'] = ''
                if 'p2' in value_list:
                    device_final_data['p2'] = value_list['p2']
                else:
                    device_final_data['p2']=''
                if 'p3' in value_list:
                    device_final_data['p3'] = value_list['p3']
                else:
                    device_final_data['p3']=''
                if 'p4' in value_list:
                    device_final_data['p4'] = value_list['p4']
                else:
                    device_final_data['p4']=''

                for key, value in device_final_data.items():
                    value = str(value)
                    temp = value.isalnum()
                    if  temp is not False:
                        value.replace('"', "'")
                        value.replace(' ','')
                        device_final_data[key] = value
                    else:
                        device_final_data[key] = ''

                deviceid = None
                deviceid = dinfo.Device_id

                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/tap3',str(device_final_data).replace(' ',''))
                    # dd=dateandtime()
                    # print("dd dd ",dd)
                    # e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap3 settings change has been requested - pulse1:{value_list['p1']}, pulse2:{value_list['p2']}, pulse3:{value_list['p3']}, pulse4:{value_list['p4']}"
                    # erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap3',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    # erro.save()
                    try:
                        value_list_final = {}
                        if 'p1' in value_list:
                            value_list_final['p1'] = value_list['p1']
                        if 'p2' in value_list:
                            value_list_final['p2'] = value_list['p2']
                        if 'p3' in value_list:
                            value_list_final['p3'] = value_list['p3']
                        if 'p4' in value_list:
                            value_list_final['p4'] = value_list['p4']
                        value_list_final['componant_name'] = 'tap3'
                        value_list_final['unit_type'] = 'water_dispense'
                        value_list_final['device_id'] = deviceid
                        value_list_final['company_id'] = request.user.company_id
                        tap3_setting.objects.create(**value_list_final)
                        return Response({"message": "NEW TAP-2 API 200"})
                    except Exception as e:
                        print("Error in tap3setting ",e) 
        except Exception as e:
            print("Error in tap3setting ",e)    


@api_view(['POST'])
def newtap4settingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            value_list = data_dict
           
            dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            if dinfo is not None:

                device_final_data = {}
                if 'p1' in value_list:
                    device_final_data['p1'] = value_list['p1']
                else:
                    device_final_data['p1'] = ''
                if 'p2' in value_list:
                    device_final_data['p2'] = value_list['p2']
                else:
                    device_final_data['p2']=''
                if 'p3' in value_list:
                    device_final_data['p3'] = value_list['p3']
                else:
                    device_final_data['p3']=''
                if 'p4' in value_list:
                    device_final_data['p4'] = value_list['p4']
                else:
                    device_final_data['p4']=''

                for key, value in device_final_data.items():
                    value = str(value)
                    temp = value.isalnum()
                    if  temp is not False:
                        value.replace('"', "'")
                        value.replace(' ','')
                        device_final_data[key] = value
                    else:
                        device_final_data[key] = ''

                deviceid = None
                deviceid = dinfo.Device_id

                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/tap4',str(device_final_data).replace(' ',''))
                    dd=dateandtime()
                    print("dd dd ",dd)
                    e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap4 settings change has been requested - pulse1:{value_list['p1']}, pulse2:{value_list['p2']}, pulse3:{value_list['p3']}, pulse4:{value_list['p4']}"
                    erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap4',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    # erro.save()
                    try:
                        value_list_final = {}
                        if 'p1' in value_list:
                            value_list_final['p1'] = value_list['p1']
                        if 'p2' in value_list:
                            value_list_final['p2'] = value_list['p2']
                        if 'p3' in value_list:
                            value_list_final['p3'] = value_list['p3']
                        if 'p4' in value_list:
                            value_list_final['p4'] = value_list['p4']
                        value_list_final['componant_name'] = 'tap4'
                        value_list_final['unit_type'] = 'water_dispense'
                        value_list_final['device_id'] = deviceid
                        value_list_final['company_id'] = request.user.company_id
                        tap4_setting.objects.create(**value_list_final)
                        return Response({"message": "NEW TAP-4 API 200"})
                    except Exception as e:
                        print("Error in tap4setting ",e) 
        except Exception as e:
            print("Error in tap4setting ",e)    



#updates api for tap
@api_view(['POST'])
def updated_disp_Tap1Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = data
        print("value_list:", value_list)

        dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()


        if dinfo:
            did = dinfo.Device_id
            qs_set = disp_tap1.objects.filter(device_id=did, message_type="updset").values('p1','p2','p3','p4','updated_at','created_at').order_by('-id')[:1:1]
            if qs_set:
                qs_set_final = qs_set[0]
            else:
                qs_set_final= {}
            last_error = Errors.objects.filter(service='tap1').values('message_type','e_discriptions','o_message','service','year','month','day','hour','minit','second')
            if last_error:
                last_error_final = last_error[0]
            else:
                last_error_final= {}

            data_final = {'data_set': qs_set_final, 'error': last_error_final}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 404,
                'message': "Device not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError as e:
        print("JSON Decode Error in updated_disp_Tap1Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_Tap1Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def updated_disp_Tap2Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = data
        print("value_list:", value_list)

        dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()


        if dinfo:
            did = dinfo.Device_id
            qs_set = disp_tap2.objects.filter(device_id=did, message_type="updset").values('p1','p2','p3','p4','updated_at','created_at').order_by('-id')[:1:1]
            if qs_set:
                qs_set_final = qs_set[0]
            else:
                qs_set_final= {}
            last_error = Errors.objects.filter(service='tap2').values('message_type','e_discriptions','o_message','service','year','month','day','hour','minit','second')
            if last_error:
                last_error_final = last_error[0]
            else:
                last_error_final= {}

            data_final = {'data_set': qs_set_final, 'error': last_error_final}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 404,
                'message': "Device not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError as e:
        print("JSON Decode Error in updated_disp_Tap2Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_Tap2Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def updated_disp_tap3Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = data
        print("value_list:", value_list)

        dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()


        if dinfo:
            did = dinfo.Device_id
            qs_set = disp_tap3.objects.filter(device_id=did, message_type="updset").values('p1','p2','p3','p4','updated_at','created_at').order_by('-id')[:1:1]
            if qs_set:
                qs_set_final = qs_set[0]
            else:
                qs_set_final= {}
            last_error = Errors.objects.filter(service='tap3').values('message_type','e_discriptions','o_message','service','year','month','day','hour','minit','second')
            if last_error:
                last_error_final = last_error[0]
            else:
                last_error_final= {}
            data_final = {'data_set': qs_set_final, 'error': last_error_final}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 404,
                'message': "Device not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError as e:
        print("JSON Decode Error in updated_disp_Tap3Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_Tap3Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def updated_disp_tap4Viewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = data
        print("value_list:", value_list)

        dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()


        if dinfo:
            did = dinfo.Device_id
            qs_set = disp_tap4.objects.filter(device_id=did, message_type="updset").values('p1','p2','p3','p4','updated_at','created_at').order_by('-id')[:1:1]
            if qs_set:
                qs_set_final = qs_set[0]
            else:
                qs_set_final= {}
            last_error = Errors.objects.filter(service='tap4').values('message_type','e_discriptions','o_message','service','year','month','day','hour','minit','second')
            if last_error:
                last_error_final = last_error[0]
            else:
                last_error_final= {}
            data_final = {'data_set': qs_set_final, 'error': last_error_final}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 404,
                'message': "Device not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError as e:
        print("JSON Decode Error in updated_disp_Tap4Viewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_Tap4Viewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def updated_disp_AtmViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = data
        print("value_list:", value_list)

        dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()


        if dinfo:
            did = dinfo.Device_id
            qs_sta = disp_atm.objects.filter(device_id=did, message_type="updsta").values('sts','ndv','ntt','nta','tmp','whr','custid','created_at','updated_at').order_by('-id')[:1:1]
            if qs_sta:
                qs_sta_final = qs_sta[0]
            else:
                qs_sta_final= {}
            qs_set = disp_atm.objects.filter(device_id=did, message_type="updset").values('ntp','nov','vl1','vl2','vl3','vl4','re1','re2','re3','re4','created_at','updated_at').order_by('-id')[:1:1]
            if qs_set:
                qs_set_final = qs_set[0]
            else:
                qs_set_final= {}
            last_error = Errors.objects.filter(service='atm').values('message_type','e_discriptions','o_message','service','year','month','day','hour','minit','second')
            if last_error:
                last_error_final = last_error[0]
            else:
                last_error_final= {}

            data_final = {'data_sta': qs_sta_final, 'data_set': qs_set_final, 'error': last_error_final}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 404,
                'message': "Device not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError as e:
        print("JSON Decode Error in updated_disp_atmViewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_atmViewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def atm_setting_Viewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            value_list = data_dict
           
            dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            if dinfo is not None:

                device_final_data = {}
                if 'ntp' in value_list:
                    device_final_data['ntp'] = value_list['ntp']
                else:
                    device_final_data['ntp'] = ''
                if 'nov' in value_list:
                    device_final_data['nov'] = value_list['nov']
                else:
                    device_final_data['nov'] = ''
                if 'vl1' in value_list:
                    device_final_data['vl1'] = value_list['vl1']
                else:
                    device_final_data['vl1'] = ''
                if 'vl2' in value_list:
                    device_final_data['vl2'] = value_list['vl2']
                else:
                    device_final_data['vl2'] = ''
                if 'vl3' in value_list:
                    device_final_data['vl3'] = value_list['vl3']
                else:
                    device_final_data['vl3'] = ''
                if 'vl4' in value_list:
                    device_final_data['vl4'] = value_list['vl4']
                else:
                    device_final_data['vl4'] = ''
                if 're1' in value_list:
                    device_final_data['re1'] = value_list['re1']
                else:
                    device_final_data['re1'] = ''
                if 're2' in value_list:
                    device_final_data['re2'] = value_list['re2']
                else:
                    device_final_data['re2'] = ''
                if 're3' in value_list:
                    device_final_data['re3'] = value_list['re3']
                else:
                    device_final_data['re3'] = ''
                if 're4' in value_list:
                    device_final_data['re4'] = value_list['re4']
                else:
                    device_final_data['re4'] = ''


                for key, value in device_final_data.items():
                    value = str(value)
                    temp = value.isalnum()
                    if  temp is not False:
                        value.replace('"', "'")
                        value.replace(' ','')
                        device_final_data[key] = value
                    else:
                        device_final_data[key] = ''

                deviceid = None
                deviceid = dinfo.Device_id

                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/atm',str(device_final_data).replace(' ',''))
                    # dd=dateandtime()
                    # e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} atm settings change has been requested - over no. Of  ntp:{value_list['ntp']}, no. Of volume:{value_list['nov']}, volume1:{value_list['vl1']}, volume2:{value_list['vl2']}, volume3:{value_list['vl3']}, volume4:{value_list['vl4']}, rate1:{value_list['re1']}, rate2:{value_list['re2']}, rate3:{value_list['re3']}, rate4:{value_list['re4']}"
                    # erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='atm',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    # erro.save()
                    try:
                        value_list_final = {}
                        if 'ntp' in value_list:
                            value_list_final['ntp'] = value_list['ntp']
                        if 'nov' in value_list:
                            value_list_final['nov'] = value_list['nov']
                        if 'vl1' in value_list:
                            value_list_final['vl1'] = value_list['vl1']
                        if 'vl2' in value_list:
                            value_list_final['vl2'] = value_list['vl2']
                        if 'vl3' in value_list:
                            value_list_final['vl3'] = value_list['vl3']
                        if 'vl4' in value_list:
                            value_list_final['vl4'] = value_list['vl4']
                        if 're1' in value_list:
                            value_list_final['re1'] = value_list['re1']
                        if 're2' in value_list:
                            value_list_final['re2'] = value_list['re2']
                        if 're3' in value_list:
                            value_list_final['re3'] = value_list['re3']
                        if 're4' in value_list:
                            value_list_final['re4'] = value_list['re4']
                        value_list_final['componant_name'] = 'atm'
                        value_list_final['unit_type'] = 'water_dispense'
                        value_list_final['device_id'] = deviceid
                        value_list_final['company_id'] = request.user.company_id
                        atm_setting.objects.create(**value_list_final)
                        return Response({"message": "NEW ATM SETTING API 200"})
                    except Exception as e:
                        print("error while saving atm record ",e)
        except Exception as e:
            print("Error in atmsetting ",e)    

#cnd_sen
@api_view(['POST'])
def cnd_senViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            value_list = data_dict
           
            dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            if dinfo is not None:

                device_final_data = {}
                if 'spn' in value_list:
                    device_final_data['spn'] = value_list['spn']
                else:
                    device_final_data['spn'] = ''
                if 'tsp' in value_list:
                    device_final_data['tsp'] = value_list['tsp']
                else:
                    device_final_data['tsp'] = ''
                if 'asp' in value_list:
                    device_final_data['asp'] = value_list['asp']
                else:
                    device_final_data['asp'] = ''

                for key, value in device_final_data.items():
                    value = str(value)
                    temp = value.isalnum()
                    if  temp is not False:
                        value.replace('"', "'")
                        value.replace(' ','')
                        device_final_data[key] = value
                    else:
                        device_final_data[key] = ''

                deviceid = None
                deviceid = dinfo.Device_id

                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/cnd_sen',str(device_final_data).replace(' ',''))
                    # dd=dateandtime()
                    # e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd settings change has been requested - span:{value_list['spn']}, trip_setpoint:{value_list['tsp']}, atert_setpoint:{value_list['asp']}"
                    # erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='cnd',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    # erro.save()
                    try:
                        value_list_final = {}
                        if 'spn' in value_list:
                            value_list_final['spn'] = value_list['spn']
                        if 'tsp' in value_list:
                            value_list_final['tsp'] = value_list['tsp']
                        if 'asp' in value_list:
                            value_list_final['asp'] = value_list['asp']
                        value_list_final['componant_name'] = 'cnd_sen'
                        value_list_final['unit_type'] = 'water_treatment'
                        value_list_final['device_id'] = deviceid
                        value_list_final['company_id'] = request.user.company_id
                        cnd_setting.objects.create(**value_list_final)
                        return Response({"message": "NEW cnd_sen API 200"})
                    except Exception as e:
                        print("error while saving cnd_sen record ",e)
        except Exception as e:
            print("Error in cnd_senetting ",e)    

    # if request.method == 'POST':
    #     try:
    #         data_dict = json.loads(request.body)
    #         unwanted_keys = ["unit_type","componant_name"]
    #         value_list=data_dict
    #         try:
    #             dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
    #         except Exception as e:
    #             print("device not found  ",e)
    #         else:
            
    #             for key in unwanted_keys:
    #                 if key in data_dict.keys():
    #                     del data_dict[key]
                
    #             deviceid = None
    #             deviceid=dinfo.Device_id
    #             if deviceid:
    #                 mqttc.publish(f'wc1/{deviceid}/chgset/cnd_sen',str(data_dict).replace(' ',''))
    #                 dd=dateandtime()
    #                 e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd settings change has been requested - span:{value_list['spn']}, trip_setpoint:{value_list['tsp']}, atert_setpoint:{value_list['asp']}"
    #                 erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='cnd',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
    #                 erro.save()

    #                 try:
    #                     value_list['componant_name'] = 'cnd_sen'
    #                     value_list['device_id'] = deviceid
    #                     value_list['company_id'] = request.user.company_id
    #                     cnd_consen_setting.objects.create(**value_list)
    #                     return Response({"message": "NEW CND_SEN SETTING API 200"})
    #                 except Exception as e:
    #                     print("error while saving cnd sen record   ",e)
                
    #     except Exception as e:
    #         print("Error in cnd_sen SETTING API  ",e)

@api_view(['POST'])
def newupdated_treat_cnd_senViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        print("********************************")

        value_list = data
        print(value_list)
        print("value_list['site_name']::",value_list['site_name'])

        dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()


        if dinfo:

            did = dinfo.Device_id
            qs_sta = treat_cnd_sen.objects.filter(device_id=did, message_type="updsta").values('cnd','created_at','updated_at').order_by('-id')[:1:1]
            if qs_sta:
                qs_sta_final = qs_sta[0]
            else:
                qs_sta_final= {}

            qs_set = treat_cnd_sen.objects.filter(device_id=did, message_type="updset").values('spn','tsp','asp','created_at','updated_at').order_by('-id')[:1:1]
            if qs_set:
                qs_set_final = qs_set[0]
            else:
                qs_set_final= {}

            last_error = Errors.objects.filter(service='cnd_sen').values('message_type','e_discriptions','o_message','service','year','month','day','hour','minit','second')
            if last_error:
                last_error_final = last_error[0]
            else:
                last_error_final= {}
            data_final = {'data_sta': qs_sta_final, 'data_set': qs_set_final, 'error': last_error_final}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 404,
                'message': "Device not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError as e:
        print("JSON Decode Error in updated_disp_cnd_senViewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_cnd_senViewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#cnd_consen
@api_view(['POST'])
def newcnd_consensettingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            value_list = data_dict
           
            dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            if dinfo is not None:

                device_final_data = {}
                if 'spn' in value_list:
                    device_final_data['spn'] = value_list['spn']
                else:
                    device_final_data['spn'] = ''
                if 'asp' in value_list:
                    device_final_data['asp'] = value_list['asp']
                else:
                    device_final_data['asp'] = ''


                for key, value in device_final_data.items():
                    value = str(value)
                    temp = value.isalnum()
                    if  temp is not False:
                        value.replace('"', "'")
                        value.replace(' ','')
                        device_final_data[key] = value
                    else:
                        device_final_data[key] = ''

                deviceid = None
                deviceid = dinfo.Device_id

                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/cnd_consen',str(device_final_data).replace(' ',''))
                    # dd=dateandtime()
                    # e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd_consen settings change has been requested - span:{value_list['spn']}, atert_setpoint:{value_list['asp']}"
                    # erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='cnd_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    # erro.save()
                    try:
                        value_list_final = {}
                        if 'spn' in value_list:
                            value_list_final['spn'] = value_list['spn']
                        if 'asp' in value_list:
                            value_list_final['asp'] = value_list['asp']
                        value_list_final['componant_name'] = 'cnd_consen'
                        value_list_final['unit_type'] = 'water_dispense'
                        value_list_final['device_id'] = deviceid
                        value_list_final['company_id'] = request.user.company_id
                        cnd_consen_setting.objects.create(**value_list_final)
                        return Response({"message": "NEW cnd_consen API 200"})
                    except Exception as e:
                        print("Error in cnd_consensetting ",e) 
        except Exception as e:
            print("Error in cnd_consensetting ",e)    

    # if request.method == 'POST':
    #     try:
    #         data_dict = json.loads(request.body)
    #         unwanted_keys = ["unit_type","componant_name"]
    #         value_list=data_dict
    #         try:
    #             dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
    #         except Exception as e:
    #             print("device not found  ",e)
    #         else:
    #             for key in unwanted_keys:
    #                 if key in data_dict.keys():
    #                     del data_dict[key]
                        
    #             deviceid = None
    #             deviceid=dinfo.Device_id
    #             if deviceid:
    #                 mqttc.publish(f'wc1/{deviceid}/chgset/cnd_consen',str(data_dict).replace(' ',''))
    #                 dd=dateandtime()
    #                 e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} cnd_consen settings change has been requested - span:{value_list['spn']}, atert_setpoint:{value_list['asp']}"
    #                 erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='cnd_consen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
    #                 erro.save()
    #                 try:
    #                     value_list['componant_name'] = 'cnd_consen'
    #                     value_list['device_id'] = deviceid
    #                     value_list['company_id'] = request.user.company_id
    #                     cnd_consen_setting.objects.create(**value_list)
    #                     return Response({"message": "NEW CND_CONSEN SETTING API 200"})
    #                 except Exception as e:
    #                     print("error while saving cnd sen record   ",e)
                
    #     except Exception as e:
    #         print("Error in cnd_consen SETTING API  ",e)


@api_view(['POST'])
def newupdated_disp_cnd_consenViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = data
        # value_list = list(data.values())

        dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()


        if dinfo:

            did = dinfo.Device_id
            qs_sta = disp_cnd_consen.objects.filter(device_id=did, message_type="updsta").values('cnd','created_at','updated_at').order_by('-id')[:1:1]
            if qs_sta:
                qs_sta_final = qs_sta[0]
            else:
                qs_sta_final= {}
            qs_set = disp_cnd_consen.objects.filter(device_id=did, message_type="updset").values('spn','asp','created_at','updated_at').order_by('-id')[:1:1]
            if qs_set:
                qs_set_final = qs_set[0]
            else:
                qs_set_final= {}

            last_error = Errors.objects.filter(service='cnd_consen').values('message_type','e_discriptions','o_message','service','year','month','day','hour','minit','second')
            if last_error:
                last_error_final = last_error[0]
            else:
                last_error_final= {}
            data_final = {'data_sta': qs_sta_final, 'data_set': qs_set_final, 'error': last_error_final}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 404,
                'message': "Device not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError as e:
        print("JSON Decode Error in updated_disp_cnd_consenViewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_disp_cnd_consenViewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#panel
@api_view(['POST'])
def newpanelsettingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            value_list = data_dict
            print("**!!!**")
            print("company_id",request.user.company_id)
            print("datais:",value_list)
            # dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            if dinfo is not None:
                device_final_data = {}
                if 'mod' in value_list:
                    device_final_data['mod'] = value_list['mod']
                else:
                    device_final_data['mod'] = ''
                if 'unv' in value_list:
                    device_final_data['unv'] = value_list['unv']
                else:
                    device_final_data['unv'] = ''
                if 'ovv' in value_list:
                    device_final_data['ovv'] = value_list['ovv']
                else:
                    device_final_data['ovv'] = ''
                if 'spn' in value_list:
                    device_final_data['spn'] = value_list['spn']
                else:
                    device_final_data['spn'] = ''
                if 'nmv' in value_list:
                    device_final_data['nmv'] = value_list['nmv']
                else:
                    device_final_data['nmv'] = ''
                if 'stp' in value_list:
                    device_final_data['stp'] = value_list['stp']
                else:
                    device_final_data['stp'] = ''
                # device_final_data['srt'] = value_list['srt']
                if 'srt' in value_list:
                    data_srt  = value_list['srt']
                    print("ATM data_srt.replace("", "")",data_srt.replace(":", ""))
                    device_final_data['srt'] = data_srt.replace(":", "")
                else:
                    device_final_data['srt'] = ''
                if 'bkt' in value_list:
                    device_final_data['bkt'] = value_list['bkt']
                else:
                    device_final_data['bkt'] = ''
                if 'rst' in value_list:
                    device_final_data['rst'] = value_list['rst']
                else:
                    device_final_data['rst'] = ''
                    
                for key, value in device_final_data.items():
                    value = str(value)
                    temp = value.isalnum()
                    if  temp is not False:
                        value.replace('"', "'")
                        value.replace(' ','')
                        device_final_data[key] = value
                    else:
                        device_final_data[key] = ''
                        # pass

                deviceid = None
                deviceid = dinfo.Device_id

                if deviceid:
                    print("srt is:",str(device_final_data))
                    mqttc.publish(f'wc1/{deviceid}/chgset/panel',str(device_final_data).replace(' ',''))
                    # dd=dateandtime()
                    # e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} panel_setting  change has been requested - mod:{value_list['mod']}, Under Voltage:{value_list['unv']}, Over Voltage:{value_list['ovv']}, Span:{value_list['spn']}, No.of Multiport valve:{value_list['nmv']}, Sensor Type:{value_list['stp']}, Service Time:{value_list['srt']}, Backwash Time:{value_list['bkt']}, Rinse Time:{value_list['rst']}"
                    # erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='panel_setting',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    # erro.save()
                    try:
                        value_list_final = {}
                        if 'srt' in value_list:
                            data_srt  = value_list['srt']
                            print("data_srt.replace("", "")",data_srt.replace(":", ""))
                            value_list_final['srt'] = data_srt.replace(":", "")
                        if 'mod' in value_list:
                            value_list_final['mod'] = value_list['mod']
                        if 'unv' in value_list:
                            value_list_final['unv'] = value_list['unv']
                        if 'ovv' in value_list:
                            value_list_final['ovv'] = value_list['ovv']
                        if 'spn' in value_list:
                            value_list_final['spn'] = value_list['spn']
                        if'nmv' in value_list:
                            value_list_final['nmv'] = value_list['nmv']
                        if 'stp' in value_list:
                            value_list_final['stp'] = value_list['stp']
                        # value_list_final['srt'] = value_list['srt']
                        if 'bkt' in value_list:
                            value_list_final['bkt'] = value_list['bkt']
                        if 'rst' in value_list:
                            value_list_final['rst'] = value_list['rst']
                        value_list_final['componant_name'] = 'panel_setting'
                        value_list_final['unit_type'] = 'water_treatment'
                        value_list_final['device_id'] = deviceid
                        value_list_final['company_id'] = request.user.company_id
                        panel_setting.objects.create(**value_list_final)
                        return Response({"message": "NEW panel_setting SETTING API 200"})
                    except Exception as e:
                        print("error while saving panel_setting record ",e)
        except Exception as e:
            print("Error in panel_settingsetting ",e)    

    # if request.method == 'POST':
    #     try:
    #         data_dict = json.loads(request.body)
    #         unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
    #         value_list=list(data_dict.values())
    #         dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
    #         if dinfo is not None:
    #             obj = panel_setting.objects.create(**data_dict)
    #             for key in unwanted_keys:
    #                 if key in data_dict.keys():
    #                     del data_dict[key]
                
    #             deviceid = None
    #             deviceid=dinfo.Device_id
    #             if deviceid:
    #                 mqttc.publish(f'wc1/{deviceid}/chgset/panel',str(data_dict).replace(' ',''))
    #                 dd=dateandtime()
    #                 e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} panel settings change has been requested - mode:{value_list[3]}, under voltage:{value_list[6]}, over voltage:{value_list[7]}, span:{value_list[8]}, no.of multiport valve:{value_list[4]}, sensor type:{value_list[5]}, service time:{value_list[9]}, backwash time:{value_list[10]}, rinse time:{value_list[11]}"
    #                 erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='panel',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
    #                 erro.save()

    #                 obj.unit_type = value_list[0]
    #                 obj.componant_name = value_list[1]
    #                 obj.device_id = deviceid
    #                 obj.company_id = request.user.company_id
    #                 obj.save()
    #             return Response({"message": "newpanelsetting API 200"})
    #     except Exception as e:
    #         print("Error in newpanelsetting API  ",e)


@api_view(['POST'])
def newupdated_treat_panelViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = data

        dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()


        if dinfo:

            did = dinfo.Device_id
            qs_sta = treat_panel.objects.filter(device_id=did, message_type="updsta").values('sts','rtl','ttl','lps','hps','dgp','ipv','err','created_at','updated_at').order_by('-id')[:1:1]
            if qs_sta:
                qs_sta_final = qs_sta[0]
            else:
                qs_sta_final= {}
            qs_set = treat_panel.objects.filter(device_id=did, message_type="updset").values('mod','unv','ovv','spn','nmv','stp','srt','bkt','rst','created_at','updated_at').order_by('-id')[:1:1]
            if qs_set:
                qs_set_final = qs_set[0]
            else:
                qs_set_final= {}

            last_error = Errors.objects.filter(service='panel').values('message_type','e_discriptions','o_message','service','year','month','day','hour','minit','second')
            if last_error:
                last_error_final = last_error[0]
            else:
                last_error_final= {}
            data_final = {'data_sta': qs_sta_final, 'data_set': qs_set_final, 'error': last_error_final}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 404,
                'message': "Device not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError as e:
        print("JSON Decode Error in updated_treat_panelViewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_treat_panelViewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#FeedFlowSensor
@api_view(['POST'])
def newFflowsensettingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            value_list = data_dict
           
            dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            if dinfo is not None:

                device_final_data = {}
                # device_final_data['fr1'] = value_list['fr1']
                if 'ff1' in value_list:
                    device_final_data['ff1'] = value_list['ff1']
                else:
                    device_final_data['ff1'] = ''

                for key, value in device_final_data.items():
                    value = str(value)
                    temp = value.isalnum()
                    if  temp is not False:
                        value.replace('"', "'")
                        value.replace(' ','')
                        device_final_data[key] = value
                    else:
                        device_final_data[key] = ''

                deviceid = None
                deviceid = dinfo.Device_id

                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/F_flowsen',str(device_final_data).replace(' ',''))
                    # dd=dateandtime()
                    # e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} F_flowsen settings change has been requested - ff1:{value_list['ff1']}"
                    # erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='F_flowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    # erro.save()
                    try:
                        value_list_final = {}
                        # value_list_final['fr1'] = value_list['fr1']
                        if 'ff1' in value_list:
                            value_list_final['ff1'] = value_list['ff1']
                        value_list_final['componant_name'] = 'F_flowsen'
                        value_list_final['unit_type'] = 'water_treatment'
                        value_list_final['device_id'] = deviceid
                        value_list_final['company_id'] = request.user.company_id
                        F_flowsen_setting.objects.create(**value_list_final)
                        return Response({"message": "NEW F_flowsen API 200"})
                    except Exception as e:
                        print("Error in F_flowsensetting ",e) 
        except Exception as e:
            print("Error in F_flowsensetting ",e)    

    # if request.method == 'POST':
    #     try:
    #         data_dict = json.loads(request.body)
    #         unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
    #         value_list=list(data_dict.values())
    #         dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
    #         if dinfo is not None:
    #             obj = F_flowsen_setting.objects.create(**data_dict)
    #             for key in unwanted_keys:
    #                 if key in data_dict.keys():
    #                     del data_dict[key]
                
    #             deviceid = None
    #             deviceid=dinfo.Device_id
    #             if deviceid:
    #                 mqttc.publish(f'wc1/{deviceid}/chgset/F_flowsen',str(data_dict).replace(' ',''))
    #                 dd=dateandtime()
    #                 e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Fflowsen settings change has been requested - flow factor:{value_list[3]}"
    #                 erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='Fflowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
    #                 erro.save()

    #                 obj.unit_type = value_list[0]
    #                 obj.componant_name = value_list[1]
    #                 obj.device_id = deviceid
    #                 obj.company_id = request.user.company_id
    #                 obj.save()
    #             return Response({"message": "newFflowsensettingViewset API 200"})
    #     except Exception as e:
    #         print("Error in newFflowsensettingViewset API  ",e)


@api_view(['POST'])
def newupdated_treat_F_flowsenViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = data

        dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()


        if dinfo:

            did = dinfo.Device_id
            qs_sta = treat_F_flowsen.objects.filter(device_id=did, message_type="updsta").values('fr1','created_at','updated_at').order_by('-id')[:1:1]
            if qs_sta:
                qs_sta_final = qs_sta[0]
            else:
                qs_sta_final= {}
            qs_set = treat_F_flowsen.objects.filter(device_id=did, message_type="updset").values('ff1','created_at','updated_at').order_by('-id')[:1:1]
            if qs_set:
                qs_set_final = qs_set[0]
            else:
                qs_set_final= {}

            last_error = Errors.objects.filter(service='F_flowsen').values('message_type','e_discriptions','o_message','service','year','month','day','hour','minit','second')
            if last_error:
                last_error_final = last_error[0]
            else:
                last_error_final= {}
            data_final = {'data_sta': qs_sta_final, 'data_set': qs_set_final, 'error': last_error_final}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 404,
                'message': "Device not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError as e:
        print("JSON Decode Error in updated_treat_F_flowsenViewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_treat_F_flowsenViewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#P_FlowSensor
@api_view(['POST'])
def newPflowsensettingViewset(request):
    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            value_list = data_dict
           
            dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()
            if dinfo is not None:

                device_final_data = {}
                # device_final_data['fr2'] = value_list['fr2']
                if 'ff2' in value_list:
                    device_final_data['ff2'] = value_list['ff2']
                else:
                    device_final_data['ff2'] = ''


                for key, value in device_final_data.items():
                    value = str(value)
                    temp = value.isalnum()
                    if  temp is not False:
                        value.replace('"', "'")
                        value.replace(' ','')
                        device_final_data[key] = value
                    else:
                        device_final_data[key] = ''

                deviceid = None
                deviceid = dinfo.Device_id

                if deviceid:
                    mqttc.publish(f'wc1/{deviceid}/chgset/P_flowsen',str(device_final_data).replace(' ',''))
                    # dd=dateandtime()
                    # e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} P_flowsen settings change has been requested - ff2:{value_list['ff2']}"
                    # erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='p_flowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                    # erro.save()
                    try:
                        value_list_final = {}
                        # value_list_final['fr2'] = value_list['fr2']
                        if 'ff2' in value_list:
                            value_list_final['ff2'] = value_list['ff2']
                        value_list_final['componant_name'] = 'p_flowsen'
                        value_list_final['unit_type'] = 'water_treatment'
                        value_list_final['device_id'] = deviceid
                        value_list_final['company_id'] = request.user.company_id
                        P_flowsen_setting.objects.create(**value_list_final)
                        return Response({"message": "NEW p_flowsen API 200"})
                    except Exception as e:
                        print("Error in p_flowsensetting ",e) 
        except Exception as e:
            print("Error in p_flowsensetting ",e)    

    # if request.method == 'POST':
    #     try:
    #         data_dict = json.loads(request.body)
    #         unwanted_keys = ["unit_type", "water_treatment","company_id","componant_name","site_name","device_id"]
    #         value_list=list(data_dict.values())
    #         dinfo = device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
    #         if dinfo is not None:
    #             obj = P_flowsen_setting.objects.create(**data_dict)
    #             for key in unwanted_keys:
    #                 if key in data_dict.keys():
    #                     del data_dict[key]
                
    #             deviceid = None
    #             deviceid=dinfo.Device_id
    #             if deviceid:
    #                 mqttc.publish(f'wc1/{deviceid}/chgset/P_flowsen',str(data_dict).replace(' ',''))
    #                 dd=dateandtime()
    #                 e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} Fflowsen settings change has been requested - flow factor:{value_list[3]}"
    #                 erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='Pflowsen',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
    #                 erro.save()

    #                 obj.unit_type = value_list[0]
    #                 obj.componant_name = value_list[1]
    #                 obj.device_id = deviceid
    #                 obj.company_id = request.user.company_id
    #                 obj.save()
    #             return Response({"message": "newPflowsensettingViewset API 200"})
    #     except Exception as e:
    #         print("Error in newPflowsensettingViewset API  ",e)


@api_view(['POST'])
def newupdated_treat_P_flowsenViewset(request):
    try:
        fields_to_exclude = ['model', 'pk']
        data = json.loads(request.body)
        value_list = data

        dinfo = device_info.objects.filter(site_name=value_list['site_name'],unit_type=value_list['unit_type'],company_id=request.user.company_id).first()


        if dinfo:

            did = dinfo.Device_id
            qs_sta = treat_P_flowsen.objects.filter(device_id=did, message_type="updsta").values('fr2','created_at','updated_at').order_by('-id')[:1:1]
            if qs_sta:
                qs_sta_final = qs_sta[0]
            else:
                qs_sta_final= {}
            qs_set = treat_P_flowsen.objects.filter(device_id=did, message_type="updset").values('ff2','created_at','updated_at').order_by('-id')[:1:1]
            if qs_set:
                qs_set_final = qs_set[0]
            else:
                qs_set_final= {}

            last_error = Errors.objects.filter(service='P_flowsen').values('message_type','e_discriptions','o_message','service','year','month','day','hour','minit','second')
            if last_error:
                last_error_final = last_error[0]
            else:
                last_error_final= {}
            data_final = {'data_sta': qs_sta_final, 'data_set': qs_set_final, 'error': last_error_final}
            response_data = {
                'data': data_final,
                'status': 200,
                'message': "Data get successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'data': "",
                'status': 404,
                'message': "Device not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError as e:
        print("JSON Decode Error in updated_treat_P_flowsenViewset:", e)
        return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Exception in updated_treat_P_flowsenViewset:", e)
        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

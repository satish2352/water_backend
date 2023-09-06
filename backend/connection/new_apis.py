from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from datetime import datetime
from connection.views import mqttc
def dateandtime():
    year=datetime.today().strftime('%Y')
    month=datetime.today().strftime('%m')
    day=datetime.today().strftime('%d')
    hour=datetime.now().strftime('%H')
    minit=datetime.now().strftime('%M')
    second=datetime.now().strftime('%S')
    return year,month,day,hour,minit,second

@api_view(['GET', 'POST'])
def newtap1settingViewset(request):

    if request.method == 'POST':
        try:
            data_dict = json.loads(request.body)
            unwanted_keys = ["unit_type", "water_treatment","componant_name","site_name","device_id"]
            for key in unwanted_keys:
                        if key in data_dict.keys():
                            del data_dict[key]
            obj = tap1_setting.objects.create(**data_dict)
            value_list=list(data_dict.values())
            print("value_list value_list",value_list)
            dinfo=device_info.objects.filter(unit_type=value_list[0],company_id=request.user.company_id).first()
            deviceid = None
            deviceid=dinfo.Device_id
            print("deviceid ",deviceid)
            if deviceid:
                mqttc.publish(f'wc1/{deviceid}/chgset/tap1',str(data_dict).replace(' ',''))
                dd=dateandtime()
                e=f"{dd[0]}-{dd[1]}-{dd[2]} {dd[3]}:{dd[4]}:{dd[5]} tap1 settings change has been requested - pulse1:{value_list[3]}, pulse2:{value_list[4]}, pulse3:{value_list[5]}, pulse4:{value_list[6]}"
                erro=Errors.objects.create(device_id=deviceid,e_discriptions=e,service='tap1',year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minit=dd[4],second=dd[5])
                erro.save()

                obj.unit_type = value_list[0]
                obj.componant_name = value_list[1]
                obj.componant_name = value_list[1]
                obj.device_id = deviceid
                obj.company_id = request.user.company_id
                obj.save()
            return Response({"message": "NEW TAP-1 API 200"})
        except Exception as e:
            print("Error in tap1setting ",e)    







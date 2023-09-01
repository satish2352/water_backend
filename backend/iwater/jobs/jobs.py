from django.conf import settings 
#from rest_framework import status
from iwater.models import Site, Subscription, Price, Order, PaymentStatus, Device




def sub_update_scheduler():
    Treatment_Unit_Active = []
    Treatment_Unit_Expired = []
    Treatment_Unit_Free_Trial = []
    Dispensing_Unit_Active = []
    Dispensing_Unit_Expired = []
    Dispensing_Unit_Free_Trial = []

       

        
          
    showdata = Site.objects.all().values('id')
    
    for a in showdata:
            ##---------------------Under Implement code with aseem Sir Logic------------------------------------------------------
            # sub = Subscription.objects.filter(site_id =a["id"],is_treatment_unit=1).order_by('-days_to_expire').values('site_id','days_to_expire','order_id')
            # sub1 = sub[0]
            # dte = sub1('days_to_expire')
            # o_id = sub1('order_id')
            ##---------------------Above Implement code with aseem Sir Logic------------------------------------------------------
        obj1= Subscription.objects.filter(site_id = a['id'],is_treatment_unit=1).order_by('-days_to_expire').values('site_id','days_to_expire','order_id')
        if len(obj1) !=0:
            
            sub1 = obj1[0] 
            

            if(sub1["days_to_expire"]>0 and sub1["order_id"]!=None):
            ##---------------------Under Implement code with aseem Sir Logic------------------------------------------------------
                div1= Device.objects.filter(site= a['id']).update(device2_sub_status="Active")
                Treatment_Unit_Active.append(div1)
    
            elif(sub1["days_to_expire"]<=0):
                div2= Device.objects.filter(site= a['id']).update(device2_sub_status="Expired")
                Treatment_Unit_Expired.append(div2)

            elif(sub1["days_to_expire"]>0 and sub1["order_id"]==None):
                div3= Device.objects.filter(site= a['id']).update(device2_sub_status="Free_Trial")
                Treatment_Unit_Free_Trial.append(div3)
        else:
            ("NO Data found for Treatment Unit")
        


        obj2= Subscription.objects.filter(site_id = a['id'],is_dispensing_unit=1).order_by('-days_to_expire').values('site_id','days_to_expire','order_id')
        if len(obj2)!=0 :
            
            sub2 = obj2[0] 
            
            if(sub2["days_to_expire"]>0 and sub2["order_id"]!=None):
            ##---------------------Under Implement code with aseem Sir Logic------------------------------------------------------
                div4= Device.objects.filter(site= a['id']).update(device3_sub_status="Active")
                Dispensing_Unit_Active.append(div4) 
    
            elif(sub2["days_to_expire"]<=0):
                div5= Device.objects.filter(site= a['id']).update(device3_sub_status="Expired")
                Dispensing_Unit_Expired.append(div5)
                

            
            elif(sub2["days_to_expire"]>0 and sub2["order_id"]==None):
                div6= Device.objects.filter(site= a['id']).update(device3_sub_status="Free_Trial")
                Dispensing_Unit_Free_Trial.append(div6)
        else:
            ("NO Data found for Dispensing Unit")

    context = { 
            'Treatment_Unit_Active':Treatment_Unit_Active,
            'Treatment_Unit_Expired':Treatment_Unit_Expired,
            'Treatment_Unit_Free_Trial':Treatment_Unit_Free_Trial,
            'Dispensing_Unit_Active':Dispensing_Unit_Active,      
            'Dispensing_Unit_Expired':Dispensing_Unit_Expired,         
            'Dispensing_Unit_Free_Trial':Dispensing_Unit_Free_Trial,
            }
   
    

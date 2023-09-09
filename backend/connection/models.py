from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# from . import django_init
# from django_init import *
import json
from django.contrib.auth.models import User
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email_id=models.EmailField(max_length=254)
    
    # class Meta:
    #     app_label = 'devices'

class user_information(models.Model):
    # User_id=models.OneToOneField(User,on_delete=models.CASCADE)
    User_id=models.ForeignKey(User,on_delete=models.CASCADE)
    # users=models.ForeignKey(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)

    def __str__(self):
        return self.User_id.username
    # class Meta:
    #     app_label = 'devices'
class treat_cnd_sen(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    cnd=models.BigIntegerField(null=True,default=None,blank=True)
    spn=models.BigIntegerField(null=True,default=None,blank=True)
    tsp=models.BigIntegerField(null=True,default=None,blank=True)
    asp=models.BigIntegerField(null=True,default=None,blank=True)
    # sensor_type=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
        # collection = 'treat_cnd_sen'

class treat_tds_sen(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    tds=models.BigIntegerField(null=True,default=None,blank=True)
    spn=models.BigIntegerField(null=True,default=None,blank=True)
    tsp=models.BigIntegerField(null=True,default=None,blank=True)
    asp=models.BigIntegerField(null=True,default=None,blank=True)
    # sensor_type=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tds_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    tds=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    tsp=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.cnd,self.spn,self.tsp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class tds_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    tds=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    tsp=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.tds,self.spn,self.tsp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tds_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    tds=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    tsp=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.tds,self.spn,self.tsp,self.created_at,self.updated_at
    
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tds_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    tds=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    tsp=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.tds,self.spn,self.tsp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class treat_tds(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    tds=models.BigIntegerField(null=True,default=None,blank=True)
    spn=models.BigIntegerField(null=True,default=None,blank=True)
    tsp=models.BigIntegerField(null=True,default=None,blank=True)
    asp=models.BigIntegerField(null=True,default=None,blank=True)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class topics(models.Model):
    Topic_name=models.CharField(max_length=100)    


    def __str__(self):
        return self.Topic_name
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class disp_atm(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    sts=models.CharField(max_length=50,null=True,default=None,blank=True)
    ndv=models.BigIntegerField(null=True,default=None,blank=True)
    ntt=models.CharField(max_length=50,null=True,default=None,blank=True)
    nta=models.BigIntegerField(null=True,default=None,blank=True)
    tmp=models.BigIntegerField(null=True,default=None,blank=True)
    whr=models.CharField(max_length=50,null=True,default=None,blank=True)
    custid=models.CharField(max_length=50,null=True,default=None,blank=True)
    ntp=models.BigIntegerField(null=True,default=None,blank=True)
    nov=models.BigIntegerField(null=True,default=None,blank=True)
    vl1=models.BigIntegerField(null=True,default=None,blank=True)
    vl2=models.BigIntegerField(null=True,default=None,blank=True)
    vl3=models.BigIntegerField(null=True,default=None,blank=True)
    vl4=models.BigIntegerField(null=True,default=None,blank=True)
    re1=models.BigIntegerField(null=True,default=None,blank=True)
    re2=models.BigIntegerField(null=True,default=None,blank=True)
    re3=models.BigIntegerField(null=True,default=None,blank=True)
    re4=models.BigIntegerField(null=True,default=None,blank=True) 
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class disp_tap1(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    p1=models.BigIntegerField(null=True,default=None,blank=True)
    p2=models.BigIntegerField(null=True,default=None,blank=True)
    p3=models.BigIntegerField(null=True,default=None,blank=True)
    p4=models.BigIntegerField(null=True,default=None,blank=True)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class disp_tap2(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    p1=models.BigIntegerField(null=True,default=None,blank=True)
    p2=models.BigIntegerField(null=True,default=None,blank=True)
    p3=models.BigIntegerField(null=True,default=None,blank=True)
    p4=models.BigIntegerField(null=True,default=None,blank=True)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class disp_tap3(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    p1=models.BigIntegerField(null=True,default=None,blank=True)
    p2=models.BigIntegerField(null=True,default=None,blank=True)
    p3=models.BigIntegerField(null=True,default=None,blank=True)
    p4=models.BigIntegerField(null=True,default=None,blank=True)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class disp_tap4(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    p1=models.BigIntegerField(null=True,default=None,blank=True)
    p2=models.BigIntegerField(null=True,default=None,blank=True)
    p3=models.BigIntegerField(null=True,default=None,blank=True)
    p4=models.BigIntegerField(null=True,default=None,blank=True)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class disp_cnd_consen(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    cnd=models.BigIntegerField(null=True,default=None,blank=True)
    spn=models.BigIntegerField(null=True,default=None,blank=True)
    asp=models.BigIntegerField(null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class disp_tds_consen(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    tds=models.BigIntegerField(null=True,default=None,blank=True)
    spn=models.BigIntegerField(null=True,default=None,blank=True)
    asp=models.BigIntegerField(null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class cnd_consen_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    cnd=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.device_id,self.service,self.cnd,self.spn,self.asp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tds_consen_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    tds=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.device_id,self.service,self.tds,self.spn,self.asp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class cnd_consen_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    cnd=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.device_id,self.service,self.cnd,self.spn,self.asp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
# class tds_consen_repo_daily(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     tds=models.JSONField(null=True,default=None,blank=True)
#     spn=models.JSONField(null=True,default=None,blank=True)
#     asp=models.JSONField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)
#     def __str__(self) -> str:
#         return self.device_id,self.service,self.tds,self.spn,self.asp,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'

class treat_ampv1(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    pos=models.CharField(max_length=50,null=True,default=None,blank=True)
    rmt=models.BigIntegerField(null=True,default=None,blank=True)
    cct=models.BigIntegerField(null=True,default=None,blank=True)
    srt=models.CharField(max_length=50,null=True,default=None,blank=True)
    bkt=models.BigIntegerField(null=True,default=None,blank=True)
    rst=models.BigIntegerField(null=True,default=None,blank=True)
    mot=models.BigIntegerField(null=True,default=None,blank=True)
    stp=models.CharField(max_length=50,null=True,default=None,blank=True)
    op1=models.CharField(max_length=50,null=True,default=None,blank=True)
    op2=models.CharField(max_length=50,null=True,default=None,blank=True)
    op3=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip1=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip2=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip3=models.CharField(max_length=50,null=True,default=None,blank=True)
    psi=models.CharField(max_length=50,null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class treat_ampv2(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    pos=models.CharField(max_length=50,null=True,default=None,blank=True)
    rmt=models.BigIntegerField(null=True,default=None,blank=True)
    cct=models.BigIntegerField(null=True,default=None,blank=True)
    srt=models.CharField(max_length=50,null=True,default=None,blank=True)
    bkt=models.BigIntegerField(null=True,default=None,blank=True)
    rst=models.BigIntegerField(null=True,default=None,blank=True)
    mot=models.BigIntegerField(null=True,default=None,blank=True)
    stp=models.CharField(max_length=50,null=True,default=None,blank=True)
    op1=models.CharField(max_length=50,null=True,default=None,blank=True)
    op2=models.CharField(max_length=50,null=True,default=None,blank=True)
    op3=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip1=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip2=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip3=models.CharField(max_length=50,null=True,default=None,blank=True)
    psi=models.CharField(max_length=50,null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class treat_ampv3(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    pos=models.CharField(max_length=50,null=True,default=None,blank=True)
    rmt=models.BigIntegerField(null=True,default=None,blank=True)
    cct=models.BigIntegerField(null=True,default=None,blank=True)
    srt=models.BigIntegerField(null=True,default=None,blank=True)
    bkt=models.BigIntegerField(null=True,default=None,blank=True)
    rst=models.BigIntegerField(null=True,default=None,blank=True)
    mot=models.BigIntegerField(null=True,default=None,blank=True)
    stp=models.CharField(max_length=50,null=True,default=None,blank=True)
    op1=models.CharField(max_length=50,null=True,default=None,blank=True)
    op2=models.CharField(max_length=50,null=True,default=None,blank=True)
    op3=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip1=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip2=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip3=models.CharField(max_length=50,null=True,default=None,blank=True)
    psi=models.CharField(max_length=50,null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class treat_ampv4(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    pos=models.CharField(max_length=50,null=True,default=None,blank=True)
    rmt=models.BigIntegerField(null=True,default=None,blank=True)
    cct=models.BigIntegerField(null=True,default=None,blank=True)
    srt=models.BigIntegerField(null=True,default=None,blank=True)
    bkt=models.BigIntegerField(null=True,default=None,blank=True)
    rst=models.BigIntegerField(null=True,default=None,blank=True)
    mot=models.BigIntegerField(null=True,default=None,blank=True)
    stp=models.CharField(max_length=50,null=True,default=None,blank=True)
    op1=models.CharField(max_length=50,null=True,default=None,blank=True)
    op2=models.CharField(max_length=50,null=True,default=None,blank=True)
    op3=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip1=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip2=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip3=models.CharField(max_length=50,null=True,default=None,blank=True)
    psi=models.CharField(max_length=50,null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class treat_ampv5(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    pos=models.CharField(max_length=50,null=True,default=None,blank=True)
    rmt=models.BigIntegerField(null=True,default=None,blank=True)
    cct=models.BigIntegerField(null=True,default=None,blank=True)
    srt=models.BigIntegerField(null=True,default=None,blank=True)
    bkt=models.BigIntegerField(null=True,default=None,blank=True)
    rst=models.BigIntegerField(null=True,default=None,blank=True)
    mot=models.BigIntegerField(null=True,default=None,blank=True)
    stp=models.CharField(max_length=50,null=True,default=None,blank=True)
    op1=models.CharField(max_length=50,null=True,default=None,blank=True)
    op2=models.CharField(max_length=50,null=True,default=None,blank=True)
    op3=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip1=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip2=models.CharField(max_length=50,null=True,default=None,blank=True)
    ip3=models.CharField(max_length=50,null=True,default=None,blank=True)
    psi=models.CharField(max_length=50,null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class treat_rwp(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    sts=models.CharField(max_length=50,null=True,default=None,blank=True)
    crt=models.BigIntegerField(null=True,default=None,blank=True)
    olc=models.BigIntegerField(null=True,default=None,blank=True)
    drc=models.BigIntegerField(null=True,default=None,blank=True)
    spn=models.BigIntegerField(null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class treat_hpp(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    sts=models.CharField(max_length=50,null=True,default=None,blank=True)
    crt=models.BigIntegerField(null=True,default=None,blank=True)
    olc=models.BigIntegerField(null=True,default=None,blank=True)
    drc=models.BigIntegerField(null=True,default=None,blank=True)
    spn=models.BigIntegerField(null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class treat_panel(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    sts=models.CharField(max_length=50,null=True,default=None,blank=True)
    rtl=models.CharField(max_length=50,null=True,default=None,blank=True)
    ttl=models.CharField(max_length=50,null=True,default=None,blank=True)
    lps=models.CharField(max_length=50,null=True,default=None,blank=True)
    hps=models.CharField(max_length=50,null=True,default=None,blank=True)
    dgp=models.CharField(max_length=50,null=True,default=None,blank=True)
    mod=models.CharField(max_length=50,null=True,default=None,blank=True)
    ipv=models.BigIntegerField(null=True,default=None,blank=True)
    unv=models.BigIntegerField(null=True,default=None,blank=True)
    ovv=models.BigIntegerField(null=True,default=None,blank=True)
    spn=models.BigIntegerField(null=True,default=None,blank=True)
    nmv=models.BigIntegerField(null=True,default=None,blank=True)
    stp=models.CharField(max_length=50,null=True,default=None,blank=True)
    srt=models.CharField(max_length=50,null=True,default=None,blank=True)
    bkt=models.BigIntegerField(null=True,default=None,blank=True)
    rst=models.BigIntegerField(null=True,default=None,blank=True)
    err=models.CharField(max_length=50,null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class treat_P_flowsen(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    fr2=models.FloatField(null=True,default=None,blank=True)
    ff2=models.FloatField(null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class repo_latestdata(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    cnd_sen=models.JSONField(null=True,default=None,blank=True)
    tds_sen=models.JSONField(null=True,default=None,blank=True)
    rwp=models.JSONField(null=True,default=None,blank=True)
    hpp=models.JSONField(null=True,default=None,blank=True)
    panel=models.JSONField(null=True,default=None,blank=True)
    flowsen=models.JSONField(null=True,default=None,blank=True)
    ampv1=models.JSONField(null=True,default=None,blank=True)
    ampv2=models.JSONField(null=True,default=None,blank=True)
    ampv3=models.JSONField(null=True,default=None,blank=True)
    ampv4=models.JSONField(null=True,default=None,blank=True)
    ampv5=models.JSONField(null=True,default=None,blank=True)
    atm=models.JSONField(null=True,default=None,blank=True)
    tap1=models.JSONField(null=True,default=None,blank=True)
    tap2=models.JSONField(null=True,default=None,blank=True)
    tap3=models.JSONField(null=True,default=None,blank=True)
    tap4=models.JSONField(null=True,default=None,blank=True)
    # consen=models.JSONField(null=True,default=None,blank=True)
    cnd_consen=models.JSONField(null=True,default=None,blank=True)
    tds_consen=models.JSONField(null=True,default=None,blank=True)
    F_flowsen=models.JSONField(null=True,default=None,blank=True)
    P_flowsen=models.JSONField(null=True,default=None,blank=True)
    flowsen1=models.JSONField(null=True,default=None,blank=True)
    flowsen2=models.JSONField(null=True,default=None,blank=True)
    flowsen3=models.JSONField(null=True,default=None,blank=True)
    flowsen4=models.JSONField(null=True,default=None,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.device_id,self.message_type,self.cnd_sen,self.rwp,self.hpp,self.panel,self.flowsen,self.ampv1,self.ampv2,self.ampv3,self.ampv4,self.ampv5,self.atm,self.tap1,self.tap2,self.tap3,self.tap4,self.consen
    
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class repo_history(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    component_name=models.CharField(max_length=100)
    msg_json=models.JSONField(null=True,default=None,blank=True)
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
# class cnd_tds_repo_hourly(models.Model):
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     sum_cnd=models.BigIntegerField(null=True,default=None,blank=True)
#     sum_spn=models.BigIntegerField(null=True,default=None,blank=True)
#     sum_tsp=models.BigIntegerField(null=True,default=None,blank=True)
#     sum_asp=models.BigIntegerField(null=True,default=None,blank=True)
#     count=models.BigIntegerField(null=True,default=None,blank=True)
#     avg_cnd=models.FloatField(null=True,default=None,blank=True)
#     avg_spn=models.FloatField(null=True,default=None,blank=True)
#     avg_tsp=models.FloatField(null=True,default=None,blank=True)
#     avg_asp=models.FloatField(null=True,default=None,blank=True)
#     # avg=models.f(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)

#     def __str__(self) -> str:
#         return self.device_id,self.service,self.sum_cnd,self.count,self.avg_cnd,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class cnd_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    cnd=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    tsp=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.cnd,self.spn,self.tsp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class rwp_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    crt=models.JSONField(null=True,default=None,blank=True)
    olc=models.JSONField(null=True,default=None,blank=True)
    drc=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.crt,self.spn,self.olc,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class rwp_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    crt=models.JSONField(null=True,default=None,blank=True)
    olc=models.JSONField(null=True,default=None,blank=True)
    drc=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.crt,self.spn,self.olc,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class rwp_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    crt=models.JSONField(null=True,default=None,blank=True)
    olc=models.JSONField(null=True,default=None,blank=True)
    drc=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.crt,self.spn,self.olc,self.created_at,self.updated_at

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class rwp_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    crt=models.JSONField(null=True,default=None,blank=True)
    olc=models.JSONField(null=True,default=None,blank=True)
    drc=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.crt,self.spn,self.olc,self.created_at,self.updated_at


    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class hpp_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    crt=models.JSONField(null=True,default=None,blank=True)
    olc=models.JSONField(null=True,default=None,blank=True)
    drc=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.crt,self.spn,self.olc,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class hpp_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    crt=models.JSONField(null=True,default=None,blank=True)
    olc=models.JSONField(null=True,default=None,blank=True)
    drc=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.crt,self.spn,self.olc,self.created_at,self.updated_at

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class hpp_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    crt=models.JSONField(null=True,default=None,blank=True)
    olc=models.JSONField(null=True,default=None,blank=True)
    drc=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.crt,self.spn,self.olc,self.created_at,self.updated_at

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class hpp_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    crt=models.JSONField(null=True,default=None,blank=True)
    olc=models.JSONField(null=True,default=None,blank=True)
    drc=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.crt,self.spn,self.olc,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv1_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv1_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv1_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv1_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv2_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv2_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv2_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv2_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv3_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv3_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv3_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv3_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv4_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv4_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv4_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv4_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv5_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv5_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv5_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv5_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    rmt=models.JSONField(null=True,default=None,blank=True)
    cct=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    mot=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.rmt,self.cct,self.srt,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class F_flowsen_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr1=models.JSONField(null=True,default=None,blank=True)
    ff1=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr1,self.ff1,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class P_flowsen_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr2=models.JSONField(null=True,default=None,blank=True)
    ff2=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr2,self.ff2,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class F_flowsen_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr1=models.JSONField(null=True,default=None,blank=True)
    ff1=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr1,self.ff1,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class P_flowsen_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr2=models.JSONField(null=True,default=None,blank=True)
    ff2=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr2,self.ff2,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class F_flowsen_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr1=models.JSONField(null=True,default=None,blank=True)
    ff1=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr1,self.ff1,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class P_flowsen_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr2=models.JSONField(null=True,default=None,blank=True)
    ff2=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr2,self.ff2,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class F_flowsen_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr1=models.JSONField(null=True,default=None,blank=True)
    ff1=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr1,self.ff1,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class P_flowsen_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr2=models.JSONField(null=True,default=None,blank=True)
    ff2=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr2,self.ff2,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'


class panel_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    ipv=models.JSONField(null=True,default=None,blank=True)
    unv=models.JSONField(null=True,default=None,blank=True)
    ovv=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    nmv=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.ipv,self.spn,self.unv,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class panel_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    ipv=models.JSONField(null=True,default=None,blank=True)
    unv=models.JSONField(null=True,default=None,blank=True)
    ovv=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    nmv=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.ipv,self.spn,self.unv,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class panel_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    ipv=models.JSONField(null=True,default=None,blank=True)
    unv=models.JSONField(null=True,default=None,blank=True)
    ovv=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    nmv=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.ipv,self.spn,self.unv,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class panel_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    ipv=models.JSONField(null=True,default=None,blank=True)
    unv=models.JSONField(null=True,default=None,blank=True)
    ovv=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    nmv=models.JSONField(null=True,default=None,blank=True)
    srt=models.JSONField(null=True,default=None,blank=True)
    bkt=models.JSONField(null=True,default=None,blank=True)
    rst=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.ipv,self.spn,self.unv,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class cnd_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    cnd=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    tsp=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.cnd,self.spn,self.tsp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class cnd_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    cnd=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    tsp=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.cnd,self.spn,self.tsp,self.created_at,self.updated_at
    
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class cnd_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    cnd=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    tsp=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.cnd,self.spn,self.tsp,self.created_at,self.updated_at
# #   class Meta:
#         app_label = 'devices'
# class repo_yearly(models.Model):
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     sum=models.BigIntegerField(null=True,default=None,blank=True)
#     count=models.BigIntegerField(null=True,default=None,blank=True)
#     avg=models.FloatField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     def __str__(self) -> str:
#         return self.device_id,self.service,self.sum,self.count,self.avg,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class atm_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    ndv=models.JSONField(null=True,default=None,blank=True)
    nta=models.JSONField(null=True,default=None,blank=True)
    tmp=models.JSONField(null=True,default=None,blank=True)
    whr=models.JSONField(null=True,default=None,blank=True)
    # custid=models.CharField(max_length=50,null=True,default=None,blank=True)
    ntp=models.JSONField(null=True,default=None,blank=True)
    nov=models.JSONField(null=True,default=None,blank=True)
    vl1=models.JSONField(null=True,default=None,blank=True)
    vl2=models.JSONField(null=True,default=None,blank=True)
    vl3=models.JSONField(null=True,default=None,blank=True)
    vl4=models.JSONField(null=True,default=None,blank=True)
    re1=models.JSONField(null=True,default=None,blank=True)
    re2=models.JSONField(null=True,default=None,blank=True)
    re3=models.JSONField(null=True,default=None,blank=True)
    re4=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.ndv,self.ntp,self.nta,self.created_at,self.updated_at   
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class atm_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    ndv=models.JSONField(null=True,default=None,blank=True)
    nta=models.JSONField(null=True,default=None,blank=True)
    tmp=models.JSONField(null=True,default=None,blank=True)
    whr=models.JSONField(null=True,default=None,blank=True)
    # custid=models.CharField(max_length=50,null=True,default=None,blank=True)
    ntp=models.JSONField(null=True,default=None,blank=True)
    nov=models.JSONField(null=True,default=None,blank=True)
    vl1=models.JSONField(null=True,default=None,blank=True)
    vl2=models.JSONField(null=True,default=None,blank=True)
    vl3=models.JSONField(null=True,default=None,blank=True)
    vl4=models.JSONField(null=True,default=None,blank=True)
    re1=models.JSONField(null=True,default=None,blank=True)
    re2=models.JSONField(null=True,default=None,blank=True)
    re3=models.JSONField(null=True,default=None,blank=True)
    re4=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.ndv,self.ntp,self.nta,self.created_at,self.updated_at   
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class atm_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    ndv=models.JSONField(null=True,default=None,blank=True)
    nta=models.JSONField(null=True,default=None,blank=True)
    tmp=models.JSONField(null=True,default=None,blank=True)
    whr=models.JSONField(null=True,default=None,blank=True)
    # custid=models.CharField(max_length=50,null=True,default=None,blank=True)
    ntp=models.JSONField(null=True,default=None,blank=True)
    nov=models.JSONField(null=True,default=None,blank=True)
    vl1=models.JSONField(null=True,default=None,blank=True)
    vl2=models.JSONField(null=True,default=None,blank=True)
    vl3=models.JSONField(null=True,default=None,blank=True)
    vl4=models.JSONField(null=True,default=None,blank=True)
    re1=models.JSONField(null=True,default=None,blank=True)
    re2=models.JSONField(null=True,default=None,blank=True)
    re3=models.JSONField(null=True,default=None,blank=True)
    re4=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.ndv,self.ntp,self.nta,self.created_at,self.updated_at   
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class atm_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    ndv=models.JSONField(null=True,default=None,blank=True)
    nta=models.JSONField(null=True,default=None,blank=True)
    tmp=models.JSONField(null=True,default=None,blank=True)
    whr=models.JSONField(null=True,default=None,blank=True)
    # custid=models.CharField(max_length=50,null=True,default=None,blank=True)
    ntp=models.JSONField(null=True,default=None,blank=True)
    nov=models.JSONField(null=True,default=None,blank=True)
    vl1=models.JSONField(null=True,default=None,blank=True)
    vl2=models.JSONField(null=True,default=None,blank=True)
    vl3=models.JSONField(null=True,default=None,blank=True)
    vl4=models.JSONField(null=True,default=None,blank=True)
    re1=models.JSONField(null=True,default=None,blank=True)
    re2=models.JSONField(null=True,default=None,blank=True)
    re3=models.JSONField(null=True,default=None,blank=True)
    re4=models.JSONField(null=True,default=None,blank=True)
    # avg=models.f(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.ndv,self.ntp,self.nta,self.created_at,self.updated_at   
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
# class tap1_repo_daily(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     p1=models.JSONField(null=True,default=None,blank=True)
#     p2=models.JSONField(null=True,default=None,blank=True)
#     p3=models.JSONField(null=True,default=None,blank=True)
#     p4=models.JSONField(null=True,default=None,blank=True)
#     # avg=models.f(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)

#     def __str__(self) -> str:
#         return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'
class tap1_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap1_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap1_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap1_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap2_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap2_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap2_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap2_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap3_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap3_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap3_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap3_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap4_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap4_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap4_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap4_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    p1=models.JSONField(null=True,default=None,blank=True)
    p2=models.JSONField(null=True,default=None,blank=True)
    p3=models.JSONField(null=True,default=None,blank=True)
    p4=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.device_id,self.service,self.p1,self.p2,self.p4,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
# class consen_repo_hourly(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     cnd=models.JSONField(null=True,default=None,blank=True)
#     spn=models.JSONField(null=True,default=None,blank=True)
#     asp=models.JSONField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)
#     def __str__(self) -> str:
#         return self.device_id,self.service,self.cnd,self.spn,self.asp,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'
# class consen_repo_daily(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     cnd=models.JSONField(null=True,default=None,blank=True)
#     spn=models.JSONField(null=True,default=None,blank=True)
#     asp=models.JSONField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)
#     def __str__(self) -> str:
#         return self.device_id,self.service,self.cnd,self.spn,self.asp,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'
# class consen_repo_monthly(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     cnd=models.JSONField(null=True,default=None,blank=True)
#     spn=models.JSONField(null=True,default=None,blank=True)
#     asp=models.JSONField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)
#     def __str__(self) -> str:
#         return self.device_id,self.service,self.cnd,self.spn,self.asp,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'
# class consen_repo_yearly(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     cnd=models.JSONField(null=True,default=None,blank=True)
#     spn=models.JSONField(null=True,default=None,blank=True)
#     asp=models.JSONField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)
#     def __str__(self) -> str:
#         return self.device_id,self.service,self.cnd,self.spn,self.asp,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'



class tds_consen_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    tds=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.device_id,self.service,self.cnd,self.spn,self.asp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class cnd_consen_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    cnd=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.device_id,self.service,self.cnd,self.spn,self.asp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tds_consen_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    tds=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.device_id,self.service,self.tds,self.spn,self.asp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'


class cnd_consen_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    cnd=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.device_id,self.service,self.cnd,self.spn,self.asp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tds_consen_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    tds=models.JSONField(null=True,default=None,blank=True)
    spn=models.JSONField(null=True,default=None,blank=True)
    asp=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.device_id,self.service,self.tds,self.spn,self.asp,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class device_info(models.Model):
    Device_id=models.CharField(max_length=100)
    Device_name=models.CharField(max_length=100)    
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    site_name=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return self.Device_id
    
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class key_info(models.Model):
    key_name=models.CharField(max_length=100)
    key_value=models.CharField(max_length=100)    
    


    def str(self):
        return self.key_name
    
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class graph_info(models.Model):
    service_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)    
    


    def str(self):
        return self.service_name
    
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class rwp_setting(models.Model):
    olc=models.CharField(max_length=100)
    drc=models.CharField(max_length=100)
    spn=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100) 
    device_id=models.CharField(max_length=100)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return self.olc,self.drc,self.spn,self.unit_type,self.company_id,self.componant_name   
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class hpp_setting(models.Model):
    olc=models.CharField(max_length=100)
    drc=models.CharField(max_length=100)
    spn=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)    
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return self.olc
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class cnd_setting(models.Model):
    spn=models.CharField(max_length=100)
    tsp=models.CharField(max_length=100)
    asp=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)  
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.spn 
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tds_setting(models.Model):
    spn=models.CharField(max_length=100)
    tsp=models.CharField(max_length=100)
    asp=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)  
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.spn 
    

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
# 
class panel_setting(models.Model):
    mod=models.CharField(max_length=100)
    unv=models.CharField(max_length=100)
    ovv=models.CharField(max_length=100)
    spn=models.CharField(max_length=100)    
    nmv=models.CharField(max_length=100)    
    stp=models.CharField(max_length=100)    
    srt=models.CharField(max_length=100)    
    bkt=models.CharField(max_length=100)    
    rst=models.CharField(max_length=100)    
    componant_name=models.CharField(max_length=100)    
    unit_type=models.CharField(max_length=100)    
    company_id=models.CharField(max_length=100)    
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.mod 

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class atm_setting(models.Model):
    ntp=models.CharField(max_length=100)
    nov=models.CharField(max_length=100)
    vl1=models.CharField(max_length=100)
    vl2=models.CharField(max_length=100)    
    vl3=models.CharField(max_length=100)    
    vl4=models.CharField(max_length=100)    
    re1=models.CharField(max_length=100)    
    re2=models.CharField(max_length=100)    
    re3=models.CharField(max_length=100)    
    re4=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)    
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.ntp 
    
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class cnd_consen_setting(models.Model):
    spn=models.CharField(max_length=100)
    asp=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.spn

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tds_consen_setting(models.Model):
    spn=models.CharField(max_length=100)
    asp=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.spn

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap1_setting(models.Model):
    p1=models.CharField(max_length=100)
    p2=models.CharField(max_length=100)
    p3=models.CharField(max_length=100)
    p4=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.p1
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap2_setting(models.Model):
    p1=models.CharField(max_length=100)
    p2=models.CharField(max_length=100)
    p3=models.CharField(max_length=100)
    p4=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.p1
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap3_setting(models.Model):
    p1=models.CharField(max_length=100)
    p2=models.CharField(max_length=100)
    p3=models.CharField(max_length=100)
    p4=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.p1
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class tap4_setting(models.Model):
    p1=models.CharField(max_length=100)
    p2=models.CharField(max_length=100)
    p3=models.CharField(max_length=100)
    p4=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.p1
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'


class Rwp_state(models.Model):
    sts=models.CharField(max_length=100) 
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.sts

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class hpp_state(models.Model):
    sts=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.sts
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'


class F_flowsen_setting(models.Model):
    ff1=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.ff
    
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class P_flowsen_setting(models.Model):
    ff2=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.ff
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class ampv1_setting(models.Model):
    srt=models.CharField(max_length=100)
    # srt2=models.CharField(max_length=100)
    bkt=models.CharField(max_length=100)
    rst=models.CharField(max_length=100)
    mot=models.CharField(max_length=100)
    stp=models.CharField(max_length=100)
    op1=models.CharField(max_length=100)
    op2=models.CharField(max_length=100)
    op3=models.CharField(max_length=100)
    ip1=models.CharField(max_length=100)
    ip2=models.CharField(max_length=100)
    ip3=models.CharField(max_length=100)
    psi=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.srt
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv2_setting(models.Model):
    srt=models.CharField(max_length=100)
    # srt2=models.CharField(max_length=100)
    bkt=models.CharField(max_length=100)
    rst=models.CharField(max_length=100)
    mot=models.CharField(max_length=100)
    stp=models.CharField(max_length=100)
    op1=models.CharField(max_length=100)
    op2=models.CharField(max_length=100)
    op3=models.CharField(max_length=100)
    ip1=models.CharField(max_length=100)
    ip2=models.CharField(max_length=100)
    ip3=models.CharField(max_length=100)
    psi=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.srt

    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv1_state(models.Model):
    pos=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.pos
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class ampv2_state(models.Model):
    pos=models.CharField(max_length=100)
    unit_type=models.CharField(max_length=100)
    company_id=models.CharField(max_length=100)
    componant_name=models.CharField(max_length=100)
    device_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def str(self):
        return self.pos
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class treat_F_flowsen(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    fr1=models.FloatField(null=True,default=None,blank=True)
    ff1=models.FloatField(null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'


# class F_flowsen_repo_hourly(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     fr1=models.FloatField(null=True,default=None,blank=True)
#     ff1=models.FloatField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)

#     def _str_(self) -> str:
#         return self.device_id,self.service,self.fr1,self.ff1,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'

# class P_flowsen_repo_hourly(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     fr2=models.FloatField(null=True,default=None,blank=True)
#     ff2=models.FloatField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)

#     def _str_(self) -> str:
#         return self.device_id,self.service,self.fr2,self.ff2,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'

# class F_flowsen_repo_daily(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     fr1=models.FloatField(null=True,default=None,blank=True)
#     ff1=models.FloatField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)

#     def _str_(self) -> str:
#         return self.device_id,self.service,self.fr1,self.ff1,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'

# class P_flowsen_repo_daily(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     fr2=models.FloatField(null=True,default=None,blank=True)
#     ff2=models.FloatField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)

#     def _str_(self) -> str:
#         return self.device_id,self.service,self.fr2,self.ff2,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'

# class F_flowsen_repo_monthly(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     fr1=models.FloatField(null=True,default=None,blank=True)
#     ff1=models.FloatField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)

#     def _str_(self) -> str:
#         return self.device_id,self.service,self.fr1,self.ff1,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'

# class P_flowsen_repo_monthly(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     fr2=models.FloatField(null=True,default=None,blank=True)
#     ff2=models.FloatField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)

#     def _str_(self) -> str:
#         return self.device_id,self.service,self.fr2,self.ff2,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'

# class F_flowsen_repo_yearly(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     fr1=models.FloatField(null=True,default=None,blank=True)
#     ff1=models.FloatField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)

#     def _str_(self) -> str:
#         return self.device_id,self.service,self.fr1,self.ff1,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'

# class P_flowsen_repo_yearly(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     device_id=models.CharField(max_length=100)
#     service=models.CharField(max_length=100,null=True,default=None,blank=True)
#     fr2=models.FloatField(null=True,default=None,blank=True)
#     ff2=models.FloatField(null=True,default=None,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
#     month =  models.CharField(max_length=50)
#     year =  models.CharField(max_length=50)
#     day =  models.CharField(max_length=50)
#     hour =  models.CharField(max_length=50)

#     def _str_(self) -> str:
#         return self.device_id,self.service,self.fr2,self.ff2,self.created_at,self.updated_at
#     class Meta:
#         app_label = 'devices'

class disp_flowsen1(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    fr=models.FloatField(null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class disp_flowsen2(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    fr=models.FloatField(null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class disp_flowsen3(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    fr=models.FloatField(null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
class disp_flowsen4(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    fr=models.FloatField(null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'



class flowsen1_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen1_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen1_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen1_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen2_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen2_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen2_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen2_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen3_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen3_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen3_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen3_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen4_repo_yearly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen4_repo_monthly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen4_repo_daily(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class flowsen4_repo_hourly(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id=models.CharField(max_length=100)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    fr=models.JSONField(null=True,default=None,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    month =  models.CharField(max_length=50)
    year =  models.CharField(max_length=50)
    day =  models.CharField(max_length=50)
    hour =  models.CharField(max_length=50)

    def _str_(self) -> str:
        return self.device_id,self.service,self.fr,self.created_at,self.updated_at
    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'

class Errors(models.Model):
    device_id=models.CharField(max_length=100)
    message_type=models.CharField(max_length=50)
    e_discriptions=models.CharField(max_length=250)
    o_message=models.CharField(max_length=150)
    service=models.CharField(max_length=100,null=True,default=None,blank=True)
    year=models.CharField(max_length=50)
    month=models.CharField(max_length=50)
    day=models.CharField(max_length=50)
    hour=models.CharField(max_length=50)
    minit=models.CharField(max_length=50)
    second=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # class Meta:
    #     app_label = 'devices'
    # class Meta:
    #     app_label = 'connection'
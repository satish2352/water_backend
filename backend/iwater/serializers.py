from .models import User, Site
from rest_framework import serializers


class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = '__all__'
        # ('id',
        #  'site_name',
        #  'address',
        #  'city',
        #  'state',
        #  'phone',
        #  'device_name',
        #  'serial_no',
        #  'status',
        #  'alerts',
        #  'created')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


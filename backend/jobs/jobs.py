from django.conf import settings
import json
import paho.mqtt.client as mqtt
from connection.views import MqttClient
from iwater.iw_logger import logger


def schedule_api():
    if mqttc is None:
        mqttc = MqttClient()
        logger.info("mqtt object Not found so created")
    elif mqttc.connected_flag == False:
        mqttc.reconnect()
        logger.info("mqtt reconnected from scheduler")
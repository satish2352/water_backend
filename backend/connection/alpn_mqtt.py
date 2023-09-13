from __future__ import print_function
# import sys
# import ssl
# import time
# import datetime
# import logging, traceback
# import paho.mqtt.client as mqtt
# import os
# import requests
from init_water_app import settings
# # import environ
# # env = environ.Env()
# # environ.Env.read_env()
# current_directory = os.getcwd()
# # pathtofiles = current_directory + "\\aws_broker_files\\"
# pathtofiles = current_directory + "\\Test\\"
# IoT_protocol_name = "x-amzn-mqtt-ca"

# aws_iot_endpoint = "a2al4qktysi6gi-ats.iot.ap-southeast-1.amazonaws.com"
aws_iot_endpoint = "a2al4qktysi6gi-ats.iot.ap-south-1.amazonaws.com"
# aws_iot_endpoint = settings.AWS_IOT_ENDPOINT

# url = "https://{}".format(aws_iot_endpoint)

# # ca =  pathtofiles +"RootCA1.pem"
# # cert = pathtofiles + "Device-certificate.pem.crt"
# # private = pathtofiles + "private.pem.key"
# ca =  "C:/Users/My Pc/Desktop/crownWebDevServer_28-06-2023/local webcrown 11-9-23/water_backend/backend/Test/RootCA1.pem"
# cert = "C:/Users/My Pc/Desktop/crownWebDevServer_28-06-2023/local webcrown 11-9-23/water_backend/backend/Test/Dc.pem.crt"
# private = "C:/Users/My Pc/Desktop/crownWebDevServer_28-06-2023/local webcrown 11-9-23/water_backend/backend/Test/private.pem.key"


# # ca = settings.CA

# # cert = settings.CERT
# # private = settings.PRIVATE

# # ca=requests.get(ca)
# # cert=requests.get(cert)
# # private=requests.get(private)


# # ca = ca.content
# # cert = cert.content
# # private = private.content
# # ca=ca.text
# # cert=cert.text
# # private=private.text
# # print("private.pem.key: ",private)

# logger = logging.getLogger()
# logger.setLevel(logging.WARNING)
# handler = logging.StreamHandler(sys.stdout)
# log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(log_format)
# logger.addHandler(handler)

# import tempfile
# # .. (previous imports and code)

# # Fetch the content of the certificate files from URLs
# ca_response = requests.get(ca)
# cert_response = requests.get(cert)
# private_key_response = requests.get(private)

# ca_content = ca_response.content
# cert_content = cert_response.content
# private_key_content = private_key_response.content

# # Create temporary files to store certificate content
# with tempfile.NamedTemporaryFile(delete=False) as ca_tempfile, \
#      tempfile.NamedTemporaryFile(delete=False) as cert_tempfile, \
#      tempfile.NamedTemporaryFile(delete=False) as private_tempfile:

#     ca_tempfile.write(ca_content)
#     cert_tempfile.write(cert_content)
#     private_tempfile.write(private_key_content)

#     # Obtain the file paths
#     ca_path = ca_tempfile.name
#     cert_path = cert_tempfile.name
#     private_key_path = private_tempfile.name

# # ... (rest of the code)



# # def ssl_alpn():
# #     try:
# #         logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
# #         ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

# #         # Load CA certificate from temporary file
# #         ssl_context.load_verify_locations(cafile=ca_path)

# #         # Load client certificate and private key
# #         ssl_context.load_cert_chain(certfile=cert_path, keyfile=private_key_path)

# #         return ssl_context
# #     except Exception as e:
# #         print("exception ssl_alpn()")
# #         raise e


# def ssl_alpn():
#     try:
#         logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
#         ssl_context = ssl.create_default_context()
#         ssl_context.set_alpn_protocols([IoT_protocol_name])
#         ssl_context.load_verify_locations(cafile=ca_path)
#         ssl_context.load_cert_chain(certfile=cert_path, keyfile=private_key_path)

#         return ssl_context
#     except Exception as e:
#         print("exception ssl_alpn()")
#         raise e

# ... (rest of the code)

# def ssl_alpn():
#     try:
#         #debug print opnessl version
#         logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
#         ssl_context = ssl.create_default_context()
#         ssl_context.set_alpn_protocols([IoT_protocol_name])
#         ssl_context.load_verify_locations(cafile=ca)
#         ssl_context.load_cert_chain(certfile=cert, keyfile=private)

#         return  ssl_context
#     except Exception as e:
#         print("exception ssl_alpn()")
#         raise e

# if __name__ == '__main__':
#     topic = "test/date"
#     try:
#         mqttc = mqtt.Client()
#         ssl_context= ssl_alpn()
#         mqttc.tls_set_context(context=ssl_context)
#         logger.info("start connect")
#         mqttc.connect(aws_iot_endpoint, port=443)
#         logger.info("connect success")
#         mqttc.loop_start()

#         while True:
#             now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
#             logger.info("try to publish:{}".format(now))
#             mqttc.publish(topic, now)
#             time.sleep(1)
        

#     except Exception as e:
#         logger.error("exception main()")
#         logger.error("e obj:{}".format(vars(e)))
#         logger.error("message:{}".format(e.message))
#         traceback.print_exc(file=sys.stdout)
     
# from __future__ import print_function
import sys
import ssl
import time
import datetime
import logging, traceback
import paho.mqtt.client as mqtt

IoT_protocol_name = "x-amzn-mqtt-ca"
# aws_iot_endpoint = "aiko32o7f20z-ats.iot.eu-north-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
# aws_iot_endpoint = "a2al4qktysi6gi-ats.iot.ap-southeast-1.amazonaws.com" # <random>.iot.<region>.amazonaws.com
url = "https://{}".format(aws_iot_endpoint)

# # ca = "C://Users/harsh/Downloads/AmazonRootCA1.pem" #testing
# ca =  "C:/Users/My Pc/Desktop/6-7water/aws_django/aws_broker_files/RootCA1.pem"
# ca =  "C:/Users/My Pc/Desktop/6-7water/aws_django/aws_broker_files/RootCA1.pem"
# # cert = "C:/Users/harsh/Downloads/30f1d28338acfe6f98921e02f445954428b147a069400dec8327a8d0c3356924-certificate.pem.crt" #testing
# cert = "C:/Users/My Pc/Desktop/6-7water/aws_django/aws_broker_files/Device-certificate.pem.crt"
# # private = "C:/Users/harsh/Downloads/30f1d28338acfe6f98921e02f445954428b147a069400dec8327a8d0c3356924-private.pem.key" #testing
# private = "C:/Users/My Pc/Desktop/6-7water/aws_django/aws_broker_files/private.pem.key"
ca =  "C:/Users/My Pc/Desktop/crownWebDevServer_28-06-2023/local webcrown 11-9-23/water_backend/backend/Test/RootCA1.pem"
cert = "C:/Users/My Pc/Desktop/crownWebDevServer_28-06-2023/local webcrown 11-9-23/water_backend/backend/Test/Dc.pem.crt"
private = "C:/Users/My Pc/Desktop/crownWebDevServer_28-06-2023/local webcrown 11-9-23/water_backend/backend/Test/private.pem.key"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)

def ssl_alpn():
    try:
        #debug print opnessl version
        logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([IoT_protocol_name])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

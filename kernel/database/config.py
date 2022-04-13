import base64
import json
import sys

# DEVELOPMENT CONFIGURATION
# database

mysql_write_url = "classfit-clone.cluster-cjwhdnfvi5np.us-east-2.rds.amazonaws.com"
mysql_read_url = "classfit-clone.cluster-ro-cjwhdnfvi5np.us-east-2.rds.amazonaws.com"
mysql_user = "admin"
mysql_password = "admin3030"
mysql_db_name = "fastplayapp_test"
mysql_payment_db_name = "payments"
mysql_bundle_db_name = "bundles"
# bundle microservice
bundle_url = "https://v2.classfit.com/bundles/"
backend_url = "https://react.classfit.com/api/index.php/c/"
# payment microservice
payment_url = "https://v2.classfit.com/payment/"
json = json
base64 = base64
sys = sys
# image_s3_bucket
s3_bucket_url = "https://classfit-assets.s3.amazonaws.com"
ImgServer = "https://classfit-assets.s3.amazonaws.com/backup"
# PRODUCTION CONFIGURATION
# # database
# mysql_url="classfit-clone-instance-1-restored-cluster.cluster-cjwhdnfvi5np.us-east-2.rds.amazonaws.com"
# mysql_user="admin"
# mysql_password="admin3030"
# mysql_db_name="fastplayapp_test"
#
# #bundle microservice
# bundle_url="https://v2.classfit.com/bundles/"
#
# #payment microservice
# payment_url="https://v2.classfit.com/payment/"

web_notification_url = 'https://fcm.googleapis.com/fcm/send'

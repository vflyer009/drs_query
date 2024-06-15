import json
import mysql.connector
import urllib3
from urllib.parse import urlencode

DRS_AD_URL = "https://drs.faa.gov/browse/excelExternalWindow"
http = urllib3.PoolManager()

# def get_drs_ads(base_url=DRS_BASE_URL, method=HTTP_METHOD):
#     response = http.request(
#         method=method,
#         url=DRS_BASE_URL,
#         headers={"x-api-key": DRS_API_KEY},
#         # body=encoded_params
#     )


# for x in myresult:
#   print(x[-2])

ex_ad_num = "FR-ADFRAWD-2024-04557-0000000000" 

full_drs_url = f"{DRS_AD_URL}/{ex_ad_num}.0001"

response = http.request(
    method="GET",
    url=full_drs_url,
)

print(response.data)

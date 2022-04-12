import requests

from Cafe24_Data import *

def retrieve_Order_Resource(Access_Token):
  print("============================================================================================")
  print("============================================================================================")
  print("====================          Cafe24 Retrieve a Order resource          ====================")
  print("============================================================================================")
  print("============================================================================================")

  requestsURL = "https://" + mall_id + ".cafe24api.com/api/v2/admin/orders?start_date=2022-03-01&end_date=2022-04-12"

  # Access Token 요청에 필요한 header
  h = {
    'Authorization': 'Bearer ' + Access_Token,
    'Content-Type': 'application/json',
    'X-Cafe24-Api-Version': cafe24_version
  }

  # rest API
  response = requests.request('GET', requestsURL, headers=h)

  return response
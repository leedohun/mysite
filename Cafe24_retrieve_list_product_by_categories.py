import requests

from Cafe24_Data import *

def retrieve_Product_by_Categories(Access_Token, category_no):
  print("============================================================================================")
  print("============================================================================================")
  print("====================    Cafe24 Retrieve a product category resource    ====================")
  print("============================================================================================")
  print("============================================================================================")

  requestsURL = "https://" + mall_id + ".cafe24api.com/api/v2/admin/categories/" + str(category_no) + "/products?display_group=1"

  # Access Token 요청에 필요한 header
  h = {
    'Authorization': 'Bearer ' + Access_Token,
    'Content-Type': 'application/json',
    'X-Cafe24-Api-Version': cafe24_version
  }

  # rest API
  response = requests.request('GET', requestsURL, headers=h)

  return response
import requests
import base64

from Cafe24_Data import *

def get_Access_Token(code):
  print("============================================================================================")
  print("============================================================================================")
  print("====================              Cafe24 Get Access Token              ====================")
  print("============================================================================================")
  print("============================================================================================")

  # token 요청 URL
  requestsURL = "https://" + mall_id + ".cafe24api.com/api/v2/oauth/token"

  # Access Token 요청에 필요한 header
  h = {
    'Authorization': 'Basic ' + str(base64.b64encode((client_id + ":" + client_secret).encode('utf-8'))).split("'")[1],
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  # Access Token 요청에 필요한  data
  d = { 
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': client_redirect_url
  }

  # rest API
  response = requests.request('POST', requestsURL, headers=h, data=d)

  return response


def get_Access_Token_with_Refresh_Token(refresh_Token):
  print("============================================================================================")
  print("============================================================================================")
  print("====================     Cafe24 Get Access Token with Refresh Token     ====================")
  print("============================================================================================")
  print("============================================================================================")

  # token 요청 URL
  requestsURL = "https://" + mall_id + ".cafe24api.com/api/v2/oauth/token"

  # Access Token 요청에 필요한 header
  h = {
    'Authorization': 'Basic ' + str(base64.b64encode((client_id + ":" + client_secret).encode('utf-8'))).split("'")[1],
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  # Access Token 요청에 필요한  data
  d = { 
    'grant_type': 'refresh_token',
    'refresh_token': refresh_Token
  }

  # rest API
  response = requests.request('POST', requestsURL, headers=h, data=d)

  return response
import os
import json

import datetime
from pkgutil import iter_modules

from django.shortcuts import redirect, render
from .models import *

# API 필요한 data
from Cafe24_Data import *

from Cafe24_get_Code import *           # Cafe24 API 필요한 인증 코드
from Cafe24_get_Access_Token import *   # Cafe24 API 필요한 Access Token 발급


from Cafe24_retrieve_Product_resource import *          # Cafe24 쇼핑몰 product 정보 검색
from Cafe24_retrieve_list_product_categories import *   # Cafe24 쇼핑몰 product categories정보 검색

# Create your views here.

# product 데이터 담는 list
shop_no = []
product_no = []
product_code = []
product_name = []
price = []
display = []
selling = []
detail_image = []
list_image = []
tiny_image = []
small_image = []
sold_out = []

# category 데이터 담는 list
category_no = []
category_name = []
upper_category_name = []
upper_category_no = []
root_category_no = []


# product json 데이터 가공해 list로 저장
def Select_Product(product_json_data):
  shop_no.clear(), product_no.clear(), product_code.clear(), product_name.clear(), price.clear(), display.clear(), selling.clear(),
  detail_image.clear(), list_image.clear(), tiny_image.clear(), small_image.clear(), sold_out.clear()
  for product in product_json_data["products"]:
    shop_no.append(int(product["shop_no"]))
    product_no.append(int(product["product_no"]))
    product_code.append(product["product_code"])
    product_name.append(product["product_name"])
    price.append(product["price"])
    
    if product["display"] == "T":
      display.append(True)
    elif product["display"] == "F":
      display.append(False)
    
    if product["selling"] == "T":
      selling.append(True)
    elif product["selling"] == "F":
      selling.append(False)
    
    detail_image.append(product["detail_image"])
    list_image.append(product["list_image"])
    tiny_image.append(product["tiny_image"])
    small_image.append(product["small_image"])
    
    if product["sold_out"] == "T":
      sold_out.append(True)
    elif product["sold_out"] == "F":
      sold_out.append(False)


# category json 데이터 가공해 list로 저장
def Select_Categories(Categories_json_data):
  category_no.clear(), category_name.clear(), upper_category_name.clear(), upper_category_no.clear(), root_category_no.clear()
  for category in Categories_json_data["categories"]:
    categories_size = int(category["category_depth"])
  
    for cnt in range(1, categories_size + 1):
      category_no.append(int(category["category_no"]))
      category_name.append(category["category_name"])
      
      if cnt == 1:
        upper_category_name.append(category["full_category_name"]["1"])
        upper_category_no.append(int(category["full_category_no"]["1"]))
      elif cnt == 2:
        upper_category_name.append(category["full_category_name"]["2"])
        upper_category_no.append(int(category["full_category_no"]["2"]))
      elif cnt == 3:
        upper_category_name.append(category["full_category_name"]["3"])
        upper_category_no.append(int(category["full_category_no"]["3"]))
      elif cnt == 4:
        upper_category_name.append(category["full_category_name"]["4"])
        upper_category_no.append(int(category["full_category_no"]["4"]))
    
      root_category_no.append(int(category["root_category_no"]))

  
# Access_Token_File 생성
def make_Access_Token_File():
  code = get_Code()
  new_Access_Token_Data = get_Access_Token(code).json()

  with open("./" + mall_id + "_Access_Token.json", 'w') as outfile:
    json.dump(new_Access_Token_Data, outfile)

# Access_Token_File을 refresh_Token으로 재 할당
def rebuild_Access_Token_file(refresh_Token):
  new_Access_Token_Data = get_Access_Token_with_Refresh_Token(refresh_Token).json()

  with open("./" + mall_id + "_Access_Token.json", 'w') as outfile:
    json.dump(new_Access_Token_Data, outfile)

def Cafe24API():
  # 현재 Access_Token_File이 있는 경우
  if os.path.isfile("./" + mall_id + "_Access_Token.json"):
    with open("./" + mall_id + "_Access_Token.json", 'r') as f:
      access_Token_Data = json.load(f)
    
    refresh_token_expires_at = str(access_Token_Data["refresh_token_expires_at"])

    # refresh_Token이 만료 된 경우
    if datetime.datetime.now() - datetime.timedelta(days=10) > datetime.datetime.strptime(refresh_token_expires_at.split('T')[0], "%Y-%m-%d"):
      make_Access_Token_File()
    # refresh_Token이 만료가 안된 경우
    else:
      rebuild_Access_Token_file(access_Token_Data['refresh_token'])
  # 현재 Access_Token_File이 없는 경우
  else:
    make_Access_Token_File()

def home(request):
  Cafe24API()
  return render(request,'upsell/home.html')

def products(request):
  # 사용가능한 Access Key 발급
  with open("./" + mall_id + "_Access_Token.json", 'r') as f:
    access_Token_Data = json.load(f)
    
  # 쇼핑몰의 현재 제품 데이터 가져오기
  product_Resource = retrieve_Product_Resource(access_Token_Data['access_token']).json()
  Select_Product(product_Resource)

  print("쇼핑몰 번호, 제품 번호, 제품 코드, 제품 이름, 제품 가격, 제품 보이게?, 판매 제품?, 자세한 이미지, 리스트 이미지, 티니 이미지, 작은 이미지, 재고 없음?")
  for i in range(0, len(product_no)):
    print(shop_no[i], " ", product_no[i], " ", product_code[i], " ", product_name[i], " ", price[i], " ", display[i], " ", selling[i], " ", detail_image[i], " ", list_image[i], " ", tiny_image[i], " ", small_image[i], " ", sold_out[i], " ")
  
  for i in range(0, len(product_no)):
    order, created = product.objects.update_or_create(
      mall_cafe24 = mall_cafe24.objects.all()[0],
      mall = mall.objects.all()[0],

      product_no = product_no[i],
      product_code = product_code[i],

      defaults = { 
        "product_name": product_name[i],
        "price": price[i],
        "display": display[i],
        "selling": selling[i],
        "detail_image": detail_image[i],
        "list_image": list_image[i],
        "tiny_image": tiny_image[i],
        "small_image": small_image[i],
        "sold_out": sold_out[i]
      }
    )

  return render(request,'upsell/products.html')


def orders(request):
  return render(request,'upsell/orders.html')

def order_item(request):
  return render(request, 'upsell/order_item.html')



def categories(request):
  # 사용가능한 Access Key 발급
  with open("./" + mall_id + "_Access_Token.json", 'r') as f:
    access_Token_Data = json.load(f)
    
  product_Categories = retrieve_Product_Categories(access_Token_Data['access_token']).json()
  Select_Categories(product_Categories)

  print("카테고리 번호, 카테고리 이름, 상위 카테고리 이름, 상위 카테고리 번호, 루트 카테고리 번호")
  for i in range(0, len(category_no)):
    print(category_no[i], " ", category_name[i], " ", upper_category_name[i], " " , upper_category_no[i], " ", root_category_no[i])

  for i in range(0, len(category_no)):
    order, created = category.objects.update_or_create(
      mall_cafe24 = mall_cafe24.objects.all()[0],
      mall = mall.objects.all()[0],

      category_no = category_no[i],
      upper_category_no = upper_category_no[i],

      defaults = { 
        "category_name": category_name[i],
        "upper_category_name": upper_category_name[i],
        "root_category_no": root_category_no[i],
      }
    )

  return render(request,'upsell/categories.html')
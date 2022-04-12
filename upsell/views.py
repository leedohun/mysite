import os
import json

import datetime
from pkgutil import iter_modules
from sre_constants import CATEGORY_NOT_SPACE

from django.shortcuts import redirect, render
from .models import *

# API 필요한 data
from Cafe24_Data import *

from Cafe24_get_Code import *           # Cafe24 API 필요한 인증 코드
from Cafe24_get_Access_Token import *   # Cafe24 API 필요한 Access Token 발급

from Cafe24_retrieve_list_product_by_categories import *    # Cafe24 쇼핑몰 product by category 정보 검색
from Cafe24_retrieve_Product_resource import *              # Cafe24 쇼핑몰 product 정보 검색
from Cafe24_retrieve_list_product_category_count import *   # Cafe24 쇼핑몰 product categories count 검색
from Cafe24_retrieve_list_product_categories import *       # Cafe24 쇼핑몰 product categories 정보 검색
from Cafe24_retrieve_Order_resource import *                # Cafe24 쇼핑몰 product order 정보 검색

# Create your views here.


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

  print("제품 번호, 제품 코드, 제품 이름, 제품 가격, 제품 보이게?, 판매 제품?, 자세한 이미지, 리스트 이미지, 티니 이미지, 작은 이미지, 재고 없음?")
  for products in product_Resource["products"]:
    print(products["product_no"], " ", products["product_code"], " ", products["product_name"], " ", products["price"], " ", products["display"], " ", products["selling"], " ", products["detail_image"], " ", products["list_image"], " ", products["tiny_image"], " ", products["small_image"], " ", products["sold_out"], " ")
  
  for products in product_Resource["products"]:
    order, created = product.objects.get_or_create(
      mall_cafe24 = mall_cafe24.objects.all()[0],
      mall = mall.objects.all()[0],

      product_no = int(products["product_no"]),
      product_code = products["product_code"],
    )

    order.product_name = products["product_name"]
    order.price = products["price"]

    if products["display"] == "T":
      order.display = True
    elif products["display"] == "F":
      order.display = False
    if products["selling"] == "T":
      order.selling = True
    elif products["selling"] == "F":
      order.selling = False

    if products["detail_image"]:
      order.detail_image = products["detail_image"]
    if products["list_image"]:
      order.list_image = products["list_image"]
    if products["tiny_image"]:
      order.tiny_image = products["tiny_image"]
    if products["small_image"]:
      order.small_image = products["small_image"]

    if products["sold_out"] == "T":
      order.sold_out = True
    elif products["sold_out"] == "F":
      order.sold_out = False

    order.save()
    
  return render(request,'upsell/products.html')


def orders(request):
  # 사용가능한 Access Key 발급
  with open("./" + mall_id + "_Access_Token.json", 'r') as f:
    access_Token_Data = json.load(f)

  product_order_data = retrieve_Order_Resource(access_Token_Data['access_token']).json()

  print(product_order_data)

  return render(request,'upsell/orders.html')

def order_item(request):
  return render(request, 'upsell/order_item.html')


def categories(request):
  # 사용가능한 Access Key 발급
  with open("./" + mall_id + "_Access_Token.json", 'r') as f:
    access_Token_Data = json.load(f)

  product_Categories_Count = retrieve_Product_Categories_Count(access_Token_Data['access_token']).json()
  product_Categories_Count = int(product_Categories_Count["count"])
  i = 0

  while i + 10 < product_Categories_Count:
    product_Categories = retrieve_Product_Categories(access_Token_Data['access_token'], i).json()

    print("카테고리 번호, 카테고리 이름, 상위 카테고리 이름, 상위 카테고리 번호, 루트 카테고리 번호")
    for categories in product_Categories["categories"]:
      print(categories["category_no"], " ", categories["category_name"], " ", categories["full_category_name"], " " , categories["full_category_no"], " ", categories["root_category_no"])

    for categories in product_Categories["categories"]:
      categories_size = int(categories["category_depth"])

      for cnt in range(1, categories_size + 1):
        if cnt == 1:
          upper_category_no = categories["full_category_no"]["1"]
          upper_category_name = categories["full_category_name"]["1"]
        elif cnt == 2:
          upper_category_no = categories["full_category_no"]["2"]
          upper_category_name = categories["full_category_name"]["2"]
        elif cnt == 3:
          upper_category_no = categories["full_category_no"]["3"]
          upper_category_name = categories["full_category_name"]["3"]
        elif cnt == 4:
          upper_category_no = categories["full_category_no"]["4"]
          upper_category_name = categories["full_category_name"]["4"]

        order, created = category.objects.get_or_create(
          mall_cafe24 = mall_cafe24.objects.all()[0],
          mall = mall.objects.all()[0],

          category_no = categories["category_no"],
          category_name = categories["category_name"],

          category_depth = categories["category_depth"],

          upper_category_no = upper_category_no,
          upper_category_name = upper_category_name,
        )

    i = i + 10

  return render(request,'upsell/categories.html')


# 제품과 카테고리 저장
def products_by_categories(request):
  # 사용가능한 Access Key 발급
  with open("./" + mall_id + "_Access_Token.json", 'r') as f:
    access_Token_Data = json.load(f)

  chk_category_no = set()
  categories_data = category.objects.all()

  for category_data in categories_data:

    time.sleep(1)

    if category_data.category_no not in chk_category_no:
      chk_category_no.add(category_data.category_no)
      product_by_categories = retrieve_Product_by_Categories(access_Token_Data['access_token'], category_data.category_no).json()

      print(product_by_categories)

      for product_by_cate in product_by_categories["products"]:
        get_product = product.objects.filter(product_no=product_by_cate["product_no"])

        order, created = product_by_category.objects.get_or_create(
          mall_cafe24 = mall_cafe24.objects.all()[0],
          mall = mall.objects.all()[0],
          
          product = get_product[0],

          category_no = category_data.category_no,
          category_name = category_data.category_name
        )
  
  return render(request,'upsell/products_by_categories.html')
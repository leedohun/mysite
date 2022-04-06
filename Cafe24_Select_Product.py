import json

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

def Select_Product():
  with open('./dlehgns011_Product.json', 'r') as f:
    product_json_data = json.load(f)

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

  print("쇼핑몰 번호, 제품 번호, 제품 코드, 제품 이름, 제품 가격, 제품 보이게?, 판매 제품?, 자세한 이미지, 리스트 이미지, 티니 이미지, 작은 이미지, 재고 없음?")
  for i in range(0, len(product_no)):
    print(shop_no[i], " ", product_no[i], " ", product_code[i], " ", product_name[i], " ", price[i], " ", display[i], " ", selling[i], " ", detail_image[i], " ", list_image[i], " ", tiny_image[i], " ", small_image[i], " ", sold_out[i], " ")


Select_Product()
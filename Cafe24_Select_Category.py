import json

category_no = []
category_name = []
upper_category_name = []
upper_category_no = []
root_category_no = []

def Select_Categories():
  with open('./dlehgns011_Categories.json', 'r') as f:
    Categories_json_data = json.load(f)

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

  print("카테고리 번호, 카테고리 이름, 상위 카테고리 이름, 상위 카테고리 번호, 루트 카테고리 번호")
  for i in range(0, len(category_no)):
    print(category_no[i], " ", category_name[i], " ", upper_category_name[i], " " , upper_category_no[i], " ", root_category_no[i])

Select_Categories()
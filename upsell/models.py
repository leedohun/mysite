from tkinter import CASCADE
from django.db import models
from django.utils import timezone
from numpy import maximum

# Create your models here.

# Cafe24상에서 사용하는 access_token 관리를 위한 테이블
class mall_cafe24(models.Model):
  mallid = models.CharField(null=False, primary_key=True, max_length=500) # 사용자 쇼핑몰 아이디
  access_token = models.CharField(null=False, max_length=500)             # API 호출 시 필요한 액세스 토큰
  expires_at = models.DateTimeField(null=True, )                          # 액세스 토큰 만료 일시
  refresh_token = models.CharField(null=True, max_length=500)             # 액세스 토큰을 재발급 할 수 있는 토큰
  refresh_token_expires_at = models.DateTimeField(null=True, )            # 액세스 토큰을 재발급 할 수 있는 토큰 만료 일시


# 기본적인 쇼핑몰 정보를 위한 테이블
class mall(models.Model):
  mall_cafe24 = models.ForeignKey(mall_cafe24, on_delete=models.CASCADE)

  shop_no = models.IntegerField(default=1)


# 쇼핑몰의 상품 정보 테이블
class product(models.Model):
  mall_cafe24 = models.ForeignKey(mall_cafe24, on_delete=models.CASCADE)
  mall = models.ForeignKey(mall, on_delete=models.CASCADE)

  product_no = models.IntegerField(null=True,)
  product_code = models.CharField(null=True, max_length=500)
  product_name = models.CharField(null=True, max_length=500)
  price = models.CharField(null=True, max_length=500)
  display = models.BooleanField(null=True, default=True)
  selling = models.BooleanField(null=True, default=True)
  category_no = models.IntegerField(null=True,)
  category_name = models.CharField(null=True, max_length=500)
  detail_image = models.CharField(blank=True, max_length=500)
  list_image = models.CharField(blank=True, max_length=500)
  tiny_image = models.CharField(blank=True, max_length=500)
  small_image = models.CharField(blank=True, max_length=500)
  sold_out = models.BooleanField(null=True)


# 쇼핑몰 카테고리 정보 테이블
class category(models.Model):
  mall_cafe24 = models.ForeignKey(mall_cafe24, on_delete=models.CASCADE)
  mall = models.ForeignKey(mall, on_delete=models.CASCADE)

  category_no = models.IntegerField(blank=True,)
  category_name = models.CharField(blank=True, max_length=500)
  category_depth = models.IntegerField(blank=True,)
  upper_category_no = models.IntegerField(blank=True, )
  upper_category_name = models.CharField(blank=True, max_length=500)

# 쇼핑몰 주문 정보 테이블

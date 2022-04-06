import time

from selenium import webdriver
from Cafe24_Data import *

def get_Code():
  print("============================================================================================")
  print("============================================================================================")
  print("====================                  Cafe24 Get Code                  ====================")
  print("============================================================================================")
  print("============================================================================================")

  requestsURL = "https://" + mall_id + ".cafe24api.com/api/v2/oauth/authorize?response_type=" + response_type + "&client_id=" + client_id + "&state=" + state + "&redirect_uri=" + client_redirect_url + "&scope=" + scope
  # 옵션 생성
  options = webdriver.ChromeOptions()

  # 창 숨기는 옵션 추가
  options.add_argument("headless")

  # driver 실행
  driver = webdriver.Chrome(options=options)
  driver.get(requestsURL)

  # 아이디/비밀번호를 입력해준다.
  driver.find_element_by_name('mall_id').send_keys('dlehgns011')
  driver.find_element_by_name('userpasswd').send_keys('Ldh980912k@')

  # 로그인 버튼을 누르기
  driver.find_element_by_xpath('/html/body/div[2]/div/section/div/form/div/div[3]/button').click()

  # 5초 정도 대기
  time.sleep(5)

  currentURL = str(driver.current_url).replace('=', '&')

  code=currentURL.split('&')[1]
  print(code)
  # driver 종료
  driver.quit()

  return code
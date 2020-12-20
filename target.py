import requests
from useragents import *

from random import randint
from random import seed

def add_to_cart(target, quantity, useragent):
  tcin = ''

  for loc, x in enumerate(target):
    if x == 'A':
      for x in range(2, 10):
        tcin += target[loc + x]
      tcin += '"'
    elif x == 'p' and target[loc+1] == 'r' and target[loc+2] == 'e':
      tcin = ''
      for x in range(10, 18):
        tcin += target[loc + x]
      tcin += '"'

  url = "https://carts.target.com/web_checkouts/v1/cart_items?field_groups=CART%2CCART_ITEMS%2CSUMMARY&key=feaf228eb2777fd3eee0fd5192ae7107d6224b39"

  payload="{\"cart_type\":\"REGULAR\",\"channel_id\":\"10\",\"shopping_context\":\"DIGITAL\",\"cart_item\":{\"tcin\":\"" + tcin + ",\"quantity\":" + str(quantity) + ",\"item_channel_id\":\"10\"},\"fulfillment\":{\"fulfillment_test_mode\":\"grocery_opu_team_member_test\"}}"

  headers = {
    'Host': 'carts.target.com',
    'Cookie': 'visitorId=017639E01D600201A4DB3CAE8C694FAB; sapphire=1; UserLocation=22102|38.920|-77.210|VA|US; fiatsCookie=DSI_2790|DSN_Merrifield|DSZ_22031; criteo={}; TealeafAkaSid=_5ZWYpyRF9YmUDpM6CkB9RCQ-YuCg9UH; tlThirdPartyIds=%7B%22pt%22%3A%22v2%3A586a19543c304cc6a65e4bce031c406dd0781a1e67f2e1e98578501c1b246360%7Ce282e0b9502221b842945a81509251acf359c18ba47030063f897be9b042a7a2%22%2C%22adHubTS%22%3A%22Fri%20Dec%2018%202020%2021%3A43%3A47%20GMT-0500%20(Eastern%20Standard%20Time)%22%7D; adaptiveSessionId=A9981059459; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIxN2Q1NGU1Ny1lM2VmLTQzMDItOWMzYi1hMjc2YTlkYzQzMGQiLCJpc3MiOiJNSTYiLCJleHAiOjE2MDg1MDc1NjgsImlhdCI6MTYwODQyMTE2OCwianRpIjoiVEdULmRiYjg1OTE3MjMzMzQ3ZWNhZDE4NzdmOThlMDYyYmY4LWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6Ijk5ZTk0MGIwNjM1MjY1OWY4ZmU2MDVlMDY5MGZhNmQ1ZmRmMDhjOWRmMjVjMzY5YjU5MjM5MjkzZWM1Yjk2MmMiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.v6Y8uZRpHqSYRVcuGy3G5Pz0D2tU-ZyvM-PWePGFmUpXupa8p8ina_ZbooL7SE7jw1QkTvKhCwU-IblYVK6sQ5IlovR2i3jLWg97TAeaj5LqPE_-rEJ9tHe4NQD5osk1bN9mfM6WNLqjf0u30lOUpcE4QYxJBsdvFFjArvAx3ZzViu7XGj6sgbQ0jRNcXJ1fKAvaCxwnCcx1WZWk2vAZnEJ5UoauwS0XftdkUHetl0ERvRlC7iRlgyLNOIkWSXtvBQSyZ_l9m155N_JbwpXRrHix0ZOorsmdxGMabaEcK0FAHBHpXVoUtqoZWoGG0ITO6xMEQtDzfTsjeVmOK5JYmQ; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiIxN2Q1NGU1Ny1lM2VmLTQzMDItOWMzYi1hMjc2YTlkYzQzMGQiLCJpc3MiOiJNSTYiLCJleHAiOjE2MDg1MDc1NjgsImlhdCI6MTYwODQyMTE2OCwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=6Gz7eLY7ZjxsQmTMX7BouozTZV3mgg9Rinrt4fW7UK-8PoN5H14pqBvJhCZ0GDeNBnPTXC0ya8gxgB54kkUbzg; guestType=G|1608421168000; ffsession={%22sessionHash%22:%2211fc4a95e117bf1608421168120%22%2C%22sessionHit%22:70%2C%22prevPageType%22:%22product%20details%22%2C%22prevPageName%22:%22electronics:%20product%20detail%22%2C%22prevPageUrl%22:%22' + target + '}; targetMobileCookie=cartQty:1~guestLogonId:null~guestDisplayName:null~guestHasVerifiedPhone:false',
    'accept': 'application/json',
    'dnt': '1',
    'x-application-name': 'web',
    'user-agent': useragent,
    'content-type': 'application/json',
    'origin': 'https://www.target.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': target,
    'accept-language': 'en-US,en;q=0.9,ko;q=0.8'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)


target = input("Please input your URL: ")
quantity = input("Please input your quantity: ")
useragent = useragents[randint(0, len(useragents))]

add_to_cart(target, quantity, useragent)
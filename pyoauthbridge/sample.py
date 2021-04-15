from connect import Connect
import webbrowser
from threading import Thread 
import time
import json

def get_request(self, url, params):
  headers = self.headers
  headers['Authorization'] = f'Bearer {self.access_token}'
  res = requests.get(f'{self.base_url}{url}' , params=params, headers=headers)
  return res.json()

def post_request(self, url, data):
  headers = self.headers
  headers['Authorization'] = f'Bearer {self.access_token}'
  res = requests.post(f'{self.base_url}{url}', headers=headers, data=json.dumps(data))
  print(res.json())
  return res.json()

if __name__ == '__main__':
  client_id = ""
  client_secret = ""
  redirect_url = "http://127.0.0.1:65010"
  
  websocket_url = ""
  base_url = ""
  conn = Connect(client_id, client_secret, redirect_url, base_url)
  webbrowser.open("http://127.0.0.1:65010/getcode")
  access_token = conn.get_access_token()

  print(access_token)

  # marketdata_payload = {'exchangeCode': 1, 'instrumentToken': 3045}
  # snapquotedata_payload = {'exchangeCode': 1, 'instrumentToken': 3045}
  orderupdate_payload = {'client_id': 'NA003'}

  ws_status = conn.run_socket()

  print("websocket connected ...")
  print(ws_status)
  # conn.subscribe_detailed_marketdata(marketdata_payload,)
  # conn.subscribe_snapquote_data(snapquotedata_payload,)
  conn.subscribe_order_update(orderupdate_payload)

  # print("channels subscribed ....")

  order_payload = {
    "exchange": "NSE",
    "instrument_token": 3045,
    "client_id": "NA003",
    "order_type": "LIMIT",
    "amo": "false",
    "price": 320,
    "quantity": 1,
    "disclosed_quantity": 0,
    "validity": "DAY",
    "product": "MIS",
    "order_side": "BUY",
    "device": "api",
    "user_order_id": 10002,
    "trigger_price": 0,
    "execution_type": "REGULAR"
  }

  order_deletion_payload = {
    "client_id": "NA003",
    "oms_order_id": "20210413-2531",
    "execution_type": "AMO"
  }

  res = conn.place_order(order_payload)
  # res = conn.cancel_order(order_deletion_payload)

  while True:
    order_update = conn.read_order_update_data()
    if(order_update):
      # print(order_update)
      new_order_status = 
      print(order_update["login_id"], order_update["order_status"])

  # i = 0
  # while True:
  #   time.sleep(1)
  #   detailed_market_data = conn.read_detailed_marketdata()
  #   print(detailed_market_data)
  #   # time.sleep(1)
  #   # snapquote_data = conn.read_snapquote_data()
  #   # print(detailed_market_data)
  #   i = i + 1
  #   print("==================================")
  #   # if i > 5:
  #   #   print("unsubscribe marketdata")
  #   #   conn.unsubscribe_detailed_marketdata(marketdata_payload)
  #   #   print("unsubscribe snapquote")
  #   #   conn.unsubscribe_detailed_marketdata(snapquotedata_payload)
    
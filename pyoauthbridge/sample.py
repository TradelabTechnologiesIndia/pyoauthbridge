from connect import Connect
import webbrowser
from threading import Thread 
import time

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

  marketdata_payload = {'exchangeCode': 1, 'instrumentToken': 3045}
  snapquotedata_payload = {'exchangeCode': 4, 'instrumentToken': 226027}

  ws_status = conn.run_socket()

  print("websocket connected ...")
  print(ws_status)
  conn.subscribe_detailed_marketdata(marketdata_payload,)
  conn.subscribe_snapquote_data(snapquotedata_payload,)

  print("channels subscribed ....")

  while True:
    time.sleep(1)
    detailed_market_data = conn.read_detailed_marketdata()
    print(detailed_market_data)
    time.sleep(1)
    snapquote_data = conn.read_snapquote_data()
    print(detailed_market_data)
    
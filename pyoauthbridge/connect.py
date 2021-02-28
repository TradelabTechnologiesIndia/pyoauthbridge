import requests
import json
from server import Server
from wsclient import socket_connect, read_compact_marketdata, read_detailed_marketdata, read_snapqotedata
import sys

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
class Connect:
    def __init__(self, client_id, client_secret, redirect_url, base_url):
        self.headers = {'Content-type': 'application/json'}
        self.access_token = ""
        self.login_id = ""
        self.base_url=base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url
        url = ""
        if "https" in base_url:
            url = base_url.replace("https", "wss")
        else:
            url = base_url.replace("http", "ws")
        self.websocket_url = url

    def get_access_token(self):
        base_url = self.base_url
        client_id = self.client_id
        client_secret = self.client_secret
        redirect_url = self.redirect_url
        server = Server(client_id, client_secret, redirect_url, base_url)
        app = server.create_app()
        app.env = 'development'
        print('Open this url in browser:', 'http://127.0.0.1:65010/getcode', end='\n\n')
        app.run(host='127.0.0.1', debug=False, port=65010)
        access_token = server.fetch_access_token()
        self.access_token = access_token
        return server.fetch_access_token()

    def print_access_token(self):
        return self.access_token

    def set_access_token(self, access_token):
        self.access_token = access_token

    def get_request(self, url, params):
        headers = self.headers
        headers['Authorization'] = f'Bearer {self.access_token}'
        res = requests.get(f'{self.base_url}{url}' , params=params, headers=headers)
        return res.json()

    def post_request(self, url, data):
        headers = self.headers
        headers['Authorization'] = f'Bearer {self.access_token}'
        res = requests.post(f'{self.base_url}{url}', headers=headers, data=json.dumps(data))
        print(res)
        return res.json()

    def put_request(self, url, data):
        headers = self.headers
        headers['Authorization'] = f'Bearer {self.access_token}'
        res = requests.put(f'{self.base_url}{url}', headers=headers, data=json.dumps(data))
        print(res)
        return res.json()

    def delete_request(self, url, params):
        headers = self.headers
        headers['Authorization'] = f'Bearer {self.access_token}'
        res = requests.delete(f'{self.base_url}{url}' , params=params, headers=headers)
        return res.json()

    def fetch_profile(self, payload):
        params = {'client_id': payload['client_id']}
        res = self.get_request("/api/v1/user/profile", params)
        return res

    def place_order(self, payload):
        data = {
            "exchange": payload['exchange'],
            "instrument_token": payload['instrument_token'],
            "client_id": payload['client_id'],
            "order_type": payload['order_type'],
            "amo": payload['amo'],
            "price": payload['price'],
            "quantity": payload['quantity'],
            "disclosed_quantity": payload['disclosed_quantity'],
            "validity": payload['validity'],
            "product": payload['product'],
            "order_side": payload['order_side'],
            "device": "api",
            "user_order_id": payload['user_order_id'],
            "trigger_price": payload['trigger_price'],
            "execution_type": payload['execution_type']
        }
        res = self.post_request(f'/api/v1/orders', data)
        return res

    def modify_order(self, payload):
        data = {
            "exchange": payload['exchange'],
            "instrument_token": payload['instrument_token'],
            "client_id": payload['client_id'],
            "order_type": payload['order_type'],
            "price": payload['price'],
            "quantity": payload['quantity'],
            "disclosed_quantity": payload['disclosed_quantity'],
            "validity": payload['validity'],
            "product": payload['product'],
            "oms_order_id": payload['oms_order_id'],
            "trigger_price": payload['trigger_price'],
            "execution_type": payload['execution_type']
        }
        res = self.put_request("/api/v1/orders", data)
        return res

    def cancel_order(self, payload):
        params = {
            'client_id': payload['client_id'],
            'execution_type': payload['execution_type']
        }
        res = self.delete_request(f'/api/v1/orders/{payload.oms_order_id}', params)
        return res

    def fetch_scripinfo(self, payload):
        params = {
            'info': 'scrip',
            'token': payload['token']
        }
        res = self.get_request(f'/api/v1/contract/NSE', params)
        return res

    def search_scrip(self, payload):
        params = {
            'key': payload['key']
        }
        res = self.get_request(f'/api/v1/search', params)
        return res

    def fetch_pending_orders(self, payload):
        params = {
            'type': 'pending',
            'client_id': payload['client_id']
        }
        res = self.get_request(f'/api/v1/orders', params)
        return res

    def fetch_completed_orders(self, payload):
        params = {
            'type': 'completed',
            'client_id': payload['client_id']
        }
        res = self.get_request(f'/api/v1/orders', params)
        return res

    def fetch_trades(self, payload):
        params = {
            'client_id': payload['client_id']
        }
        res = self.get_request(f'/api/v1/trades', params)
        return res

    def fetch_order_history(self, payload):
        params = {
            'client_id': payload['client_id']
        }
        res = self.get_request(f'/api/v1/order/{payload.oms_order_id}/history', params)
        return res

    def fetch_live_positions(self, payload):
        params = {
            'client_id': payload['client_id'],
            'type': 'live'
        }
        res = self.get_request(f'/api/v1/positions', params)
        return res

    def fetch_netwise_positions(self, payload):
        params = {
            'client_id': payload['client_id'],
            'type': 'historical'
        }
        res = self.get_request(f'/api/v1/positions', params)
        return res

    def fetch_holdings(self, payload):
        params = {
            'client_id': payload['client_id']
        }
        res = self.get_request(f'/api/v1/holdings', params)
        return res

    def fetch_funds_v2(self, payload):
        params = {
            'client_id': payload['client_id'],
            'type': 'all'
        }
        res = self.get_request(f'/api/v2/funds/view', params)
        return res

    def fetch_funds_v1(self, payload):
        params = {
            'client_id': payload['client_id'],
            'type': 'all'
        }
        res = self.get_request(f'/api/v1/funds/view', params)
        return res

    def create_alert(self, payload):
        data = {
            'exchange': payload['exchange'],
            'instrument_token': payload['instrument_token'],
            'wait_time': payload['wait_time'],
            'condition': payload['condition'],
            'user_set_values': payload['user_set_values'],
            'frequency': payload['frequency'],
            'expiry': payload['expiry'],
            'state_after_expiry': payload['state_after_expiry'],
            'user_message': payload['user_message']
        }
        res = self.post_request(f'/api/v1/alerts', data)
        return res

    def fetch_alerts(self):
        params = {}
        res = self.get_request(f'/api/v1/alerts', params)
        return res

    def update_alert(self, payload):
        data = {
            'exchange': payload['exchange'],
            'instrument_token': payload['instrument_token'],
            'wait_time': payload['wait_time'],
            'condition': payload['condition'],
            'user_set_values': payload['user_set_values'],
            'frequency': payload['frequency'],
            'expiry': payload['expiry'],
            'state_after_expiry': payload['state_after_expiry'],
            'user_message': payload['user_message']
        }
        res = self.put_request(f'/api/v1/alerts', data)
        return res

    def run_socket(self, message_type, payload):
        client_id = self.client_id
        access_token = self.access_token
        base_url = self.base_url
        socket_connect(client_id, access_token, message_type, payload, websocket_url)

    def subscribe_detailed_marketdata():
        data = read_detailed_marketdata()
        return data

    def subscribe_compact_marketdata():
        data = read_compact_marketdata()
        return data

    def subscribe_snapquote_data():
        data = read_snapqotedata()
        return data


#------------------------------------------------
#For testing
#------------------------------------------------
#
#
# if __name__ == "__main__":
#     client_id = "*******-TEST"
#     client_secret = "****************BLTBYJn10gYLYIWJqpOcn9zEYI96SJRzZ1"
#     redirect_url = "http://127.0.0.1:*****"
#     base_url = "https://***********.in"
#     conn = Connect(client_id, client_secret, redirect_url, base_url)
#     access_token = conn.get_access_token()
#
#     ##Run api
#     # payload={
#     #     "client_id": "***********"
#     # }
#     # res = conn.fetch_profile(payload)
#     # print(res)
#
#     ##Run Socket
#
#     conn.run_socket("marketdata", {
#         'exchangeCode': 1,
#         'instrumentToken': 3045
#     })


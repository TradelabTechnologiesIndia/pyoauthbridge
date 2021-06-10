import requests
import json
from server import Server
from threading import Thread 
from wsclient import socket_connect, get_compact_marketdata, get_detailed_marketdata, get_snapquotedata, send_message, get_ws_connection_status, unsubscribe_update, get_order_update, get_multiple_detailed_marketdata, get_multiple_compact_marketdata, get_multiple_snapquotedata
import sys
import time

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
        redirect_url_split = redirect_url.split(":")
        if (int(redirect_url_split[2])) :
            self.port = int(redirect_url_split[2])
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
        print('Open this url in browser:', 'http://127.0.0.1:' + str(self.port) + '/getcode', end='\n\n')
        app.run(host='127.0.0.1', debug=False, port=self.port)
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
        oms_order_id = payload['oms_order_id']
        res = self.delete_request(f'/api/v1/orders/{oms_order_id}', params)
        return res

    def fetch_scripinfo(self, payload):
        params = {
            'info': 'scrip',
            'token': payload['token']
        }
        exchange = payload["exchange"]
        res = self.get_request(f'/api/v1/contract/{exchange}', params)
        return res

    def search_scrip(self, payload):
        params = {
            'key': payload['key']
        }
        res = self.get_request(f'/api/v1/search', params)
        return res

    def fetch_scrip_price(self, payload):
        params = {}
        exchange = payload['exchange']
        token = payload['token']
        if exchange == 'NSE':
            ltp_res = self.get_request(f'/api/v1/marketdata/NSE/Capital?token={token}&key=last_trade_price', params)
            close_price_res = self.get_request(f'/api/v1/marketdata/NSE/Capital?token={token}&key=close_price', params)
        elif exchange == 'BSE':
            ltp_res = self.get_request(f'/api/v1/marketdata/BSE/Capital?token={token}&key=last_trade_price', params)
            close_price_res = self.get_request(f'/api/v1/marketdata/BSE/Capital?token={token}&key=close_price', params)
        elif exchange == 'NFO':
            ltp_res = self.get_request(f'/api/v1/marketdata/NSE/FutOpt?token={token}&key=last_trade_price', params)
            close_price_res = self.get_request(f'/api/v1/marketdata/NSE/FutOpt?token={token}&key=close_price', params)
        elif exchange == 'CDS':
            ltp_res = self.get_request(f'/api/v1/marketdata/NSE/Currency?token={token}&key=last_trade_price', params)
            close_price_res = self.get_request(f'/api/v1/marketdata/NSE/Currency?token={token}&key=close_price', params)
        elif exchange == 'MCX':
            ltp_res = self.get_request(f'/api/v1/marketdata/MCX/FutOpt?token={token}&key=last_trade_price', params)
            close_price_res = self.get_request(f'/api/v1/marketdata/MCX/FutOpt?token={token}&key=close_price', params)
        else:
            ltp_res = {"data": 0, "message": "Exchange is ---- invalid", "status": "error"}
            close_price_res = {"data": 0, "message": "Exchange is invalid", "status": "error"}
        if (ltp_res["status"] == "error" or close_price_res["status"] == "error"):
            res = {"last_traded_price": 0, "close_price": 0, "status": "error", "message": ltp_res['message']}
        else:
            res = {"last_traded_price": ltp_res['data'], "close_price": close_price_res['data'], "status": "success", "message": ""}
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
        oms_order_id = payload['oms_order_id']
        res = self.get_request(f'/api/v1/order/{oms_order_id}/history', params)
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

    def run_socket(self):
        client_id = self.client_id
        access_token = self.access_token
        websocket_url = self.websocket_url
        th_websocket = Thread(target=socket_connect, args=(client_id, access_token, websocket_url,))
        th_websocket.start()
        counter = 0
        while True:
            status = get_ws_connection_status()
            if status == True:
                return True
            time.sleep(1)
            counter = counter + 1
            if counter > 5:
                return False
        # socket_connect(client_id, access_token, websocket_url)

    def subscribe_detailed_marketdata(self, detailedmarketdata_payload):
        subscription_pkt = [[detailedmarketdata_payload['exchangeCode'], detailedmarketdata_payload['instrumentToken']]]
        th_detailed_marketdata = Thread(target=send_message, args=('DetailedMarketDataMessage', subscription_pkt))
        th_detailed_marketdata.start()

    def read_detailed_marketdata(self):
        data = get_detailed_marketdata()
        return data

    def unsubscribe_detailed_marketdata(self, detailedmarketdata_payload):
        unsubscription_pkt = [[detailedmarketdata_payload['exchangeCode'], detailedmarketdata_payload['instrumentToken']]]
        th_detailed_marketdata = Thread(target=unsubscribe_update, args=('DetailedMarketDataMessage', unsubscription_pkt))
        th_detailed_marketdata.start()

    def subscribe_compact_marketdata(self, compactmarketdata_payload):
        subscription_pkt = [[compactmarketdata_payload['exchangeCode'], compactmarketdata_payload['instrumentToken']]]
        th_compact_marketdata = Thread(target=send_message, args=('CompactMarketDataMessage', subscription_pkt))
        th_compact_marketdata.start()

    def unsubscribe_compact_marketdata(self, compactmarketdata_payload):
        unsubscription_pkt = [[compactmarketdata_payload['exchangeCode'], compactmarketdata_payload['instrumentToken']]]
        th_compact_marketdata = Thread(target=unsubscribe_update, args=('CompactMarketDataMessage', unsubscription_pkt))
        th_compact_marketdata.start()
    
    def read_compact_marketdata(self):
        data = get_compact_marketdata()
        return data

    def subscribe_snapquote_data(self, snapquotedata_payload):
        subscription_pkt = [[snapquotedata_payload['exchangeCode'], snapquotedata_payload['instrumentToken']]]
        th_snapquote = Thread(target=send_message, args=('SnapquoteDataMessage', subscription_pkt))
        th_snapquote.start()
    
    def unsubscribe_snapquote_data(self, snapquotedata_payload):
        unsubscription_pkt = [[snapquotedata_payload['exchangeCode'], snapquotedata_payload['instrumentToken']]]
        th_snapquote = Thread(target=unsubscribe_update, args=('SnapquoteDataMessage', unsubscription_pkt))
        th_snapquote.start()

    def read_snapquote_data(self):
        data = get_snapquotedata()
        return data

    def subscribe_order_update(self, orderupdate_payload):
        subscription_pkt = [orderupdate_payload['client_id'], "web"]
        th_order_update = Thread(target=send_message, args=('OrderUpdateMessage', subscription_pkt))
        th_order_update.start()
    
    def unsubscribe_order_update(self, orderupdate_payload):
        unsubscription_pkt = [orderupdate_payload['client_id'], "web"]
        th_order_update = Thread(target=unsubscribe_update, args=('OrderUpdateMessage', unsubscription_pkt))
        th_order_update.start()

    def read_order_update_data(self):
        data = get_order_update()
        return data

    def subscribe_multiple_detailed_marketdata(self, detailedmarketdata_payload):
        subscription_pkt = []
        for payload in detailedmarketdata_payload:
            pkt = [payload['exchangeCode'], payload['instrumentToken']]
            subscription_pkt.append(pkt)
        th_detailed_marketdata = Thread(target=send_message, args=('DetailedMarketDataMessage', subscription_pkt))
        th_detailed_marketdata.start()

    def unsubscribe_multiple_detailed_marketdata(self, detailedmarketdata_payload):
        unsubscription_pkt = []
        for payload in detailedmarketdata_payload:
            pkt = [payload['exchangeCode'], payload['instrumentToken']]
            unsubscription_pkt.append(pkt)
        th_detailed_marketdata = Thread(target=unsubscribe_update, args=('DetailedMarketDataMessage', unsubscription_pkt))
        th_detailed_marketdata.start()

    def read_multiple_detailed_marketdata(self):
        data = get_multiple_detailed_marketdata()
        return data

    def subscribe_multiple_compact_marketdata(self, compactmarketdata_payload):
        subscription_pkt = []
        for payload in compactmarketdata_payload:
            pkt = [payload['exchangeCode'], payload['instrumentToken']]
            subscription_pkt.append(pkt)
        th_compact_marketdata = Thread(target=send_message, args=('CompactMarketDataMessage', subscription_pkt))
        th_compact_marketdata.start()

    def unsubscribe_multiple_compact_marketdata(self, compactmarketdata_payload):
        unsubscription_pkt = []
        for payload in compactmarketdata_payload:
            pkt = [payload['exchangeCode'], payload['instrumentToken']]
            unsubscription_pkt.append(pkt)
        th_compact_marketdata = Thread(target=unsubscribe_update, args=('CompactMarketDataMessage', unsubscription_pkt))
        th_compact_marketdata.start()

    def read_multiple_compact_marketdata(self):
        data = get_multiple_compact_marketdata()
        return data

    def subscribe_multiple_snapquote_data(self, snapquotedata_payload):
        subscription_pkt = []
        for payload in snapquotedata_payload:
            pkt = [payload['exchangeCode'], payload['instrumentToken']]
            subscription_pkt.append(pkt)
        th_snapquotetdata = Thread(target=send_message, args=('SnapquoteDataMessage', subscription_pkt))
        th_snapquotetdata.start()

    def unsubscribe_multiple_snapquote_data(self, snapquotedata_payload):
        unsubscription_pkt = []
        for payload in snapquotedata_payload:
            pkt = [payload['exchangeCode'], payload['instrumentToken']]
            unsubscription_pkt.append(pkt)
        th_snapquotetdata = Thread(target=unsubscribe_update, args=('SnapquoteDataMessage', unsubscription_pkt))
        th_snapquotetdata.start()

    def read_multiple_snapquote_data(self):
        data = get_multiple_snapquotedata()
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


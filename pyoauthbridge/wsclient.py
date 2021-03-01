import websocket
import threading
import json
import time
from struct import pack_into
import ctypes, struct
from packetDecoder import decodeDetailedMarketData, decodeCompactMarketData, decodeSnapquoteData

login_id = "",
access_token = "",
payload = {},
websock = {},
compact_marketdata_response = {},
detailed_marketdata_response = {},
snapquote_marketdata_response = {}

def get_detailed_marketdata():
    return detailed_marketdata_response

def get_compact_marketdata():
    return compact_marketdata_response

def get_snapquotedata():
    return snapquote_marketdata_response

def heartbeat_thread(clientSocket):
    while clientSocket:
        send_data = '{"a": "h", "v": [], "m": ""}'
        try:
            clientSocket.send(send_data)
        except Exception as e:
            print(e)
            print("HEARTBEAT [ERROR]: [BLITZ_HYDRA_STREAM] Connection closed.")
            break
        print("Sent Heart-Beat to Exchange")
        time.sleep(8)


def on_message(ws, message):
    mode = struct.unpack('>b', message[0:1])[0]
    if mode == 1:
        res = decodeDetailedMarketData(message)
        # print("detailed market data")
        # print(res)
        global detailed_marketdata_response
        detailed_marketdata_response = res
    elif mode == 2:
        res = decodeCompactMarketData(message)
        global compact_marketdata_response
        compact_marketdata_response = res
    elif mode == 4:
        res = decodeSnapquoteData(message)
        # print("snap quote data")
        # print(res)
        global snapquote_marketdata_response
        snapquote_marketdata_response = res

def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):

    hbThread = threading.Thread(target=heartbeat_thread, args=(ws,))
    hbThread.start()

    # hbThread1 = threading.Thread(target=send_message, args=(ws,))
    # hbThread1.start()



def send_message(message_type, payload):
    # print(message_type)
    global websock
    clientSocket = websock
    print(clientSocket)
    if message_type == "DetailedMarketDataMessage":
        sub_packet = {
            "a": "subscribe",
            "v": [[payload['exchangeCode'], payload['instrumentToken']]],
            "m": "marketdata"
        }
        clientSocket.send(json.dumps(sub_packet))
    elif message_type == "CompactMarketDataMessage":
        sub_packet = {
            "a": "subscribe",
            "v": [[payload['exchangeCode'], payload['instrumentToken']]],
            "m": "compact_marketdata"
        }
        clientSocket.send(json.dumps(sub_packet))
    elif message_type == "SnapquoteDataMessage":
        sub_packet = {
            "a": "subscribe",
            "v": [[payload['exchangeCode'], payload['instrumentToken']]],
            "m": "full_snapquote"
        }
        clientSocket.send(json.dumps(sub_packet))
    elif message_type == "TbtSnapquoteDataMessage":
        sub_packet = {
            "a": "subscribe",
            "v": [[payload['exchangeCode'], payload['instrumentToken']]],
            "m": "tbt_full_snapquote"
        }
        clientSocket.send(json.dumps(sub_packet))
    elif message_type == "OrderUpdate":
        sub_packet = {
            "a": "subscribe",
            "v": [payload['client_id'], "web"],
            "m": "updates"
        }
        print(sub_packet)
        clientSocket.send(json.dumps(sub_packet))
    elif message_type == "TradeUpdate": 
        sub_packet = {
            "a": "subscribe",
            "v": [[payload['client_id'], "web"]],
            "m": "updates"
        }
        clientSocket.send(json.dumps(sub_packet))
    elif message_type == "ExchangeMessage": 
        sub_packet = {
            "a": "subscribe",
            "v": [payload['client_id']],
            "m": "exchange_messages"
        }
        clientSocket.send(json.dumps(sub_packet))
    elif message_type == "PositionUpdate":
        sub_packet = {
            "a": "subscribe",
            "v": [[payload['client_id'], "web"]],
            "m": "position_updates"
        }
        clientSocket.send(json.dumps(sub_packet))

def connect(base_url):
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(f"{base_url}",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    return ws

def webs_start(ws):
    ws.run_forever()

def socket_connect(client_id, token, websocket_url):

    global websock
    websock = connect(f'{websocket_url}/ws/v1/feeds?login_id={client_id}&access_token={token}')
    # print(message_type)
    hbThread2 = threading.Thread(target=webs_start, args=(websock,))
    hbThread2.run()
    hbThread2.isAlive()

import ctypes, struct
from struct import pack_into

def decodeDetailedMarketData(packet_buffer):
  return {
    "mode" : struct.unpack('>b', packet_buffer[0:1])[0],
    "exchange_code" : struct.unpack('>b', packet_buffer[1:2])[0],
    "instrument_token" : struct.unpack('>I', packet_buffer[2:6])[0],
    "last_traded_price" : struct.unpack('>I', packet_buffer[6:10])[0],
    "last_traded_time" : struct.unpack('>I', packet_buffer[10:14])[0],
    "last_traded_quantity" : struct.unpack('>I', packet_buffer[14:18])[0],
    "trade_volume" : struct.unpack('>I', packet_buffer[18:22])[0],
    "best_bid_price" : struct.unpack('>I', packet_buffer[22:26])[0],
    "best_bid_quantity" : struct.unpack('>I', packet_buffer[26:30])[0],
    "best_ask_price" : struct.unpack('>I', packet_buffer[30:34])[0],
    "best_ask_quantity" : struct.unpack('>I', packet_buffer[34:38])[0],
    "total_buy_quantity" : struct.unpack('>Q', packet_buffer[38:46])[0],
    "total_sell_quantity" : struct.unpack('>Q', packet_buffer[46:54])[0],
    "average_trade_price" : struct.unpack('>I', packet_buffer[54:58])[0],
    "exchange_timestamp" : struct.unpack('>I', packet_buffer[58:62])[0],
    "open_price" : struct.unpack('>I', packet_buffer[62:66])[0],
    "high_price" : struct.unpack('>I', packet_buffer[66:70])[0],
    "low_price" : struct.unpack('>I', packet_buffer[70:74])[0],
    "close_price" : struct.unpack('>I', packet_buffer[74:78])[0],
    "yearly_high_price" : struct.unpack('>I', packet_buffer[78:82])[0],
    "yearly_low_price" : struct.unpack('>I', packet_buffer[82:86])[0],
    "lowDPR": struct.unpack('>I', packet_buffer[86:90])[0],
    "highDPR": struct.unpack('>I', packet_buffer[90:94])[0],
    "currentOpenInterest": struct.unpack('>I', packet_buffer[94:98])[0],
    "initialOpenInterest": struct.unpack('>I', packet_buffer[98:102])[0],
  }

def decodeCompactMarketData(packet_buffer):
  return {
    "mode" : struct.unpack('>b', packet_buffer[0:1])[0],
    "exchange_code" : struct.unpack('>b', packet_buffer[1:2])[0],
    "instrument_token" : struct.unpack('>I', packet_buffer[2:6])[0],
    "last_traded_price" : struct.unpack('>I', packet_buffer[6:10])[0],
    "change": struct.unpack('>I', packet_buffer[10:14])[0],
    "last_traded_time": struct.unpack('>I', packet_buffer[14:18])[0],
    "lowDPR": struct.unpack('>I', packet_buffer[18:22])[0],
    "highDPR": struct.unpack('>I', packet_buffer[22:26])[0],
    "currentOpenInterest": struct.unpack('>I', packet_buffer[26:30])[0],
    "initialOpenInterest": struct.unpack('>I', packet_buffer[30:34])[0],
    "bidPrice": struct.unpack('>I', packet_buffer[34:38])[0],
    "askPrice": struct.unpack('>I', packet_buffer[38:42])[0],
  }

def decodeSnapquoteData(packet_buffer):
  return {
    "mode" : struct.unpack('>b', packet_buffer[0:1])[0],
    "exchange_code" : struct.unpack('>b', packet_buffer[1:2])[0],
    "instrument_token" : struct.unpack('>I', packet_buffer[2:6])[0],
    "buyers": [
      struct.unpack('>I', packet_buffer[6:10])[0],
      struct.unpack('>I', packet_buffer[10:14])[0],
      struct.unpack('>I', packet_buffer[14:18])[0],
      struct.unpack('>I', packet_buffer[18:22])[0],
      struct.unpack('>I', packet_buffer[22:26])[0]
    ],
    "bidPrices": [
      struct.unpack('>I', packet_buffer[26:30])[0],
      struct.unpack('>I', packet_buffer[30:34])[0],
      struct.unpack('>I', packet_buffer[34:38])[0],
      struct.unpack('>I', packet_buffer[38:42])[0],
      struct.unpack('>I', packet_buffer[42:46])[0]
    ],
    "bidQtys": [
      struct.unpack('>I', packet_buffer[46:50])[0],
      struct.unpack('>I', packet_buffer[50:54])[0],
      struct.unpack('>I', packet_buffer[54:58])[0],
      struct.unpack('>I', packet_buffer[58:62])[0],
      struct.unpack('>I', packet_buffer[62:66])[0]
    ],
    "sellers": [
      struct.unpack('>I', packet_buffer[66:70])[0],
      struct.unpack('>I', packet_buffer[70:74])[0],
      struct.unpack('>I', packet_buffer[74:78])[0],
      struct.unpack('>I', packet_buffer[78:82])[0],
      struct.unpack('>I', packet_buffer[82:86])[0]
    ],
    "askPrices": [
      struct.unpack('>I', packet_buffer[86:90])[0],
      struct.unpack('>I', packet_buffer[90:94])[0],
      struct.unpack('>I', packet_buffer[94:98])[0],
      struct.unpack('>I', packet_buffer[98:102])[0],
      struct.unpack('>I', packet_buffer[102:106])[0]
    ],
    "askQtys": [
      struct.unpack('>I', packet_buffer[106:110])[0],
      struct.unpack('>I', packet_buffer[110:114])[0],
      struct.unpack('>I', packet_buffer[114:118])[0],
      struct.unpack('>I', packet_buffer[118:122])[0],
      struct.unpack('>I', packet_buffer[122:126])[0]
    ],
    "averageTradePrice": struct.unpack('>I', packet_buffer[126:130])[0],
    "open": struct.unpack('>I', packet_buffer[130:134])[0],
    "high": struct.unpack('>I', packet_buffer[134:138])[0],
    "low" : struct.unpack('>I', packet_buffer[138:142])[0],
    "close" : struct.unpack('>I', packet_buffer[142:146])[0],
    "totalBuyQty" : struct.unpack('>Q', packet_buffer[146:154])[0],
    "totalSellQty": struct.unpack('>Q', packet_buffer[154:162])[0],
    "volume" : struct.unpack('>I', packet_buffer[162:166])[0],
  }
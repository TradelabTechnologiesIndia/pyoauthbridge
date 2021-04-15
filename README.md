# pyoauthbridge

pyoauthbridge is a official python library to communicate with Tradelab API.

### Prerequisites

* Please refer the document http://primusapi.tradelab.in/webapi/
* This API uses OAuth 2.0 protocol . You will need following to get started -(Please contact your broker team to get these details)
```
app_id
app_secret
redirect_url
base_url
```

### Installation

pyoauthbridge requires [python](https://www.python.org/) v3+ to run.

Install the package using pip.

```sh
$ pip3 install pyoauthbridge
```

### How to use

import package
```sh
from pyoauthbridge import Connect
```

Get access token
```sh
conn = Connect(app_id, app_secret, redirect_url, base_url)
access_token = conn.get_access_token()
```

#### Open the link in your browser displayed in terminal. Complete your login process.

If the user has access_token , it can be set without calling get_access_token()
```sh
conn.set_access_token(access_token)
```

implementation
```sh
payload = {
    'client_id': 'JOHN'
}
res = conn.fetch_profile(payload)
print(res)
```

### Websocket implementation

```sh

# To connect to websocket
ws_status = conn.run_socket()

# To subscribe to Detailed Market Data Message
conn.subscribe_detailed_marketdata({'exchangeCode': 4, 'instrumentToken': 226027})

# To subscribe to Compact Market Data 
conn.subscribe_compact_marketdata({'exchangeCode': 4, 'instrumentToken': 226027})

# To subscribe to Snapquote Data 
conn.subscribe_snapquote_data({'exchangeCode': 4, 'instrumentToken': 226027})

# To read/listen to Detailed Market Data
detailed_market_data = conn.read_detailed_marketdata()

# To read/listen to Compact Market Data
compact_market_data = conn.read_compact_marketdata()

# To read/listen to Snapquote Data
snapquote_data = conn.read_snapquote_data()

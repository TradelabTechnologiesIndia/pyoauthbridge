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

Set access token
```sh
conn.set_token(auth_token)
```

implementation
```sh
payload = {
    'client_id': 'JOHN'
}
res = conn.fetch_profile(payload)
print(res)
```

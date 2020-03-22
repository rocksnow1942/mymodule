import requests
import json
from datetime import datetime

datetime.now().strftime('%c')
gist : bfe7a685c025a4b4eb203e72e6e530d5c57adf82

url = "https://api.github.com/gists/07afd0ad32a04a231382906a12af7eed"

https://gist.github.com/07afd0ad32a04a231382906a12af7eed

headers = {
    'Authorization' : 'token bfe7a685c025a4b4eb203e72e6e530d5c57adf82',
    'Content-Type' : 'applicaiton/json'
}

data = {
  "description": "Hello World Examples",
  "files": {
    "new.json": {
      "content": "Run `ruby hello_world.rb` or `python hello_world.py` to print Hello World",

    },

  }
}

res= requests.patch(url,headers = headers,data=json.dumps(data))
res
res.status_code == 200

print(json.dumps(res.json(),indent=2))
print()
{"message":"Not Found","documentation_url":"https://developer.github.com/v3/gists/#edit-a-gist"}

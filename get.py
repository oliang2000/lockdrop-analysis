import requests
import json

# url = 'https://api.etherscan.io/api?module=logs&action=getLogs&address=0x458dabf1eff8fcdfbf0896a6bd1f457c01e2ffd6&fromBlock=0&toBlock=latest&sort=asc'
url = 'https://api.etherscan.io/api?module=account&action=txlist&address=0x458dabf1eff8fcdfbf0896a6bd1f457c01e2ffd6&startblock=0&endblock=latest&sort=asc'
headers = {"content-type": "application/json"}
r = requests.get(url, headers=headers)
data = r.json()
print(json.dumps(data, indent=4))

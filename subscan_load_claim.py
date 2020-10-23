import urllib.request
import json
import time

url = 'https://plasm.subscan.io/api/scan/events'
req_header = {
    'Content-Type': 'application/json',
}

froot = './data/2ndclaim'

for i in range(0,500):
    time.sleep(1)
    req_data = json.dumps({
        "row":25,
        "page":i,
        "call":"claimrequest",
        "module":"plasmlockdrop"
    })
    req = urllib.request.Request(url, data=req_data.encode(), method='POST', headers=req_header)
    fname = "{}/{}_events.json".format(froot,i)
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read())
            headers = response.getheaders()
            status = response.getcode()

            print(headers)
            print(status)
            print(body)
            print(fname)

            # d = json.loads(body)
            if body["data"]["events"] == None:
                exit(0)
            with open(fname, 'w') as f:
                json.dump(body, f)

    except urllib.error.URLError as e:
        print(e.reason)
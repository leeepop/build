import requests
import json
import os

napi = os.environ['NGROK_API']
cf = os.environ['CF_API']
zone = os.environ['ZONE']
domain = os.environ['DOMAIN']
service = os.environ['SERVICE']

headers = {
        "Authorization": "Bearer "+napi,
        "Ngrok-Version": "2"
        }

r = requests.get('https://api.ngrok.com/tunnels',headers=headers)
r = json.loads(r.text)
url = r["tunnels"][0]["public_url"][6:]
print(url)
id = url[0]
print(id)
port = url[-5:]
print(port)
headers = {
            'Authorization': 'Bearer '+cf,
            'Content-Type': 'application/json'
        }
try:
        r = requests.get('https://api.cloudflare.com/client/v4/zones/+'zone'/dns_records?type=SRV',headers=headers)
        r = json.loads(r.text)
        idd = r["result"][0]["id"]
        print(idd)
        r = requests.delete('https://api.cloudflare.com/client/v4/zones/+'zone'+/dns_records/'+idd,headers=headers)
except:
        print('Nothing to delete')
data = {
            "type":"SRV",
            "data":{
                "name": domain,
                "port": port,
                "priority":1,
                "proto":"_tcp",
                "service":service,
                "target": id+".tcp.ngrok.io",
                "weight":1,
                "ttl":1,
            }
        }
a = requests.post('https://api.cloudflare.com/client/v4/zones/'+zone+'/dns_records',headers = headers,data = json.dumps(data))
print(a.text)

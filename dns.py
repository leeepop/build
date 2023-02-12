import requests
import json
import os
import socket
napi = os.environ['NGROK_API']
cf = os.environ['CF_API']
zone = os.environ['ZONEID']
domain = os.environ['DOMAIN']
domain2 = os.environ['DOMAIN2']
service = os.environ['SERVICE']
def get_ip_address(domain_name):
    try:
        return socket.gethostbyname(domain_name)
    except socket.gaierror as e:
        print("Error resolving hostname: %s" % e)
        return None
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
ip = get_ip_address(id+".tcp.ngrok.io")
headers = {
            'Authorization': 'Bearer '+cf,
            'Content-Type': 'application/json'
        }
try:
        r = requests.get('https://api.cloudflare.com/client/v4/zones/'+zone+'/dns_records?type=A&name='+domain2,headers=headers)
        r = json.loads(r.text)
        idd = r["result"][0]["id"]
        print(idd)
        r = requests.delete('https://api.cloudflare.com/client/v4/zones/'+zone+'/dns_records/'+idd,headers=headers)
except:
        print('No A to delete')

data = {
    "type":"A",
    "data":{
        "name": domain2,
        "content": ip,
        "ttl":1,
    }
}
a = requests.post('https://api.cloudflare.com/client/v4/zones/'+zone+'/dns_records',headers = headers,data = json.dumps(data))
try:
        r = requests.get('https://api.cloudflare.com/client/v4/zones/'+zone+'/dns_records?type=SRV',headers=headers)
        r = json.loads(r.text)
        idd = r["result"][0]["id"]
        print(idd)
        r = requests.delete('https://api.cloudflare.com/client/v4/zones/'+zone+'+/dns_records/'+idd,headers=headers)
except:
        print('No SRV to delete')
data = {
            "type":"SRV",
            "data":{
                "name": domain,
                "port": port,
                "priority":1,
                "proto":"_tcp",
                "service":service,
                "target": domain2,
                "weight":1,
                "ttl":1,
            }
        }
a = requests.post('https://api.cloudflare.com/client/v4/zones/'+zone+'/dns_records',headers = headers,data = json.dumps(data))
print(a.text)

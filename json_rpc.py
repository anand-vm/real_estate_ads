import urllib.request
import json
import random

# Odoo connection details
url = "http://localhost:8069"
username = "admin@catalistindia.in"
password = "admin"
db = "db_1"

def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    headers = {"Content-Type": "application/json"}
    data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data, headers)

    response_data = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
    if response_data.get('error'):
        raise Exception(response_data['error'])
    return response_data['result']

def call(url, service, method, *args):
    return json_rpc(f"{url}/jsonrpc", "call", {"service": service, "method": method, "args": args})

user_id = call(url, "common", "authenticate", db, username, password, {})

print("user ID :", user_id)

vasl = { "name": "JSON Property", "description": "Description of the property", "price": 100000, "bedrooms": 3, "bathrooms": 2, "property_type": "House", "property_status": "For Sale" }

# # crate property
# create_property = call(url, "object", "execute", db, user_id, password, 'estate.property,', 'create', vasl)   
# print(create_property)

# Read property
read_property = call(url, "object", "execute", db, user_id, password, 'estate.property', 'read', [1])
print(read_property)

# New method : odooRPC
# URL : https://pythonhosted.org/OdooRPC/
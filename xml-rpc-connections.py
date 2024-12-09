import xmlrpc.client

# Odoo connection details
url = "http://localhost:8069"
username = "admin@catalistindia.in"
password = "admin"
db = "db_1"

# Create a connection to the common endpoint
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")

user_uid = common.authenticate(db, username, password, {})

# Print Odoo version
# print(common.version())
print(user_uid)

'xmlrpc/2/object' 'execute_kw' 
'db, uid, password, model_name, method_name, [], {}'

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# search function
property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'search', [[]])
print("search Function :", property_ids)

#count function
count = models.execute_kw(db, user_uid, password, 'estate.property', 'search_count', [[]])
print("Count Function :", count)

#Read function
read_property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'read', [property_ids], {'fields': ['name']})
print("Read Function :", read_property_ids)

#create function
create_property_id = models.execute_kw(db, user_uid, password, 'estate.property', 'create', [{
    'name': 'Property 1'}])

#write function
write_function_id = models.execute_kw(db, user_uid, password, 'estate.property', 'write', [create_property_id], {'name': 'Property 1 Updated'})

#unlink function
delete_function_id = models.execute_kw(db, user_uid, password, 'estate.property', 'unlink', [create_property_id])   

# Read with page and page_size
read_with_pagination = models.execute_kw(db, user_uid, password, 'estate.property', 'read', [[]], {'page': 1, 'page_size': 2})



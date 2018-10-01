import requests
import json
from random import randint

random_user_number = randint(0, 5000)

print("USER ID : " + str(random_user_number))

headers = {'content-type': 'application/json'}


print("\n---------------------------BEGIN-------------------------------------\n")


url = "http://explorer.blockwala.io:8000/api/createStoreEntry"

random_store_number = randint(0, 5000)

data = {"id": random_store_number, "name":"Shop Store number " + str(random_store_number), "user_id": random_user_number}

response = requests.post(url, params=None, data=json.dumps(data), headers=headers)

if(response.status_code == 200):
    print("STORE entry created successfully with id " + str(random_store_number))


print("\n----------------------------------------------------------------\n")


url = "http://explorer.blockwala.io:8000/api/createBranchEntry"

random_branch_number = randint(0, 5000)

data = {
        "id": random_branch_number,
        "name":"Branch number " + str(random_branch_number),
        "store_id": random_store_number,
        "user_id": random_user_number
        }

response = requests.post(url, params=None, data=json.dumps(data), headers=headers)

if(response.status_code == 200):
    print("BRANCH entry created successfully with id " + str(random_branch_number) + " for STORE number " + str(random_store_number))


print("\n----------------------------------------------------------------")

url = "http://explorer.blockwala.io:8000/api/createItemEntry"

random_item_number = randint(0, 5000)

data = {
	"name":"name "+str(random_item_number),
	"brand": "brand "+str(random_item_number),
	"category": "category "+str(random_item_number),
	"product_code":random_item_number,
	"branch_id":random_branch_number,
    "user_id": random_user_number
}

response = requests.post(url, params=None, data=json.dumps(data), headers=headers)

if(response.status_code == 200):
    print("ITEM entry created successfully with product_code " + str(random_item_number) +  " for BRANCH number " + str(random_branch_number) )

print("\n----------------------------------------------------------------\n")


url = "http://explorer.blockwala.io:8000/api/create_variant_entry"

random_variant_number = randint(0,5000)

data = {
	"item_product_code": random_item_number,
	"variant_name": "variant "+str(random_variant_number),
	"selling_price": randint(200,400),
	"cost_price": randint(0,200),
	"quantity": randint(0,100),
	"properties": {
		"size":"small",
        "color":"red",
        "cloth":"cotton"
	},
	"variant_code": random_variant_number,
	"user_id": random_user_number
}

response = requests.post(url, params=None, data=json.dumps(data), headers=headers)

if(response.status_code == 200):
    print("VARIANT entry created successfully with product_code " + str(random_variant_number) + " of ITEM number "+ str(random_item_number))


print("\n---------------------------LOGS-------------------------------------\n")

url = "http://explorer.blockwala.io:8000/api/getLogs"

data = {
	"user_id": random_user_number
}

response = requests.post(url, params=None, data=json.dumps(data), headers=headers)

if(response.status_code == 200):
    jsonData = json.loads(response.text)['Logs'];
    for log in jsonData:
        print("\n")
        for key, value in log.iteritems():
            print(str(key) + ": "+str(value))

#Inventory project for Weavedin by Karan

Project is made on Django using SqlAlchemy as ORM

##APIs

###/api/createStoreEntry

Request:

{
	"id":12,
	"name":"shopStore",
  "user_id": 24,
}


Response:

{
    "Success": "true"
}


###/api/createBranchEntry

Request:

{
	"id":123,
	"name":"shopStoreBranch1",
	"store_id":12,
  	"user_id": 24,
}



Response:

{
    "Success": "true"
}



###/api/createItemEntry/

Request:

{
	"name":"pant",
	"brand": "c&h",
	"category": "clothes",
	"product_code":121,
	"branch_id":123,
  	"user_id": 24,
}


Response:

{
    "Success": "true"
}


###/api/create_variant_entry


Request:


{
	"item_product_code":121,
	"variant_name": "tshirts",
	"selling_price": 100,
	"cost_price":70,
	"quantity":4,
	"properties": {
		"size":"small",
    "color": "red"
	},
	"variant_code": 21192,
  	"user_id": 24,
}



Response:

{
    "Success": "true"
}



###/api/edit_variants


Request:


{
	"variant_name":"shirt1",
	"variant_code": 21192,
	"properties": {
                "color": "red",
                "size":"large"
            },
    "selling_price": 1000,
    "cost_price": 20,
    "quantity":100,
    	"user_id": 24,
}


Response:


{
    "Success": "true"
}


###/api/get_variants?variant_code=21192


TYPE: GET

Request:

variant_code : optional. if not provided, all data will be returned



Response:


{
    "Items": [
        {
            "item_product_code": 121,
            "variant_name": "shirt1",
            "variant_code": 21192,
            "selling_price": 1000,
            "quantity": 100,
            "properties": {
                "color": "red",
                "size": "Large"
            },
            "cost_price": 20
        }
    ],
    "Success": "true"
}



###/api/getItem?product_code=121


TYPE: GET

Request:

product_code: optional. if not provided, all data will be returned


Response:

{
    "Items": [
        {
            "category": "clothes1",
            "brand": "c&h1",
            "product_code": 121,
            "name": "pant1"
        }
    ],
    "Success": "true"
}



###/api/edit_items

type: POST

Request:

{
	"category": "clothes1",
  "brand": "c&h1",
  "product_code": 121,
  "name": "pant1",
  "user_id": 24,
}


Response:

{
    "Success": "true"
}




###/api/getLogs


type: POST

Request:


All param are optional

{
	"user_id": 24,
	"start_time": 1538401634,
	"end_time": 1538402653
}


Response:

{
    "Logs": [
        {
            "user_id": "unknown",
            "field": "name",
            "value": "pant1",
            "date": "2018-10-01 19:32:24+05:30",
            "action": "update name",
            "table": "items"
        },
        {
            "user_id": "unknown",
            "field": "brand",
            "value": "c&h1",
            "date": "2018-10-01 19:32:24+05:30",
            "action": "update brand",
            "table": "items"
        },
        {
            "user_id": "unknown",
            "field": "category",
            "value": "clothes1",
            "date": "2018-10-01 19:32:24+05:30",
            "action": "update category",
            "table": "items"
        }
    ],
    "Success": "true"
}

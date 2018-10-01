# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

import sqlalchemy, sqlalchemy.orm
from sqlalchemy.exc import SQLAlchemyError

from models import Base, Item, Variant, Store, Branch, User, Logs
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import arrow
import re

engine = sqlalchemy.create_engine(settings.DATABASE_ENGINE)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

'''
create a user
'''
@csrf_exempt
def create_user_entry(request):
    if request.method == 'POST':
        try:
            received_json_data=json.loads(request.body)
            id = received_json_data.get('id','')
            name = received_json_data.get('name','')

            if name == "" or id == "":
                return JsonResponse({"error":"Make sure all Attributes are sent."}, status=500)

            row = User(name=name, id=id)
            session.add(row)
            session.commit()
            create_new_log(id, "create user", "users", "all fields", str(id))
            return JsonResponse({"Success":"true"}, status=200)
        except SQLAlchemyError as e:
            session.rollback()
            return JsonResponse({"success":"false","error":e.message}, status=500)
        except ValueError as e:
            session.rollback()
            return JsonResponse({"success":"false", "error":e.message}, status=500)
    else:
        return JsonResponse({"success":"false", "error":"Method is POST"}, status=500)


'''
create a store
'''
@csrf_exempt
def create_store_entry(request):
    if request.method == 'POST':
        try:
            received_json_data=json.loads(request.body)
            id = received_json_data.get('id','')
            name = received_json_data.get('name','')
            user_id = received_json_data.get('user_id', 'unknown')

            if name == "" or id == "":
                return JsonResponse({"error":"Make sure all Attributes are sent."}, status=500)

            row = Store(name=name, id=id)
            session.add(row)
            session.commit()
            create_new_log(user_id, "create store", "stores", "all fields", str(id))
            return JsonResponse({"Success":"true"}, status=200)
        except SQLAlchemyError as e:
            session.rollback()
            return JsonResponse({"success":"false","error":e.message}, status=500)
        except ValueError as e:
            session.rollback()
            return JsonResponse({"success":"false", "error":e.message}, status=500)
    else:
        return JsonResponse({"success":"false", "error":"Method is POST"}, status=500)


'''
create a branches
if store doesn't exist, return error
'''
@csrf_exempt
def create_branch_entry(request):
    if request.method == 'POST':
        try:
            received_json_data=json.loads(request.body)
            id = received_json_data.get('id','')
            name = received_json_data.get('name','')
            store_id = received_json_data.get('store_id','')
            user_id = received_json_data.get('user_id', 'unknown')

            query = session.query(Store).filter(Store.id == store_id)
            _row = query.first()

            if _row is None:
                return JsonResponse({"success":"false","error":"Store entry with store_id of "+str(store_id)+" not found"}, status=500)

            row = Branch(name=name, id=id, store_id=store_id)
            session.add(row)
            session.commit()
            create_new_log(user_id, "create branch", "branches", "all", str(id))
            return JsonResponse({"Success":"true"}, status=200)
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            return JsonResponse({"success":"false","error":e.message}, status=500)
        except ValueError as e:
            session.rollback()
            return JsonResponse({"success":"false", "error":e.message}, status=500)

    else:
        return JsonResponse({"success":"false", "error":"Method is POST"}, status=500)

    return JsonResponse({"Success":"true"}, status=200)



'''

Takes in the attributes and creates a new item entry

'''
@csrf_exempt
def create_item_entry(request):

    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        name = received_json_data.get('name','')
        brand = received_json_data.get('brand','')
        category = received_json_data.get('category','')
        product_code = received_json_data.get('product_code','')
        branch_id = received_json_data.get('branch_id','')
        user_id = received_json_data.get('user_id', 'unknown')

        if name == "" or brand == "" or category == "" or product_code == "" or branch_id == "":
            return JsonResponse({"error":"Make sure all Attributes are sent."}, status=500)
        try:
            query = session.query(Branch).filter(Branch.id == branch_id)
            _row = query.first()

            if _row is None:
                return JsonResponse({"success":"false","error":"Branch entry with branch_id of "+str(branch_id)+" not found"}, status=500)

            row = Item(name=name, brand=brand, category=category, product_code=product_code)
            session.add(row)
            session.commit()
            create_new_log(user_id, "Create item", "items", "all", str(product_code))
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            return JsonResponse({"success":"false","error":e.message}, status=500)
        except IntegrityError as e:
            session.rollback()
            return JsonResponse({"success":"false","error": e.message}, status=500)
        return JsonResponse({"Success":"true"}, status=200)
    else:
        return JsonResponse({"success":"false", "error":"Method is POST"}, status=500)


'''

Return item from database against given product code. If no product_code
is given, all items are returned , sorted by id.

'''
@csrf_exempt
def get_item(request):

    return_items = []
    if request.method == 'GET':
        product_code =  request.GET.get('product_code','')
        if product_code == "":
            query = session.query(Item).order_by(Item.product_code)
            for _row in query.all():
                print(_row.name, _row.brand, _row.category, _row.product_code)
                json_obj = {"name": _row.name, "brand":_row.brand, "category":_row.category, "product_code":_row.product_code}
                return_items.append(json_obj)
        else:
            query = session.query(Item).filter(Item.product_code == product_code)
            _row = query.first()
            if _row == None:
                return JsonResponse({"success":"false", "error":"No Item found with the product code"}, status=500)
            json_obj = {"name": _row.name, "brand":_row.brand, "category":_row.category, "product_code":_row.product_code}
            return_items.append(json_obj)

        return JsonResponse({"Success":"true", "Items": return_items}, status=200)
    else:
        return JsonResponse({"success":"false", "error":"Method is GET"}, status=500)


'''

Takes in the attributes and creates a new variant entry

checks if properties is a dictionary

then checks if corresponding item occurs

if all is ok, then __init__ the entry and store it in db

'''
@csrf_exempt
def create_variant_entry(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        item_product_code = received_json_data.get('item_product_code','')
        variant_name = received_json_data.get('variant_name','')
        selling_price = received_json_data.get('selling_price','')
        cost_price = received_json_data.get('cost_price','')
        quantity = received_json_data.get('quantity','')
        properties = received_json_data.get('properties','')
        variant_code = received_json_data.get('variant_code','')
        user_id = received_json_data.get('user_id', 'unknown')

        print(properties)

        #Check if property is a dict
        try:
            for k, v in properties.iteritems():
                print(k)
                print(v)
        except AttributeError as e:
            return JsonResponse({"success":"false","error":"Properties should be a dictionary"}, status=500)


        #check if item exists:
        query = session.query(Item).filter(Item.product_code == item_product_code)
        _row = query.first()
        if _row is None:
            return JsonResponse({"success":"false","error":"Item entry for the variant not found"}, status=500)

        #store in db
        try:
            row = Variant(item_product_code=item_product_code, variant_name=variant_name, selling_price=selling_price, cost_price=cost_price, quantity=quantity, variant_code=variant_code, properties=properties)
            session.add(row)
            session.commit()
            create_new_log(user_id, "created variant", "variant", "all", str(variant_code))
        except SQLAlchemyError as e:
            session.rollback()
            return JsonResponse({"success":"false","error": e.message}, status=500)
        except IntegrityError as e:
            session.rollback()
            return JsonResponse({"success":"false","error": e.message}, status=500)

        return JsonResponse({"Success":"true"}, status=200)
    else:
        return JsonResponse({"success":"false", "error":"Method is POST"}, status=500)



'''

Return item from database against given product code. If no variant_code
is given, all items are returned , sorted by id.

'''
@csrf_exempt
def get_variants(request):

    return_items = []
    if request.method == 'GET':
        variant_code =  request.GET.get('variant_code','')
        query = ''

        if variant_code == "":
            #all data
            query = session.query(Variant).order_by(Variant.variant_code)
            for _row in query.all():
                json_obj = {"variant_code": _row.variant_code, "variant_name":_row.variant_name, "selling_price":_row.selling_price, "cost_price":_row.cost_price, "properties":_row.properties, "quantity":_row.quantity, "item_product_code":_row.item_product_code}
                return_items.append(json_obj)
        else:
            #variant code entry
            query = session.query(Variant).filter(Variant.variant_code == variant_code)
            _row = query.first()
            if _row == None:
                return JsonResponse({"success":"false", "error":"No Item found with the product code"}, status=500)
            json_obj = {"variant_code": _row.variant_code, "variant_name":_row.variant_name, "selling_price":_row.selling_price, "cost_price":_row.cost_price, "properties":_row.properties, "quantity":_row.quantity, "item_product_code":_row.item_product_code}
            return_items.append(json_obj)

        return JsonResponse({"Success":"true", "Items": return_items}, status=200)
    else:
        return JsonResponse({"success":"false", "error":"Method is GET"}, status=500)


'''
Takes in 1-8 params and updates variant against variant_code

does not update item_product_code

updates properties
'''
@csrf_exempt
def edit_variants(request):
    if request.method == 'POST':
        try:
            received_json_data=json.loads(request.body)
            item_product_code = received_json_data.get('item_product_code','')
            variant_name = received_json_data.get('variant_name','')
            selling_price = received_json_data.get('selling_price','')
            cost_price = received_json_data.get('cost_price','')
            quantity = received_json_data.get('quantity','')
            properties = received_json_data.get('properties','')
            variant_code = received_json_data.get('variant_code','')
            user_id = received_json_data.get('user_id', 'unknown')

            #sanity
            if variant_code == "":
                return JsonResponse({"success":"false", "error":"variant_code can't be empty"}, status=500)

            if item_product_code != "":
                return JsonResponse({"success":"false", "error":"Item product code can't be updated"}, status=500)

            #query row
            variant = session.query(Variant).filter(Variant.variant_code == variant_code).first()

            if variant == None:
                return JsonResponse({"success":"false", "error": "Variant not found with id "+str(variant_code)}, status=500)

            #check for updates
            if variant_name != "" :
                create_new_log(user_id, "edit name", "variant", "name", variant_name)
                variant.variant_name = variant_name
            if selling_price != "":
                create_new_log(user_id, "edit selling_price", "variant", "selling_price", selling_price)
                variant.selling_price = selling_price
            if cost_price != "":
                create_new_log(user_id, "edit cost_price", "variant", "cost_price",  cost_price)
                variant.cost_price = cost_price
            if quantity != "":
                create_new_log(user_id, "edit quantity", "variant", "quantity", quantity)
                variant.quantity = quantity
            if variant_code != "":
                create_new_log(user_id, "edit variant_code", "variant", "variant_code", variant_code)
                variant.variant_code = variant_code
            if properties != "":
                try:
                    new_properties = {}
                    for k, v in properties.iteritems():
                        print(k)
                        print(v)
                        create_new_log(user_id, "edit properties", "variant", "properties "+str(k), v)
                        new_properties[k] = v
                    variant.properties = new_properties
                except AttributeError as e:
                    return JsonResponse({"success":"false","error":"Properties should be a dictionary"}, status=500)
            #commit
            session.commit()
            return JsonResponse({"Success":"true"}, status=200)
        except ValueError as e:
            session.rollback()
            return JsonResponse({"success":"false", "error":e.message}, status=500)
        except SQLAlchemyError as e:
            session.rollback()
            return JsonResponse({"success":"false", "error":e.message}, status=500)
    else:
        return JsonResponse({"success":"false", "error":"Method is POST"}, status=500)

'''
Takes in 1-4 params and updates item against product_code
'''

@csrf_exempt
def edit_items(request):
    if request.method == 'POST':
        try:
            received_json_data=json.loads(request.body)
            name = received_json_data.get('name','')
            brand = received_json_data.get('brand','')
            category = received_json_data.get('category','')
            product_code = received_json_data.get('product_code','')
            user_id = received_json_data.get('user_id', 'unknown')

            if product_code == "":
                return JsonResponse({"success":"false", "error":"product_code can't be empty"}, status=500)

            item = session.query(Item).filter(Item.product_code == product_code).first()

            if item == None:
                return JsonResponse({"success":"false", "error": "Item not found with id "+str(product_code)}, status=500)

            if name != "":
                create_new_log(user_id, "update name", "items", "name", name)
                item.name = name
            if brand != "":
                create_new_log(user_id, "update brand", "items", "brand", brand)
                item.brand = brand
            if category != "":
                create_new_log(user_id, "update category", "items", "category", category)
                item.category = category

            session.commit();
            return JsonResponse({"Success":"true"}, status=200)
        except ValueError as e:
            session.rollback()
            return JsonResponse({"success":"false", "error":e.message}, status=500)
        except SQLAlchemyError as e:
            session.rollback()
            return JsonResponse({"success":"false", "error":e.message}, status=500)
    else:
        return JsonResponse({"success":"false", "error":"Method is POST"}, status=500)



def create_new_log(user_id, action, table, field, value):
    try:
        row = Logs(user_id=user_id, action=action, table=table, field=field, value=value, date=arrow.utcnow())
        session.add(row)
        session.commit()
        return JsonResponse({"Success":"true"}, status=200)
    except SQLAlchemyError as e:
        session.rollback()
        return JsonResponse({"success":"false","error":e.message}, status=500)
    except ValueError as e:
        session.rollback()
        return JsonResponse({"success":"false", "error":e.message}, status=500)


'''

get all logs for user_id

todo add date range fields

'''
@csrf_exempt
def get_logs(request):
    return_logs = []
    if request.method == 'POST':
        try:
            received_json_data = {}
            if request.body != "":
                received_json_data=json.loads(request.body)
            user_id =  received_json_data.get('user_id','')
            start_time = received_json_data.get('start_time', '')
            end_time = received_json_data.get('end_time', '')

            #parse start date if given
            if start_time == "":
                start_time = arrow.utcnow().shift(weeks=-4) #one month
            else:
                start_time = arrow.get(start_time)

            #parse end date if given
            if end_time == "":
                end_time = arrow.utcnow()
            else:
                end_time = arrow.get(end_time)

            query = ""

            #construct query based on user_id availability
            if user_id == "":
                query = session.query(Logs).filter(Logs.date <= end_time, Logs.date >= start_time) #all
            else:
                query = session.query(Logs).filter(Logs.user_id == user_id, Logs.date <= end_time, Logs.date >= start_time) #user id

            for _row in query.all():
                json_obj = { "user_id": _row.user_id, "action": _row.action, "table": _row.table, "field": _row.field, "value": _row.value, "date": _row.date.to('Asia/Kolkata').format()}
                return_logs.append(json_obj)

            return JsonResponse({"Success":"true", "Logs": return_logs}, status=200)

        except ValueError as e:
            session.rollback()
            return JsonResponse({"success":"false", "error":e.message}, status=500)
    else:
        return JsonResponse({"success":"false", "error":"Method is POST"}, status=500)

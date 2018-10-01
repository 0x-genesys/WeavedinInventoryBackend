from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import PickleType, Text, Date
from sqlalchemy_utils import ArrowType
import json


Base = declarative_base()

class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer,  primary_key=True)
    name =  Column(String)

    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __repr__(self):
        return u"Item(%s, %s)" % (self.name, self.id)

class Branch(Base):
    __tablename__ = 'branches'
    id = Column(Integer,  primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'))
    name =  Column(String)

    def __init__(self, id, store_id, name):
        self.id = id
        self.store_id = store_id
        self.name = name

    def __repr__(self):
        return u"Item(%s, %s, %s)" % (self.id, self.store_id, self.name)

class Item(Base):
    __tablename__ = 'items'
    name = Column(String)
    brand = Column(String)
    category = Column(String)
    product_code = Column(Integer, primary_key=True)
    branch_id = Column(Integer, ForeignKey('branches.id'))

    def __init__(self, name, brand, category, product_code):
        self.name = name
        self.brand = brand
        self.category = category
        self.product_code = product_code

    def __repr__(self):
        return u"Item(%s, %s, %s, %s)" % (self.name, self.brand, self.category, self.product_code)


class Variant(Base):
    __tablename__ = 'variant'
    variant_code = Column(Integer, primary_key=True)
    item_product_code = Column(Integer, ForeignKey('items.product_code'))
    variant_name = Column(String)
    selling_price = Column(Integer)
    cost_price = Column(Integer)
    properties = Column(PickleType(pickler=json))
    quantity = Column(Integer)

    def __init__(self, variant_code, variant_name, selling_price, cost_price, properties, quantity, item_product_code):
        self.variant_code = variant_code
        self.variant_name = variant_name
        self.selling_price = selling_price
        self.cost_price = cost_price
        self.properties = properties
        self.quantity = quantity
        self.item_product_code = item_product_code


    def __repr__(self):
        return u"Variant(%s, %s, %s, %s, %s, %s)" % (self.variant_code, self.variant_name, self.selling_price, self.cost_price, self.properties, self.quantity, self.item_product_code)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    #other details can be put too.  we can put oAUTH /JWT over here

    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __repr__(self):
        return u"Item(%s, %s)" % (self.name, self.id)


class Logs(Base):
    __tablename__= 'logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String)
    table = Column(String)
    field = Column(String)
    value = Column(String)
    date = Column(ArrowType)

    def __init__(self, user_id, action, table, field, value, date):
        self.user_id = user_id
        self.action = action
        self.field = field
        self.table = table
        self.value = value
        self.date = date

    def __repr__(self):
        return u"Item(%s, %s, %s, %s, %s, %s)" % (self.user_id, self.action, self.table, self.field, self.value, self.date)

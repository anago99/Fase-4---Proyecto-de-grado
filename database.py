from mongoengine import *


class Users(Document):
    UserName = StringField()
    Password= StringField()

class Categories(Document):
    Name = StringField()
    Description = StringField()
    Trace=DictField()
class Products(Document):
    Name = StringField()
    Description = StringField()
    Price = FloatField()
    Quantity = IntField()
    Category = ReferenceField(Categories)
    Trace=DictField()

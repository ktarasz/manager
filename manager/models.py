from mongoengine import *
import datetime


class Company(DynamicDocument):
    # <id type="integer">1</id>
    # <name>Globex Corporation</name>
    company_id = IntField(required=True)
    name = StringField(max_length=200, required=True)


class Project(DynamicDocument):
    name = StringField(max_length=200, required=True)
    company_id = ReferenceField(Company)
    date_modified = DateTimeField(default=datetime.datetime.now)


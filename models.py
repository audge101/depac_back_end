from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
import datetime
from flask_login import UserMixin




DATABASE = PostgresqlExtDatabase(
    os.environ.get('DATABASE'), 
    host=os.environ.get('DATABASE_HOST'),
    user=os.environ.get('USER'),
    password=os.environ.get('PASSWORD'),
    port=os.environ.get(PS_PORT))

class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()
    profile_img= CharField()
    class Meta:
        database = DATABASE


class Plant(Model):
    name = CharField(max_length=60)
    locations = CharField()
    description = TextField()
    applications = TextField()
    cultural_importance = TextField()
    misc_uses = TextField()
    plant_img = CharField()
    cultural_img_1 = CharField()
    cultural_img_2 = CharField()
    cultural_img_3 = CharField()
    cultivated = BooleanField(default=False)
    wild = BooleanField(default=False)
    rare = BooleanField(default=False)
    endangered = BooleanField(default=False)
    poisonous = BooleanField(default=False)
    medicinal = BooleanField(default=False)
    psychoactive = BooleanField(default=False)
    anti_aging = BooleanField(default=False)
    superfood = BooleanField(default=False)
    ecological_considerations = TextField()
    resource_link_1 = CharField()
    resource_link_2 = CharField()
    resource_link_3 = CharField()
    owner = ForeignKeyField(User, backref='plants')
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE


class Like(Model):
    user = ForeignKeyField(User, backref="likes")
    post = ForeignKeyField(Plant, backref="likes")
    class Meta:
        database = DATABASE

class Favorite(Model):
    user = ForeignKeyField(User, backref="favorites")
    post = ForeignKeyField(Plant, backref="favorites")
    class Meta:
        database = DATABASE

class Tag(Model):
    user = ForeignKeyField(User, backref="tags")
    post = ForeignKeyField(Plant, backref="tags")
    tag = CharField()
    class Meta:
        database = DATABASE

class Comment(Model):
    user = ForeignKeyField(User, backref="comments")
    post = ForeignKeyField(Plant, backref="comments")
    comment = TextField()
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Plant, Like, Comment,Favorite, Tag], safe=True)
    print("tables created")
    DATABASE.close()
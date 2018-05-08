from peewee import *

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
import datetime

DATABASE = MySQLDatabase('icebergprivateforum3', user='caleb', password='Calebsmom@6', host='localhost')

class User(UserMixin, Model):
    name = CharField(max_length=100)
    role = CharField(max_length=100)
    passcode = CharField(max_length=100)
    
    @classmethod
    def secure_create(cls, **kwargs):
        User.create(name=kwargs.get("name"),
                    role=kwargs.get("role"),
                    passcode=generate_password_hash(kwargs.get("passcode")))
                    
    class Meta:
        database = DATABASE
        
class Post(Model):
    message = TextField(default="")
    posted_by = CharField(max_length=100)
    posted_at = DateTimeField(default=datetime.datetime.now)
    poster_role = CharField(max_length=100)
    
    class Meta:
        database = DATABASE
        
def post_message(msg, posted_by):
    poster_role = User.get(name=posted_by).role
    Post.create(message=msg,
                posted_by=posted_by,
                poster_role=poster_role)
    
def retrieve_messages():
    messages = Post.select()
    amount = len(messages)
    msgs = []
    for i in range(amount, amount-10, -1):
        msgs.append(Post.get(id=i))
    return msgs
             
DATABASE.connect()
DATABASE.create_tables([User, Post], safe=True)
DATABASE.close()
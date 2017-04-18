from sqlalchemy import Boolean
from sqlalchemy import Float
from sqlalchemy import Table, Column, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy_utils import JSONType
from sqlalchemy_utils import EmailType

Base = declarative_base()



class Buy(Base):
    __tablename__ = 'buy'
    buy_id = Column(Integer(), primary_key=True)
    id_user = Column(Integer())
    phone = Column(String(20))
    adress_city = Column(String(60))
    data_time_city = Column(String(40))
    menu = Column(String(60))
    total = Column(Float)
    calendar = Column(Boolean, default=False)
    created_on = Column(DateTime(timezone=True), default=datetime.utcnow)
    temp = Column(String(20))


def __init__(self, buy_id,username,phone,data_city,data_time_city,menu,total,calendar,created_on,temp):
        self.buy_id = buy_id
        self.username = username
        self.phone = phone
        self.data_city = data_city
        self.data_time_city = data_time_city
        self.menu = menu
        self.total = total
        self.calendar = calendar
        self.created_on = created_on
        self.temp = temp


def __repr__(self):
    return "Buy(username='{self.username}', " \
            "phone='{self.phone}', " \
            "city='{self.city}', " \
            "data_city='{self.data_city}', " \
            "data_time_city='{self.data_time_city}', " \
            "calendar='{self.calendar}', " \
            "total='{self.total}', " \
            "temp='{self.temp}', " \
            "menu='{self.menu}')".format(self=self)

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15))
    email_address = Column(EmailType)
    token = Column(JSONType)
    created_on = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_on = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.utcnow)



def __init__(self, user_id, username, email_address, token,created_on, updated_on):
    self.user_id = user_id
    self.username = username
    self.email_address = email_address
    self.token = token
    self.created_on = created_on
    self.updated_on = updated_on


def __repr__(self):
    return "User(username='{self.username}', " \
           "email_address='{self.email_address}', " \
           "token='{self.token}')".format(self=self)

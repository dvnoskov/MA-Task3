from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user_buy import User,Buy
from datetime import datetime
import time
import requests
import config

from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()



TOKEN = config.token
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

engine = create_engine('postgres://biuhgrjrrwwfjg:505787efd3ac0a86bef37d9b63d1b1fc77a335d89dace74486f5dac688d45b1d@ec2-23-21-220-188.compute-1.amazonaws.com:5432/d5r5fmsr87lqpb')
Base = declarative_base()
DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def message(i):
    query = session.query(Buy)
    conv = query.filter(Buy.buy_id == i).one()
    text= 'Reminder about delivery of the order within 1 hour from the restaurant'+conv.menu
    query1 = session.query(User)
    conv1 = query1.filter(User.user_id == conv.id_user).one()
    url = URL + "sendMessage?text={}&chat_id={}".format(text, conv1.chat_id)
    return  get_url(url)


def redir_telegram():
    query = session.query(Buy)
    count = query.filter(bool(Buy.buy_id)).count()
    i = 1
    while i <= count:
        query = session.query(Buy)
        last = query.filter(bool(Buy.buy_id)).count()
        add = query.filter(Buy.buy_id == i).one()
        add_t = add.data_time_city.split('T')  # work
        time = add_t[1].split(':')
        oclok = time[0]
       # current_date = '2017-05-22T11:00:00'  # test
        current_date=datetime.today().isoformat() #work
        curr = current_date.split('T')
        time = curr[1].split(':')
        curr_oclok = time[0]

        if add_t[0] == curr[0]:
            if int(int(oclok) - 4) == int(curr_oclok): # ('-1 hours') #work
                message(i)
                i += 1
        else:     #     ('No data')
            i += 1
            pass
    i += 1

pass


@sched.scheduled_job('interval', minutes=60)
def timed_job():
    redir_telegram()
    pass

sched.start()
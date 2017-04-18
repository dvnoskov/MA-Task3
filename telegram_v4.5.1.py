#coding:utf-8
from oauth2client.client import flow_from_clientsecrets, Credentials
import oauth2client
import re
from sqlalchemy import null
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.user_buy import User,Buy
import logging
import config
from flask import Flask, request,redirect
import telebot
import os



server = Flask(__name__)

engine = create_engine('sqlite:///SQLAlchemy_telegram_v4.5.1.db')

Base = declarative_base()

DBSession = sessionmaker(bind=engine)
session = DBSession()


bot = telebot.TeleBot(config.token)


#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    markup.row(text(3))
    markup.row(text(4), text(5))
    bot.send_message(message.chat.id,'start',reply_markup=markup)
    pass

# message menu
@bot.message_handler(regexp='Выбор меню обеда')
def handle_message(message):
    menu(message)
    pass


@bot.message_handler(regexp='Choosing a lunch menu')
def handle_message(message):
    menu(message)
    pass


def menu(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button = types.InlineKeyboardButton(text=text(9), callback_data=text(9))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=text(10), callback_data=text(10))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=text(11), callback_data=text(11))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=text(12), callback_data='Callback')
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, text(13), reply_markup=keyboard)
    pass

# message languange
@bot.message_handler(regexp='Выбор языка интерфейса')
def handle_message(message):
    languange(message)
    pass


@bot.message_handler(regexp='Selecting the interface language')
def handle_message(message):
    languange(message)
    pass


def languange(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    callback_button = types.InlineKeyboardButton(text=text(6), callback_data='Rus')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=text(7), callback_data='England')
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, text(8), reply_markup=keyboard)
    pass

# message restoran
@bot.message_handler(regexp='Добро пожаловать в ресторан рога и копыта')
def handle_message(message):
    restoran(message)
    pass


@bot.message_handler(regexp='Welcome to the restaurant of horns and hooves')
def handle_message(message):
    restoran(message)
    pass


def restoran(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button = types.InlineKeyboardButton(text=text(14), callback_data='Callback')
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, text(15), reply_markup=keyboard)
    pass

# end restoran

def menu_start_buy(message, start_text):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button = types.InlineKeyboardButton(text=text(16), callback_data='buy_start')
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, start_text, reply_markup=keyboard)
    if 0 == session.query(User).filter(User.username == message.chat.first_name).count():
        add9 = User(username=message.chat.first_name)
        session.add(add9)
        session.commit()
    pass

# call_back message
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == text(9):
            menu_start_buy(call.message,text(9))
            pass
        elif call.data == text(10):
            menu_start_buy(call.message,text(10))
            pass
        elif call.data == text(11):
            menu_start_buy(call.message,text(11))
            pass
        elif call.data == 'Rus':
            a = '1'
            lang(a,call.message)
            pass
        elif call.data == 'England':
            a = '0'
            lang(a, call.message)
            pass
        elif call.data =='Callback':
            send_welcome(call.message)
            pass
        elif call.data =='buy_start':
            add2 = call.message.text
            menu = session.query(User).filter(User.username == call.message.chat.first_name).first()
            session.add(Buy(id_user=menu.user_id, menu=add2))
            session.commit()
            bot.send_message(call.message.chat.id, text=text(17))
            if add2 == text(11): # error
                tot = 18
                total={Buy.total: tot}
                update_buy(total)
                pass

            elif add2 == text(10):
                tot = 22
                total = {Buy.total: tot}
                update_buy(total)
                pass

            elif add2 == text(9):
                tot = 26
                total = {Buy.total: tot}
                update_buy(total)
                pass

        pass

    pass


# message text
def text(i):
   f = open('text.txt', encoding='utf8')
   line = f.readlines()
 #  i=0
   if line[0] == line[1]:
       i=i-1
       pass
   else:
       i=i+26
   return line[i]


# message buy no buy
def handle_message_finish(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    markup.row('Yes-buy', 'No-buy')
    bot.send_message(message.chat.id, text =text(18),reply_markup=markup)
    pass

# message
@bot.message_handler(func=lambda message: message.text == message.text
                                         and message.content_type =='text')
def echoall(message):

    if bool('0') == bool(re.match(r'[0]{1}[0-9]{9}', message.text) and len(message.text) == 10):
        bot.send_message(message.chat.id, text=text(19))
        add4 = message.text
        phone={Buy.phone: add4}
        update_buy(phone)
        pass
    elif bool('@gmail.com') == bool(re.compile(r'@gmail.com', re.I | re.VERBOSE).search(message.text)):
        add3 = message.text
        query = session.query(User)
        query = query.filter(User.username == message.chat.first_name)
        query.update({User.email_address: add3})
        session.commit()
        query = session.query(User)
        last = query.filter(bool(User.user_id)).count()
        tok = query.filter(User.user_id == last).one()
     #   add_d = message.chat.first_name #test
     #   temp = {Buy.temp: add_d}       #
     #   update_buy(temp)
     #   oauth2()                      #test
        if None == tok.token: #  cr token
            add_d = message.chat.first_name
            temp = {Buy.temp: add_d}
            update_buy(temp)
            oauth2()
        else:
            send_welcome(message)
            pass
    elif bool('Cherkassy') == bool(re.match(r'Cherkassy', message.text)):
        bot.send_message(message.chat.id, text=text(20))
        add_d = message.text
        adres={Buy.adress_city: add_d}
        update_buy(adres)
        pass
    elif bool('2017') == bool(re.findall(r'\d{2}-\d{2}-(2017)', message.text)):
        bot.send_message(message.chat.id, text=text(21))
        add_d = message.text
        temp={Buy.temp: add_d}
        update_buy(temp)
        pass
    elif bool('11' or '12'or '13'or '14') == bool(re.findall(r'(11|12|13|14)-\d{2}',message.text)):
        query = session.query(Buy)
        last = query.filter(bool(Buy.buy_id)).count()
        add = query.filter(Buy.buy_id == last).one()
        add_d = add.temp
        add_t =  message.text
        add6 = ''.join(add_d.split('-')[2] + '-' + add_d.split('-')[1] + \
                       '-' + add_d.split('-')[0] + 'T' + add_t.replace('-',':') + ':00')
        time={Buy.data_time_city: add6}
        update_buy(time)
        handle_message_finish(message)
        pass
    elif message.text=='Yes-buy':
        bot.send_message(message.chat.id, text=text(22))
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.row('Calendar', 'No')
        bot.send_message(message.chat.id, text=text(23),reply_markup=markup)
        pass
    elif message.text == 'No':
        send_welcome(message)
        pass
    elif message.text == 'No-buy':
        bot.send_message(message.chat.id, text=text(24))
        query = session.query(Buy)
        last = query.filter(bool(Buy.buy_id)).count()
        query = query.filter(Buy.buy_id == last)
        last_del = query.one()
        session.delete(last_del)
        session.commit()
        send_welcome(message)
        pass
    elif message.text == 'Calendar':
        true={Buy.calendar: True}
        update_buy(true)
        bot.send_message(message.chat.id, text=text(25))
        pass
    elif message.text != ('Calendar' and 'No-buy' and 'No' and 'Yes-buy'\
                                  and (bool(re.findall(r'(11|12|13|14)-\d{2}', message.text)))\
                                  and (bool(re.findall(r'\d{2}-\d{2}-(2017)', message.text))) \
                                  and (bool(re.match(r'Cherkassy', message.text))) \
                                  and (bool(re.compile(r'@gmail.com', re.I | re.VERBOSE).search(message.text))) \
                                  and (bool(re.match(r'[0]{1}[0-9]{9}', message.text) and len(message.text) == 10))):
        bot.send_message(message.chat.id, text=text(26))
        pass

# bd_buy update
def update_buy(input):
    query = session.query(Buy)
    last = query.filter(bool(Buy.buy_id)).count()
    query = query.filter(Buy.buy_id == last)
    query.update(input)
    session.commit()
    pass

# languang
def lang(a,message):
    file = open('text.txt', 'r+')
    file.write(str(a))
    file.close()
    send_welcome(message)
    pass

# tokin google
scope = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/calendar'
flow = oauth2client.client.flow_from_clientsecrets('client_secret.json',
                                                       scope=scope,
                                                       redirect_uri='http://127.0.0.1:5000/oauth2callback')
flow.params['access_type'] = 'offline'



@server.route('/start')
def  oauth2():
    auth_url = flow.step1_get_authorize_url()
    return redirect(auth_url)

@server.route('/oauth2callback', methods=['GET'])
def get_credentials():
    credentials = flow.step2_exchange(request.args.get('code'))
    json_credentials = Credentials.to_json(credentials)
    query = session.query(Buy)
    last = query.filter(bool(Buy.buy_id)).count()
    add = query.filter(Buy.buy_id == last).one()
    user = add.temp
    query = session.query(User)
    query = query.filter(User.username == user)
    query.update({User.token: json_credentials})
    session.commit()
    send_welcome()
    return "Ok", 200



# route webhook
@server.route('/' + config.token, methods=['POST'])
#@server.route('/bot' + config.token, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "POST", 200

@server.route("/")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url='https://8938cd52.ngrok.io/' + config.token) #ngrok adress
    return "CONNECTED", 200

port = int(os.environ.get("PORT", 5000))
#port = int(os.environ.get("PORT", 8443))
if __name__ == "__main__":
     #server.run()
     server.run(host='127.0.0.1', port=port)


#server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
#WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')



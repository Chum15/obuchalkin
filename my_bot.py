import random
from sqlalchemy import func

from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
import load



print('Start telegram bot...')

state_storage = StateMemoryStorage()
token_bot = ''
bot = TeleBot(token_bot, state_storage=state_storage)

known_users = []
userStep = {}
buttons = []


def show_hint(*lines):
    return '\n'.join(lines)


def show_target(data):
    return f"{data['target_word']} -> {data['translate_word']}"


class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'


class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        known_users.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0
    
user = "" 
ide = 0
@bot.message_handler(commands=['cards', 'start'])
def create_cards(message):
    global cid
    cid = message.chat.id
    if cid not in known_users:
        known_users.append(cid)
        userStep[cid] = 0
        bot.send_message(cid, "Hello, stranger, let study English...")
    markup = types.ReplyKeyboardMarkup(row_width=2)
   
    global buttons
    buttons = []
    global ide
    global target_word
    global translate
    
    ide += 1
    target_w = str(load.session.query(load.English.target_word).filter(load.English.id_e ==ide).all())[3:]
    target_word = target_w[:-4]  # брать из БД
    transl = str(load.session.query(load.Russish.translate).filter(load.Russish.id_en ==ide).all())[3:] 
    translate = transl[:-4] # брать из БД
    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)
    other =str(load.session.query(load.English.target_word).order_by(func.random()).limit(1).all())[3:]
    other = other[:-4]
    othe =str(load.session.query(load.English.target_word).order_by(func.random()).limit(1).all())[3:]
    othe = othe[:-4]
    oth =str(load.session.query(load.English.target_word).order_by(func.random()).limit(1).all())[3:]
    oth = oth[:-4]
    ot =str(load.session.query(load.English.target_word).order_by(func.random()).limit(1).all())[3:]
    ot = ot[:-4]
    others = [other, othe, oth, ot]  # брать из БД
    other_words_btns = [types.KeyboardButton(word) for word in others]
    buttons.extend(other_words_btns)
    random.shuffle(buttons)
    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*buttons)

    greeting = f"Выбери перевод слова:\n🇷🇺 {translate}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = translate
        data['other_words'] = others

    
    global user 
    user = message.from_user.id
   
 
@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    
    create_cards(message)
     

@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        print(data['target_word'])  # удалить из БД
        d = load.session.query(load.User).filter(load.User.en_word == target_word).one()
    
        load.session.delete(d)
        load.session.commit()
    

@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    cid = message.chat.id

    load.session.add(load.User(en_word = target_word, ru_word = translate))
    load.session.commit() 

    userStep[cid] = 1
    print(message.text)  # сохранить в БД


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    text = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['target_word']
        if text == target_word:
           
            hint = show_target(data)
            hint_text = ["Отлично!❤", hint]
            next_btn = types.KeyboardButton(Command.NEXT)
            add_word_btn = types.KeyboardButton(Command.ADD_WORD)
            delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
            buttons.extend([next_btn, add_word_btn, delete_word_btn])
            hint = show_hint(*hint_text)
           
        else:
            for btn in buttons:
                if btn.text == text:
                    btn.text = text + '❌'
                    break
            hint = show_hint("Допущена ошибка!",
                             f"Попробуй ещё раз вспомнить слово 🇷🇺{data['translate_word']}")
       
    markup.add(*buttons)
    bot.send_message(message.chat.id, hint, reply_markup=markup)




if __name__ == '__main__':
    load.create_tables(load.engine) 
    load.open_file()  
    


bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.infinity_polling(skip_pending=True)
import random

from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
import settings
import sel




print('Start telegram bot...')

state_storage = StateMemoryStorage()

bot = TeleBot(settings.token_bot, state_storage=state_storage)

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
    word = sel.word()

    target_word = word[0]  # брать из БД
    translate = word[1] # брать из БД
    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)
    other = word[2]
    othe = word[3]
    oth = word[4]
    ot = word[5]
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
    sel.session.add(sel.User(en_word = sel.target_word, ru_word = sel.translate, user_id = cid ))
    sel.session.commit()
 
 
@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message): 
    create_cards(message)
    

@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
          # удалить из БД
        b = bot.send_message(cid,'введите удаляемое английское слово:')
        bot.register_next_step_handler(b, dell)
        print(data['target_word'])

def dell(message):
    delit = message.text
    dellit = delit.lower()
    cid =  message.chat.id 
    d = sel.session.query(sel.User).filter(sel.User.en_word == dellit, sel.User.user_id == str(cid)).one()
    
    sel.session.delete(d)
    sel.session.commit()
    
    
@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    cid = message.chat.id
   
    a = bot.send_message(cid,'Введите английское слово и его перевод: ')
    bot.register_next_step_handler(a, word)


def word(message):
    
    words = message.text
    words_en = words.split()[0]
    words_ru = words.split()[1]

    sel.session.add(sel.User(en_word = words_en, ru_word = words_ru, user_id = cid))
    sel.session.commit()

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
    sel.create_tables 
    sel.open_file  
    
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling(skip_pending=True)
from sqlalchemy import func
import load



    
create_tables = load.create_tables(load.engine)
open_file = load.open_file()

def word():

    global target_word
    global translate
    # target_word =''
    # translate = ''
    transl = str(load.session.query(load.Russish.translate).order_by(func.random()).limit(1).all())[3:]
    translate = transl[:-4] # брать из БД
    target_w = str(load.session.query(load.English.target_word).\
                join(load.Russish, load.Russish.id_en == load.English.id_e).
                filter(load.Russish.translate == translate).all())[3:]
    target_word = target_w[:-4]  # брать из БД

    other =str(load.session.query(load.English.target_word).order_by(func.random()).limit(1).all())[3:]
    other = other[:-4]
    othe =str(load.session.query(load.English.target_word).order_by(func.random()).limit(1).all())[3:]
    othe = othe[:-4]
    oth =str(load.session.query(load.English.target_word).order_by(func.random()).limit(1).all())[3:]
    oth = oth[:-4]
    ot =str(load.session.query(load.English.target_word).order_by(func.random()).limit(1).all())[3:]
    ot = ot[:-4]

    return target_word, translate, other, othe, oth, ot

    

def del_word():
    
    d = load.session.query(load.User).filter(load.User.en_word == target_word).one()
    
    load.session.delete(d)
    load.session.commit()



def add_word():

    load.session.add(load.User(en_word = target_word, ru_word = translate))
    load.session.commit() 



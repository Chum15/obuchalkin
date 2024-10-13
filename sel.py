from sqlalchemy import func
import load


    
create_tables = load.create_tables(load.engine)
open_file = load.open_file()
session = load.session
User = load.User

def word():

    global target_word
    global translate
   
    transl = str(load.session.query(load.Russish.translate).order_by(func.random()).limit(1).all())[3:]
    translate = transl[:-4] 
    target_w = str(load.session.query(load.English.target_word).\
                join(load.Russish, load.Russish.id_en == load.English.id_e).
                filter(load.Russish.translate == translate).all())[3:]
    target_word = target_w[:-4] 

    other =str(load.session.query(load.English.target_word).order_by(func.random()).limit(1).all())[3:]
    other = other[:-4]
    othe =str(load.session.query(load.English.target_word).order_by(func.random()).limit(1).all())[3:]
    othe = othe[:-4]
    oth =str(load.session.query(load.English.target_word).order_by(func.random()).limit(1).all())[3:]
    oth = oth[:-4]
    ot =str(load.session.query(load.English.target_word).order_by(func.random()).limit(1).all())[3:]
    ot = ot[:-4]

    return target_word, translate, other, othe, oth, ot


import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
import settings
import modules 



English = modules.English
Russish = modules.Russish
User = modules.User

DSN = f'{settings.database}://{settings.login}:{settings.password}@{settings.host}/{settings.base}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

def open_file():
    with open('words.json', 'r', encoding="utf-8") as fd:
        data = json.load(fd)

    for record in data:
      session.add(English(target_word = record.get('en')))
      session.add(Russish(translate = record.get('ru'), id_en = record.get('id')))
       
    session.commit()



def create_tables(engine):
    modules.Base.metadata.drop_all(engine)
    modules.Base.metadata.create_all(engine)

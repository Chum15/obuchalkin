import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship



Base = declarative_base()
class English(Base):

    __tablename__ = 'eng'

    id_e = sq.Column(sq.Integer, primary_key=True)
    target_word = sq.Column(sq.String(length=100), nullable=False)

    def __str__(self):
        return f'{self.id} {self.target_word}'
    


class Russish(Base):

    __tablename__ = 'rus'

    id_r =  sq.Column(sq.Integer, primary_key=True)
    translate = sq.Column(sq.String(length = 100), nullable=False)
    id_en = sq.Column(sq.Integer, sq.ForeignKey(English.id_e), nullable=False)

    eng = relationship(English, backref='rus')


    def __str__(self):
        return f'{self.translate}'
    


class User(Base):
    
    __tablename__ = 'user'

    id_word = sq.Column(sq.Integer, primary_key=True)
    en_word = sq.Column(sq.String(length=100), nullable=False)
    ru_word = sq.Column(sq.String(length = 100), nullable=False)
    user_id = sq.Column(sq.String(length=30), nullable=False)

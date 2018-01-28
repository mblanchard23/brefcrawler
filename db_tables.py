import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

db_uri = os.environ.get('BREF_DB_URI')
engine = create_engine(db_uri, echo=True)
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    fullname = Column(String(128))
    password = Column(String(128))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


class Players(Base):
    __tablename__ = 'players'
    id = Column(String(16), primary_key=True)
    player_name = Column(String(128), nullable=False)
    year_from = Column(Integer, nullable=False)
    year_to = Column(Integer, nullable=False)
    position = Column(String(8), nullable=False)
    height = Column(String(8), nullable=False)
    weight = Column(Integer, nullable=False)
    birth_date = Column(Date, nullable=True)
    college = Column(String(256), nullable=True)
    hall_of_fame = Column(Boolean, nullable=False)

    def __repr__(self):
        return '{player_name}'.format(player_name=self.player_name)

# DOB Transformation



def insert_players(session,lst):
    ''' Inserts a lst of player dicts'''
    for player in lst:
        try:
            p = Players(**player)
            session.add(p)
            session.commit()
        except:
            print('%s already exists, skipping' % p.player_name)
            session.rollback()
            continue

    return None

def insert_all_players_to_db():
    from get_players import get_players_dataframe
    letters_of_alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for letter in letters_of_alphabet:
        try:
            df = get_players_dataframe(letter)
            insert_players(session,df.to_dict(orient='records'))
           
        except:
            print('Letter not found: %s' % letter)



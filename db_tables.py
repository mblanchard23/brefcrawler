import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, Date, Boolean, ForeignKey, UniqueConstraint, Float
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

class Player_Season_Totals(Base):
    __tablename__ = 'player_season_totals'
    id = Column(String(64),primary_key=True,nullable=False)
    player_id = Column(String(16),ForeignKey('players.id'),nullable=False)
    season = Column(String(8),nullable=True)
    age = Column(Integer,nullable=True)
    team = Column(String(8),nullable=True)
    league = Column(String(8),nullable=True)
    position = Column(String(8),nullable=True)
    games_played = Column(Integer,nullable=True)
    games_started = Column(Integer,nullable=True)
    minutes_played = Column(Integer,nullable=True)
    field_goals = Column(Integer,nullable=True)
    field_goals_attempted = Column(Integer,nullable=True)
    field_goal_percentage = Column(Float,nullable=True)
    three_point_fg_made = Column(Integer,nullable=True)
    three_point_fg_attempted = Column(Integer,nullable=True)
    three_point_percentage = Column(Float,nullable=True)
    two_point_fg_made = Column(Integer,nullable=True)
    two_point_fg_attempted = Column(Integer,nullable=True)
    two_point_fg_percentage = Column(Float,nullable=True)
    effective_fg_percentage = Column(Float,nullable=True)
    ft_made = Column(Integer,nullable=True)
    ft_attempted = Column(Integer,nullable=True)
    ft_percentage = Column(Integer,nullable=True)
    offensive_rebounds = Column(Integer,nullable=True)
    defensive_rebounds = Column(Integer,nullable=True)
    total_rebounds = Column(Integer,nullable=True)
    assists = Column(Integer,nullable=True)
    steals = Column(Integer,nullable=True)
    blocks = Column(Integer,nullable=True)
    turnovers = Column(Integer,nullable=True)
    personal_fouls = Column(Integer,nullable=True)
    points = Column(Integer,nullable=True)


    def __repr__(self):
            return '%s - %s' % (self.player_id, self.season)



class Player_Gamelog_Totals(Base):
    __tablename__ = 'player_gamelog'
    id = Column(String(64),primary_key=True,nullable=False)
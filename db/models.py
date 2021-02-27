from sqlalchemy.engine import base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from db.db import Base

class player_season():
    id = Column(Integer, primary_key=True)
    td = Column(Integer)
    name = Column(String(50))
    year = Column(Integer)
    years_played = Column(Integer)

class qb(Base, player_season):
    __tablename__ = 'qb'

    position = Column(String)
    completions = Column(Integer)
    attempts = Column(Integer)
    completion_pct = Column(Float)
    yards_passed = Column(Integer)
    interceptions = Column(Integer)
    avg_yards_per_pass = Column(Float)

class te(Base, player_season):
    __tablename__ = 'te'

class wr(Base, player_season):
    __tablename__ = 'wr'
    targets = 0
    receptions = 0
    yardsReceived = 0

class rb(Base, player_season):
    __tablename__ = 'rb'
    rushes = Column(Integer)
    yardsRushed = Column(Float)
    avgYardsPerRush = Column(Float)
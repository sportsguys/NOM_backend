from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy.orm import relationship
from db.db import Base

class player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    url = Column(String(200))
    position = Column(String(10))

class season(): # not a table
    id = Column(Integer, primary_key=True)
    td = Column(Integer)
    year = Column(Integer)    
    games = Column(Integer)

    """
    @declared_attr
    def player_name(cls):
        return Column(String(50), ForeignKey(player.name))
    @declared_attr
    def player_relationship(cls):
        return relationship('player')
    """

class qb(Base, season):
    __tablename__ = 'qb'
    completions = Column(Integer)
    attempts = Column(Integer)
    completion_pct = Column(Float)
    yards_passed = Column(Integer)
    interceptions = Column(Integer)
    avg_yards_per_pass = Column(Float)

class wr(Base, season):
    __tablename__ = 'wr'
    targets = Column(Integer)
    receptions = Column(Integer)
    yardsReceived = Column(Integer)

class rb(Base, season):
    __tablename__ = 'rb'
    rushes = Column(Integer)
    yardsRushed = Column(Float)
    avgYardsPerRush = Column(Float)
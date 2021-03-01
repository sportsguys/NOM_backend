from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy.orm import relationship
from db.db import Base

class player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    url = Column(String(200), unique=True)
    position = Column(String(10))

class season(): # not a table
    id = Column(Integer, primary_key=True)
    year_id = Column(Integer)    
    g = Column(Integer) #games
    gs = Column(Integer) #games started
    age = Column(Integer)
    team = Column(String(5))

    @declared_attr
    def player_id(cls):
        return Column(Integer, ForeignKey(player.id))
    @declared_attr
    def player_relationship(cls):
        return relationship('player')

class qb(Base, season):
    __tablename__ = 'qb'
    pass_att = Column(Integer)
    pass_cmp = Column(Integer)
    pass_cmp_perc = Column(Integer)
    pass_yds = Column(Integer)
    pass_td = Column(Integer)
    pass_td_perc = Column(Float)
    pass_int = Column(Integer)
    pass_int_perc = Column(Float)
    pass_first_down = Column(Integer)
    pass_long = Column(Integer)
    pass_yds_per_att = Column(Float)
    pass_adj_yds_per_att = Column(Float)
    pass_sacked = Column(Integer)
    pass_sacked_yds = Column(Integer)
    pass_net_yds_per_att = Column(Float)
    gwd = Column(Integer)

class receiver():
    targets = Column(Integer)
    rec = Column(Integer)
    rec_yds = Column(Integer)
    rec_yds_per_rec = Column(Float)
    rec_td = Column(Integer)
    rec_first_down = Column(Integer)
    rec_long = Column(Integer)
    rec_per_g = Column(Float)
    rec_yds_per_g = Column(Float)
    rec_yds_per_tgt = Column(Float)

class wr(Base, season, receiver):
    __tablename__ = 'wr'
    
class rb(Base, season, receiver):
    __tablename__ = 'rb'
    rush_att  = Column(Integer)
    rush_yds = Column(Integer)
    rush_td  = Column(Integer)
    rush_first_down  = Column(Integer)
    rush_long  = Column(Integer)
    rush_yds_per_att  = Column(Float)
    rush_yds_per_g = Column(Float)
    rush_att_per_g = Column(Float)

class defense(Base, season):
    __tablename__ = 'defense'
    def_int = Column(Integer)
    def_int_yds = Column(Integer)
    def_int_td = Column(Integer)
    def_int_long = Column(Integer)
    pass_defended = Column(Integer)
    fumbles_forced = Column(Integer)
    fumbles = Column(Integer)
    fumbles_rec = Column(Integer)
    fumbles_rec_yds = Column(Integer)
    fumbles_rec_td = Column(Integer)
    sacks = Column(Integer)
    tackles_combined = Column(Integer)
    tackles_solo = Column(Integer)
    tackles_loss = Column(Integer)
    qb_hits = Column(Integer)
    safety_mb = Column(Integer)

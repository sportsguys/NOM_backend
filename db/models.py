from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declared_attr
from db.db import Base

class player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    url = Column(String(100), unique=True)
    position = Column(String(10))

class team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String(50))
    url = Column(String(10), unique=True) # 3 character PFR-specific abbreviation for url

class team_season(Base):
    __tablename__ = 'team_season'
    id = Column(Integer, primary_key=True, autoincrement=True)
    year_id = Column(Integer, primary_key=True)
    wins = Column(Integer)
    losses = Column(Integer)
    ties = Column(Integer)
    points = Column(Integer)
    points_opp = Column(Integer)
    mov = Column(Float)

    @declared_attr
    def team_url(cls):
        return Column(String(10), ForeignKey(team.url))
    @declared_attr
    def team_relationship(cls):
        return relationship('team')

class player_season(Base): #  a table
    __tablename__ = 'player_season'
    id = Column(Integer, primary_key=True)
    year_id = Column(Integer)    
    g = Column(Integer) #games
    gs = Column(Integer) #games started
    age = Column(Integer)
    team = Column(String(5))
    av = Column(Float)

    @declared_attr
    def player_id(cls):
        return Column(Integer, ForeignKey(player.id))
    @declared_attr
    def player_relationship(cls):
        return relationship('player')

    @declared_attr
    def team_season_id(cls):
        return Column(Integer, ForeignKey(team_season.id))
    @declared_attr
    def team_season_relationship(cls):
        return relationship('team_season')

class position():
    id = Column(Integer, primary_key=True, autoincrement=True)
    av = Column(Float)


    @declared_attr
    def player_season_id(cls):
        return Column(Integer, ForeignKey(player_season.id))
    @declared_attr
    def player_season_relationship(cls):
        return relationship('player_season')

    @declared_attr
    def player_id(cls):
        return Column(Integer, ForeignKey(player.id))
    @declared_attr
    def player_relationship(cls):
        return relationship('player')

    @declared_attr
    def team_season_id(cls):
        return Column(Integer, ForeignKey(team_season.id))
    @declared_attr
    def team_season_relationship(cls):
        return relationship('team_season')

class qb(Base, position):
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

class wr(Base, position, receiver):
    __tablename__ = 'wr'
    
class rb(Base, position, receiver):
    __tablename__ = 'rb'
    rush_att  = Column(Integer)
    rush_yds = Column(Integer)
    rush_td  = Column(Integer)
    rush_first_down  = Column(Integer)
    rush_long  = Column(Integer)
    rush_yds_per_att  = Column(Float)
    rush_yds_per_g = Column(Float)
    rush_att_per_g = Column(Float)

class defense(Base, position):
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


class kicker(Base, position):
    __tablename__ = 'kicker'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fga1 = Column(Integer)
    fgm1 = Column(Integer)
    fga2 = Column(Integer)
    fgm2 = Column(Integer)
    fga3 = Column(Integer)
    fgm3 = Column(Integer)
    fga4 = Column(Integer)
    fgm4 = Column(Integer)
    fga5 = Column(Integer)
    fgm5 = Column(Integer)
    fga = Column(Integer)
    fgm = Column(Integer)
    fg_long = Column(Float)
    fg_perc = Column(Float)
    xpa = Column(Integer)
    xpm = Column(Integer)
    xp_perc = Column(Float)
    kickoff = Column(Integer)
    kickoff_yds = Column(Integer)
    kickoff_tb = Column(Integer)
    kickoff_tb_pct = Column(Float)
    kickoff_yds_avg = Column(Float)
    punt = Column(Integer)
    punt_yds = Column(Integer)
    punt_long = Column(Integer)
    punt_blocked = Column(Integer)
    punt_yds_per_punt = Column(Float)

class salary(Base):
    __tablename__ = 'salary'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    salary = Column(Integer)
    year = Column(Integer)
    team = Column(String(50))
    av = Column(Integer)
    
    @declared_attr
    def player_url(cls):
        return Column(String(100), ForeignKey(player.url))
    @declared_attr
    def player_relationship(cls):
        return relationship('player')

class cap_hit(Base):
    __tablename__ = 'cap_hits'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    position = Column(String(10))
    hit = Column(Float)
    
    @declared_attr
    def player_season_id(cls):
        return Column(Integer, ForeignKey(player_season.id))
    @declared_attr
    def player_season_relationship(cls):
        return relationship('player_season')

    @declared_attr
    def team_season_id(cls):
        return Column(Integer, ForeignKey(team_season.id))
    @declared_attr
    def team_season_relationship(cls):
        return relationship('team_season')

class score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float)
    

    @declared_attr
    def player_season_id(cls):
        return Column(Integer, ForeignKey(player_season.id))
    @declared_attr
    def player_season_relationship(cls):
        return relationship('player_season')

    @declared_attr
    def player_id(cls):
        return Column(Integer, ForeignKey(player.id))
    @declared_attr
    def player_relationship(cls):
        return relationship('player')
        
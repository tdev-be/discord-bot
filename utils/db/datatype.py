from pony.orm import *
from datetime import datetime, time
import config
db=Database()
sql_debug(config.sql_debug)

class Played_game(db.Entity):
    id = PrimaryKey(int, auto=True)
    server = Required(str)
    user = Required(str)
    game = Required(str)
    date_from = Required(datetime)
    date_to = Optional(datetime)
    time = Optional(float)

class Afk(db.Entity):
    id = PrimaryKey(int, auto=True)
    server = Required(str)
    user = Required(str)
    reason = Optional(str)

@db_session
def afk_reason( server, user, message="Afk"):
    Afk(server=server,user=user, reason=message)
    commit()


class played_game_repository():
    @db_session
    def save(self):
        commit()

    @db_session
    def read(self):
        return Played_game.select()

db.bind(provider='sqlite', filename='database.db', create_db=True)
db.generate_mapping(create_tables=True)

@db_session
def log_game(server: str, user:str,game:str,date_from:datetime):
    Played_game(server=server,user=user, game=game, date_from=date_from)
    commit()
@db_session
def log_end_game(server: str, user:str,game:str,date_to:datetime):
    played = select((p) for p in Played_game if server == p.server and user == user and game == game and p.date_to is None).first()
    played.date_to = date_to
    print((played.date_to - played.date_from).total_seconds())
    played.time = (played.date_to - played.date_from).total_seconds()
    commit()

@db_session
def stats_per_game(server: str, ctx):
    games = select ((p.game, count(p), sum(p.time)) for p in Played_game if server == p.server).order_by(-2)
    list=[]
    for game in games:
        list.append(game)
    return list

@db_session
def stats_per_user(server: str, ctx):
    games = select ((p.user,p.game, count(p), sum(p.time)) for p in Played_game if server == p.server).order_by(-3,-1)
    list=[]
    for game in games:
        list.append(game)
    return list
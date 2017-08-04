from pony.orm import *
from datetime import datetime
db=Database()
sql_debug(False)

class Played_game(db.Entity):
    id = PrimaryKey(int, auto=True)
    server = Required(str)
    user = Required(str)
    game = Required(str)
    date_from = Required(datetime)

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
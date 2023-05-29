import database.db as db

from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import reconstructor

from datetime import datetime, timedelta

class UserDB(db.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(45))
    user_type = Column(String(45))

    def __init__(self, user_name, user_type):
        self.user_name = user_name
        self.user_type = user_type

    def __repr__(self):
        return f'User({self.user_name}, {self.user_type})'

    def __str__(self):
        return f'User({self.user_name}, {self.user_type})'

class ActorDB(db.Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    actor_name = Column(String(45))
    actor_type = Column(String(45))

    def __init__(self, actor_name, actor_type):
        self.actor_name = actor_name
        self.actor_type = actor_type

    def __repr__(self):
        return f'User({self.actor_name}, {self.actor_type})'

    def __str__(self):
        return f'User({self.actor_name}, {self.actor_type})'

class InteractEventDB(db.Base):
    __tablename__ = 'interact_events'

    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    scenary_type = Column(String(45))
    event_type = Column(String(45))
    event_datetime = Column(Integer)

    def __init__(self, actor_id, user_id, event_type, event_datetime):
        self.actor_id = actor_id
        self.user_id = user_id
        self.event_type = event_type
        self.event_datetime = event_datetime

    @reconstructor
    def init_db_load(self):
        self.event_datetime = int(datetime.strptime(self.event_datetime, '%Y-%m-%d %H:%M:%S').timestamp())

    def __repr__(self):
        return f'InteractEvent({self.actor_id}, {self.user_id}, {self.scenary_type}, {self.event_type}, {self.event_datetime})'

    def __str__(self):
        return f'InteractEvent({self.actor_id}, {self.user_id}, {self.scenary_type}, {self.event_type}, {self.event_datetime})'

    def as_dict(self):
        return {"user_id": self.user_id, "event_type": self.event_type, "event_datetime": self.event_datetime}

    def get_real_time(self):
        return datetime.fromtimestamp(int(self.event_datetime)).strftime("%Y-%m-%d %H:%M:%S")

class GameplayEventDB(db.Base):
    __tablename__ = 'gameplay_events'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scenary_type = Column(String(45))
    event_type = Column(String(45))
    event_datetime = Column(Integer)

    def __init__(self, user_id, event_type, event_datetime):
        self.user_id = user_id
        self.event_type = event_type
        self.event_datetime = event_datetime

    @reconstructor
    def init_db_load(self):
        self.event_datetime = int(datetime.strptime(self.event_datetime, '%Y-%m-%d %H:%M:%S').timestamp())

    def __repr__(self):
        return f'GameplayEvent({self.user_id}, {self.scenary_type}, {self.event_type}, {self.event_datetime})'

    def __str__(self):
        return f'GameplayEvent({self.user_id}, {self.scenary_type}, {self.event_type}, {self.event_datetime})'

    def as_dict(self):
        return {"user_id": self.user_id, "event_type": self.event_type, "event_datetime": self.event_datetime}

    def get_real_time(self):
        return datetime.fromtimestamp(int(self.event_datetime)).strftime("%Y-%m-%d %H:%M:%S")

    
class MoveEventDB(db.Base):
    __tablename__ = 'move_events'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scenary_type = Column(String(45))
    start_datetime = Column(Integer)
    end_datetime = Column(Integer)
    start_position = Column(String(45))
    end_position = Column(String(45))
    distance = Column(Integer)

    def __init__(self, user_id, start_datetime, end_datetime, start_position, end_position, distance):
        self.user_id = user_id
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.start_position = start_position
        self.end_position = end_position
        self.distance = distance

    @reconstructor
    def init_db_load(self):
        self.start_datetime = int(datetime.strptime(self.start_datetime, '%Y-%m-%d %H:%M:%S').timestamp())
        self.end_datetime = int(datetime.strptime(self.end_datetime, '%Y-%m-%d %H:%M:%S').timestamp())

    def __repr__(self):
        return f'MoveEvent({self.user_id}, {self.scenary_type}, {self.start_datetime}, {self.end_datetime}, \
        {self.start_position}, {self.end_position}, {self.distance})'

    def __str__(self):
        return f'MoveEvent({self.user_id}, {self.scenary_type}, {self.start_datetime}, {self.end_datetime}, \
        {self.start_position}, {self.end_position}, {self.distance})'

    def as_dict(self):
        return {"user_id": self.user_id, "start_datetime": self.start_datetime, "end_datetime": self.end_datetime, 
        "start_position": self.start_position, "end_position": self.end_position, "distance": self.distance}

    def get_real_time(self):
        return datetime.fromtimestamp(int(self.start_datetime)).strftime("%Y-%m-%d %H:%M:%S"), datetime.fromtimestamp(int(self.end_datetime)).strftime("%Y-%m-%d %H:%M:%S")



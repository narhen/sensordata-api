from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)

class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)
    temperature = Column(Float)
    time = Column(Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in ["id", "user_id"]}

class Storage:
    def __init__(self, db_uri):
        self.db_uri = db_uri
        engine = create_engine(self.db_uri)
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        self.DBSession = sessionmaker(bind=engine)

    def new_temperature(self, **kwargs):
        temperature = Temperature(**kwargs)
        session = self.DBSession()
        session.add(temperature)
        session.commit()

        return temperature

    def get_temperatures(self, user_id, start_time, end_time):
        return self.DBSession().query(Temperature).filter(\
            Temperature.user_id == user_id,\
            Temperature.time >= start_time,\
            Temperature.time <= end_time).all()


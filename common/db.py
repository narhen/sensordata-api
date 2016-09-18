from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class DBUser(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)

    def as_dict(self): return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class DBTemperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(DBUser)
    temperature = Column(Float)
    time = Column(Integer)

    def as_dict(self): return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in ["id", "user_id"]}

class Storage:
    def __init__(self, db_uri):
        self.db_uri = db_uri

        engine = create_engine(self.db_uri)
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        self.DBSession = sessionmaker(bind=engine)

    def _delete_dict_elements(self, dct, elements):
        for element in elements:
            if element in dct:
                del dct[element]
        return dct

    def new_temperature(self, **kwargs):
        temperature = DBTemperature(**kwargs)
        session = self.DBSession()
        session.add(temperature)
        session.commit()

        return temperature

    def get_temperatures(self, user_id, start_time, end_time):
        return self.DBSession().query(DBTemperature).filter(\
            DBTemperature.user_id == user_id,\
            DBTemperature.time >= start_time,\
            DBTemperature.time <= end_time).all()

    def get_user_by_name_with_password(self, username):
        user = self.DBSession().query(DBUser).filter(DBUser.name == username).first()
        if not user:
            return None

        return user.as_dict()

    def get_user_by_name(self, username):
        user = self.get_user_by_name_with_password(username)
        if not user:
            return None

        return self._delete_dict_elements(user, ["password"])

    def _get_user_by_id(self, id):
        return self.DBSession().query(DBUser).filter(DBUser.id == id).first()

    def get_user_by_id(self, id):
        user = self._get_user_by_id(id)
        if not user:
            return None

        return self._delete_dict_elements(user.as_dict(), ["password"])

    def new_user(self, username, hashed_password):
        if self.get_user_by_name(username):
            return None

        session = self.DBSession()
        session.add(DBUser(name=username, password=hashed_password))
        session.commit()

        return self._delete_dict_elements(self.get_user_by_name(username), ["password"])

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings


DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))

def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)

def delete_from_model(model, engine, Session):
    session = Session()
    try:
        session.query(model).delete()
        session.commit()
    except:
        session.rollback()


class Habrahabr(DeclarativeBase):
    __tablename__ = 'habrahabr'
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    #comments = relationship('HabrahabrCommentModel', backref='habrahabr')


class HabrahabrComment(DeclarativeBase):
    __tablename__ = 'habrahabr_comment'
    id = Column(Integer, primary_key=True)
    comment = Column('comment', String)
    habrahabr_id = Column(Integer, ForeignKey('habrahabr.id', ondelete='CASCADE'))
    habrahabr = relationship(Habrahabr, backref=backref('habrahabr_comments', uselist=True, cascade='all,delete'))

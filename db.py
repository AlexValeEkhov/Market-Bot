from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://kgyfbgmq:K_OP3EH74Y-hBdik_n039glDvN99D4eM@mouse.db.elephantsql.com/kgyfbgmq')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
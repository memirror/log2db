# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/4/17

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from .proxy import Proxy
from .core import Save2db, LoggingMQHandler
from .db import Base, Logging


class init(object):
    def __init__(self, rebuild: bool = False):
        engine = create_engine(Proxy.DBURL, echo=Proxy.ECHO, **Proxy.DBKWS)
        session = scoped_session(sessionmaker(bind=engine))
        Save2db.session = session
        if rebuild:
            Base.metadata.drop_all(bind=engine, )
        Base.metadata.create_all(bind=engine, )
        self.session = session
    

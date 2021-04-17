# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/4/17

import os
import json
from datetime import datetime

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Column, create_engine
from sqlalchemy import Integer, DateTime, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

from .constants import LOGGING_TABLE_NAME


Base = declarative_base(name="Base")


class Logging(Base):
    __tablename__ = LOGGING_TABLE_NAME

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True)
    message = Column(String(512), nullable=False)
    levelname = Column(String(32), index=True, nullable=False)
    levelno = Column(Integer)
    pathname = Column(String(255), index=True)
    filename = Column(String(255))
    module = Column(String(255))
    exc_info = Column(String(1024))
    exc_text = Column(String(1024))
    stack_info = Column(String(512))
    lineno = Column(Integer)
    funcName = Column("funcname", String(128))
    created = Column(DateTime)
    thread = Column(Integer)
    threadName = Column("threadname", String(64))
    process = Column(Integer)
    processName = Column("processname", String(64))
    extra = Column(String(512))

    def __init__(self, mapping: dict):
        self.preprocess(mapping)

    def preprocess(self, mapping: dict):
        d = {}
        for k, v in mapping.items():
            if hasattr(type(self), k):
                if k in {"created"}:
                    v = datetime.fromtimestamp(float(v))
                setattr(self, k, v)
            else:
                d[k] = v
        self.extra = json.dumps(d, ensure_ascii=False)
   

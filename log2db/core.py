# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/4/17

import json
import time
import logging
from logging import LogRecord
from threading import Thread

from .mq import simple
from .db import Logging


class LoggingMQHandler(logging.Handler):

    mq = simple.Simple()

    def __init__(self, level) -> None:
        super().__init__(level)
        Log2db(self).run()

    def emit(self, record: LogRecord) -> None:
        d = record.__dict__.copy()
        d["message"] = str(d.pop("msg")) % tuple(d.pop("args"))
        for k, v in d.items():
            try:
                d[k] = json.dumps(v)
            except TypeError:
                d[k] = str(v)
        type(self).mq.push_message(json.dumps(d, ensure_ascii=False))


class Log2db(object):
    def __init__(self, handler: logging.Handler):
        self.handler = handler

    def _run(self):
        if hasattr(self.handler, "mq"):
            while True:
                v = self.handler.mq.pull_message()
                if v:
                    Save2db(v).process()
                else:
                    time.sleep(1)

    def run(self):
        Thread(target=self._run, ).start()


class Save2db(object):

    def __init__(self, v: str):
        self.v = v
        self.preprocess()

    def preprocess(self):
        if isinstance(self.v, str):
            self.v = json.loads(self.v)

    def process(self):
        self.session.add(Logging(self.v))
        self.session.commit()
   

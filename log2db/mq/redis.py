# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/4/17

import json

import redis

from .base import MQBase
from ..constants import TOPIC


class RedisMQ(MQBase):
    storage = redis.Redis(decode_responses=True)
    p = storage.pubsub()

    def __init__(self, topic: str = TOPIC):
        print(topic)
        super().__init__(topic)
        self.p.subscribe(self.topic)

    def push_message(self, message: str) -> None:
        self.storage.publish(self.topic, message)

    def pull_message(self) -> str:
        v = self.p.get_message()
        if v:
            try:
                return json.loads(v["data"])
            except:
                # FIXME
                pass
  

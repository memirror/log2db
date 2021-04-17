# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/4/17

from abc import abstractmethod

from ..constants import TOPIC


class MQBase(object):

    def __init__(self, topic: str = TOPIC):
        self.topic = topic

    @abstractmethod
    def push_message(self, message: str) -> None:
        pass

    @abstractmethod
    def pull_message(self) -> str:
        pass
  

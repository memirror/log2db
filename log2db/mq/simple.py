# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/4/17

from queue import Queue

from .base import MQBase
from ..constants import MAX_SIZE


class Simple(MQBase):

    storage = Queue(maxsize=MAX_SIZE)

    def push_message(self, message: str) -> None:
        self.storage.put_nowait(message)

    def pull_message(self) -> str:
        if self.storage.empty():
            return None
        return self.storage.get_nowait()
   

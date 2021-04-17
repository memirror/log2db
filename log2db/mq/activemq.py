
# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/4/17

from stomp import Connection10
from stomp.connect import StompConnection10
from stomp.listener import ConnectionListener

from .base import MQBase


class ActiveMQ(object):
    def __init__(self, host_and_ports=None, username=None, passwd=None):
        if host_and_ports is None:
            self.host_and_ports = [('localhost', 61613)]
        if username is None and passwd is None:
            username = passwd = "admin"
        self.username = username
        self.passwd = passwd


class Consumer(ActiveMQ, ConnectionListener):
    def __init__(self, host_and_ports=None, username=None, passwd=None):
        ActiveMQ.__init__(self, host_and_ports, username, passwd)
        self.conn = Connection10(self.host_and_ports, reconnect_attempts_max=10)
        self.conn.set_listener("", self)
        self.conn.connect(self.username, self.passwd)

    def on_message(self, message):
        self.message = message.body
        self.conn.ack(message.headers["message-id"])

    def receivemsg(self, destination):
        self.conn.subscribe(destination, ack="client-individual")


class Producer(ActiveMQ, StompConnection10):
    def __init__(self, host_and_ports=None, username=None, passwd=None):
        StompConnection10.__init__(self, reconnect_attempts_max=10)
        ActiveMQ.__init__(self, host_and_ports, username, passwd)
        self.conn = Connection10(self.host_and_ports)
        self.conn.connect(self.username, self.passwd)

    def sendmsg(self, destination, msg, content_type=None, headers=None, **kw):
        self.conn.send(destination, msg, content_type=content_type, headers=headers, **kw)


class ActiveMQ(MQBase):

    storage = Producer()
    consumer = Consumer()

    def push_message(self, message: str) -> None:
        self.storage.sendmsg(self.topic, message)

    def pull_message(self) -> str:
        self.consumer.receivemsg(self.topic)
        if hasattr(self.consumer, "message"):
            return self.consumer.message
  

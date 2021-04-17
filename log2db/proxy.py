# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/4/17


class _Proxy:
    DBURL = "sqlite:///{}".format("logging.db")
    DBKWS = dict(connect_args={"check_same_thread": False})
    ECHO = 0

class Proxy(_Proxy):
    pass
   

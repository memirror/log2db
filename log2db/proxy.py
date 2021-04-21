# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/4/17


class _Proxy:
    DBURL = "sqlite:///{}".format("logging.db")
    DBKWS = dict(connect_args={"check_same_thread": False})
    ECHO = 0

class Proxy(_Proxy):
    pass

class Config:
    _cfg = {}

    def set(self, key, value):
        self._cfg[key] = value
        return self

    @classmethod
    def get(cls, key):
        return cls._cfg[key]

    def __getattr__(self, item):
        def _(*args, **kwargs):
            if not args and not kwargs:
                return self
            if len(args) == 1 and not kwargs.pop("_keeplist", False):
                self.set(item, args[0])
            else:
                self.set(item, args)
            for key, value in kwargs.items():
                if key == "_keeplist":
                    continue
                self.set(key, value)
            self.__dict__ = self._cfg
            return self
        return _


if __name__ == '__main__':

    Config().url("localhost")
    Config().echo(False)

    print(Config.get("url"))
    print(Config.get("echo"))
  

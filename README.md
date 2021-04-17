[![branch](https://img.shields.io/badge/branch-master-brightgreen.svg)](https://github.com/xiaodongxiexie/autoSlowSQLKiller)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/xiaodongxiexie/autoSlowSQLKiller)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/xiaodongxiexie/autoSlowSQLKiller)
[![use language](https://img.shields.io/badge/language-python3-orange.svg)](https://github.com/xiaodongxiexie/autoSlowSQLKiller)
[![write by](https://jaywcjlove.github.io/sb/lang/chinese.svg)](https://github.com/xiaodongxiexie/autoSlowSQLKiller)

# log2db
基于消息队列的非阻塞式将日志持久化到数据库

```python

import logging

from log2db import init, Proxy, LoggingMQHandler
from log2db.mq import redis

LoggingMQHandler.mq = redis.RedisMQ()
Proxy.DBURL = "sqlite:///{}".format("mylogger.db")

_ = init()

logger = logging.getLogger("log2db")
logger.parent = None
handler = LoggingMQHandler(logging.INFO)
logger.addHandler(handler)

if __name__ == '__main__':

    import random, time

    from log2db import Logging

    session = _.session

    logger.info("this is a test", extra={"user": "none"})
    logger.warning("this is a warn %s", "ohuo")
    try:
        1/0
    except:
        logger.exception("this is a exception", exc_info=True)

    print(session.query(Logging).count())

    for i in range(1000):
        random.choice([logger.info, logger.warning, logger.exception, logger.debug])(i)

    print(session.query(Logging).count())
    # time.sleep(3)
    print(session.query(Logging).count())

```

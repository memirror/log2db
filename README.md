[![branch](https://img.shields.io/badge/branch-master-brightgreen.svg)](https://github.com/xiaodongxiexie/log2db)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/xiaodongxiexie/log2db)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/xiaodongxiexie/log2db)
[![use language](https://img.shields.io/badge/language-python3-orange.svg)](https://github.com/xiaodongxiexie/log2db)
[![write by](https://jaywcjlove.github.io/sb/lang/chinese.svg)](https://github.com/xiaodongxiexie/log2db)

# log2db
基于消息队列的非阻塞式将日志持久化到数据库

## Install

```cmd
pip install -U https://github.com/xiaodongxiexie/log2db/tree/release
```

or

```cmd
git clone https://github.com/xiaodongxiexie/log2db
pip install .
```

## Usage Example

### 简单使用
```python

import logging

from log2db import init, Proxy, LoggingMQHandler

# 设置存储数据库链接
# sqlite
Proxy.DBURL = "sqlite:///{}".format("mylogger.db")
#MySQL
Proxy.DBURL = "mysql+pymysql://username:password@127.0.0.1:3306/your-database"


# 重建库表
# _ = init(rebuild=True)

# 存在则复用，否则重建
_ = init()

logger = logging.getLogger("log2db")
logger.parent = None
handler = LoggingMQHandler(logging.INFO)
logger.addHandler(handler)


if __name__ == '__main__':

    logger.info("this is a test", extra={"user": "none"})
    logger.warning("this is a warn %s", "ohuo")
    try:
        1/0
    except:
        logger.exception("this is a exception", exc_info=True)
```

### 使用redis或activemq 作为消息队列
```python

import logging

import redis as _redis

from log2db import init, Proxy, LoggingMQHandler
from log2db.mq import redis
from log2db.mq import activemq

# 使用redis作为消息队列(程序异常崩溃后日志数据不影响)
# redis 设置host, port, password等
redis.RadisMQ.storage = _redis.Redis(host="", port=6379, password=None, decode_responses=True)
LoggingMQHandler.mq = redis.RedisMQ()


# 使用activemq作为消息队列
# LoggingMQHandler.mq = activemq.ActiveMQ()

# 设置存储数据库链接
# sqlite
Proxy.DBURL = "sqlite:///{}".format("mylogger.db")
#MySQL
Proxy.DBURL = "mysql+pymysql://username:password@127.0.0.1:3306/your-database"

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

import os
import logging
from celery import Celery
from toolkit.cache import Cache
from config import current_config
from toolkit.initlogs import log_init
from tornsql.session import create_engine, create_db

# 初始化日志配置文件
local_cfg_path = os.path.abspath('logging.cfg')
log_init(file=local_cfg_path)

# 缓存管理
cache = Cache(config=current_config)

# celery
celery = Celery('apizen',  broker=current_config.CELERY_BROKER_URL)
celery.config_from_object('config.current_config')

# 日志模块
logger = logging.getLogger('root')

# 数据库配置
demo_engine = create_engine(connect_str=current_config.DEMO_DB_CONNECT)
demo_db = create_db(demo_engine)

logs_engine = create_engine(current_config.BLOG_DB_CONNECT)
logs_db = create_db(logs_engine)

databases = {
    'demo':
        {
            'engine': demo_engine,
            'db': demo_db
        },
    'logs':
        {
            'engine': logs_engine,
            'db': logs_db
        }
}

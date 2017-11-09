import os
import logging
from celery import Celery
from toolkit.cache import Cache
from config import current_config
from toolkit.initlogs import log_init

# 初始化日志配置文件
local_cfg_path = os.path.abspath('logging.cfg')
log_init(file=local_cfg_path)

torconf = {
        'style_path': os.path.join(os.path.dirname(__file__), 'style'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'upload_path': os.path.join(os.path.dirname(__file__), 'upload'),
        'cookie_secret': current_config.get('COOKIE_SECRET'),
        'login_url': current_config.get('LOGIN_URL'),
        "xsrf_cookies": True,
        'autoescape': None
    }

# 缓存管理
cache = Cache(config=current_config)

# celery
celery = Celery('apizen',  broker=current_config.CELERY_BROKER_URL)
celery.config_from_object('config.current_config')

# 日志模块
logger = logging.getLogger('root')

import os
from webapi import routing
from tookit.cache import Cache
from config import current_config
from tookit.initlogs import log_init


# 初始化日志配置文件
log_init(file=os.path.abspath('logging.cfg'))

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

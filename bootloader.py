import os
from configs import config
from webapi import routing
from tookit.cache import Cache
from tookit.initlogs import log_init


# 初始化日志配置文件
local_cfg_path = os.path.abspath('logging.cfg')
log_init(file=local_cfg_path)

torconf = {
        'style_path': os.path.join(os.path.dirname(__file__), 'style'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'upload_path': os.path.join(os.path.dirname(__file__), 'upload'),
        'cookie_secret': config.get('COOKIE_SECRET'),
        'login_url': config.get('LOGIN_URL'),
        "xsrf_cookies": True,
        'autoescape': None
    }

# 缓存管理
cache = Cache(config=config)

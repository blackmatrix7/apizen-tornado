# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/1/4 10:30
# Author: Matrix
# Site:
# File: log.py
# Software: PyCharm

import logging
import logging.config
import traceback
import os

if not os.path.exists("logs"):
    os.mkdir("logs")


def log_init(file):
    try:
        logging.config.fileConfig(file, disable_existing_loggers=False)
    except Exception as ex:
        f = open('logs/traceback.txt', 'a')
        traceback.print_exc()
        traceback.print_exc(file=f)
        f.flush()
        f.close()

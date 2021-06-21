#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import os
from sys import path

commpath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "comm"))
path.append(commpath)
path.append("../config")

from config import config
from config.config import *

try:
    import codecs
except ImportError:
    codecs = None

FORMATER = "[%(asctime)s,%(msecs)03d][%(levelname)s][%(process)d][%(filename)s(%(lineno)d)][%(funcName)s]:%(message)s"
# datefmt='%Y-%m-%d,%H:%M:%S'
DATE_FMT = "%H:%M:%S"
WHEN_SPLIT_MN = "midnight"  # at 12 PM
SPLIT_INTE = 1  # one day
BACKUP_CNT = 0  # 0:don't delete history logfile

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class LoggerHandler(TimedRotatingFileHandler):
    """
    TimedRotatingFileHandler
    """

    def __init__(self, log_dir, log_name):
        self.log_dir = log_dir
        self.file_name = "{}.log".format(log_name)
        self._mkdirs()
        self.baseFilename = os.path.join(self.log_dir, self.file_name)
        """
        When computing the next rollover time for the first time (when the handler is created)
        the last modification time of an existing log file, or else the current time
        is used to compute when the next rotation will occur.
        """
        TimedRotatingFileHandler.__init__(
            self,
            self.baseFilename,
            when=WHEN_SPLIT_MN,
            interval=SPLIT_INTE,
            backupCount=BACKUP_CNT,
            encoding=None,
        )

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        dt = datetime.now()
        # get the time that this sequence started at and make it a TimeTuple
        self.baseFilename = "%s-%s" % (
            os.path.join(self.log_dir, self.file_name),
            dt.strftime("%Y-%m-%d"),
        )
        self.stream = open(self.baseFilename, "a")
        self.rolloverAt = self.rolloverAt + self.interval

    def _mkdirs(self):
        try:
            os.makedirs(self.log_dir)
            os.chmod(self.log_dir, 755)
            os.access(self.log_dir, os.W_OK | os.X_OK)
        except:
            pass


class Logger(object):
    _instance_lock = threading.Lock()
    _log = {}

    def __init__(self, log_dir=None, log_name="app", log_level="debug"):
        # with Logger._instance_lock:
        #     if Logger._log.get(log_name) is not None:
        #         return
        Logger._log[log_name] = logging.getLogger(log_name)
        filehandler = LoggerHandler(log_dir, log_name)
        filehandler.suffix = "%Y-%m-%d"
        filehandler.setFormatter(logging.Formatter(FORMATER, DATE_FMT))
        Logger._log[log_name].addHandler(filehandler)
        Logger._log[log_name].setLevel(LOG_LEVELS.get(log_level.upper(), logging.DEBUG))

    def __new__(cls, *args, **kwargs):
        if len(args) > 1:
            name = args[1]
        else:
            name = kwargs.get("log_name", "app")
        with Logger._instance_lock:
            if Logger._log.get(name) is None:
                Logger._log[name] = object.__new__(cls)
        return Logger._log[name]

    @staticmethod
    def get_logger(log_name="app"):
        return logging.getLogger(log_name)


def get_logger(log_name="app", log_level="debug", log_dir=None):
    if log_dir is None:
        log_dir = LOG_DIR
    Logger(log_dir=log_dir, log_name=log_name, log_level=log_level)
    return Logger.get_logger(log_name=log_name)


log = Logger.get_logger()

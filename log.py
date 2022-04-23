import os
import logging
from common import singleton

@singleton
class Log():
    def __init__(self):
        self.logger = logging.getLogger()
        self.setLevel('DEBUG')
        log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log')
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        log_file = os.path.join(log_dir, 'log.log')
        if not os.path.exists(log_file):
            with open(log_file, 'w', encoding='utf-8') as a:
                pass
        info_fh = logging.FileHandler(log_file,mode='a', encoding='utf-8')
        formatter = logging.Formatter(
            '[%(levelname)s]\t%(asctime)s\t%(filename)s:%(lineno)d\tpid:%(thread)d\t%(message)s')
        info_fh.setFormatter(formatter)
        self.logger.addHandler(info_fh)
        self.logger.info('log模块初始化完成')

    def __call__(self):
        return self.logger

    def setLevel(self,level):
        lmap = {
            'NOTSET':logging.NOTSET,
            'DEBUG':logging.DEBUG,
            'INFO':logging.INFO,
            'WARNING':logging.WARNING,
            'ERROR':logging.ERROR,
            'CRITICAL':logging.CRITICAL
        }
        self.logger.setLevel(lmap[level])


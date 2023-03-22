#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
	'[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
	datefmt='%Y%m%d %H:%M:%S')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

log_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S.log")
fh = logging.FileHandler(log_filename)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

if __name__ == "__main__":
	logging.debug('debug')
	logging.info('info')
	logging.warning('warning')
	logging.error('error')
	logging.critical('critical')
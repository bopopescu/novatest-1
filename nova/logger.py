import logging
logger = logging.getLogger("nova-test")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(module)s:%(filename)s:%(funcName)s:%(lineno)d %(message)s","%H:%M:%S")
fh = logging.FileHandler("/tmp/nova.log")
fh.setFormatter(formatter)

logger.addHandler(fh)

import logging
import inspect

def generate_logger(name="nova-test",filename="/tmp/nova.log"):
    logger = logging.getLogger("nova-test")

    if len(logger.handlers) == 0:
        formatter = logging.Formatter("%(asctime)s %(pathname)s:%(filename)s:%(funcName)s:%(lineno)d %(message)s","%H:%M:%S")
        fh = logging.FileHandler(filename)
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

    return logger

def get_caller(num=5):
    current_frame = inspect.currentframe()
    outerframes = inspect.getouterframes(current_frame)
    return map(lambda x:[x[1],x[2],x[3]],outerframes)[1:num]

#def get_caller(num=5):
#    record = dict()
#    current_frame = None
#    for x in xrange(num):
#        if current_frame is None:
#           current_frame = inspect.currentframe()
#        current_frame = getattr(current_frame,"f_back")
#        caller = inspect.getframeinfo(curent_frame)[2]
#        record[caller] = record.get(caller,0) + 1
#    callers = sorted(record.items(),key=lambda a:a[1])
#    return callers

logger = generate_logger()
msg_logger = generate_logger("nova-msg","/tmp/nova-msg.log")
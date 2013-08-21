import logging
import inspect

#def generate_logger(name="nova-test",filename="/tmp/nova.log"):
#    logger = logging.getLogger("nova-test")
#
#    if len(logger.handlers) == 0:
#        formatter = logging.Formatter("%(asctime)s %(thread)d:%(pathname)s:%(filename)s:%(funcName)s:%(lineno)d %(message)s","%H:%M:%S.%f")
#        fh = logging.FileHandler(filename)
#        fh.setFormatter(formatter)
#        fh.setLevel(logging.DEBUG)
#        logger.addHandler(fh)
#
#    return logger

def get_caller(num=5):
    current_frame = inspect.currentframe()
    outerframes = inspect.getouterframes(current_frame)
    return map(lambda x:[x[1],x[2],x[3]],outerframes)[1:num]

class Color:
    normal = "\033[0m"
    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    purple = "\033[35m"
    cyan = "\033[36m"
    grey = "\033[37m"

    bold = "\033[1m"
    uline = "\033[4m"
    blink = "\033[5m"
    invert = "\033[7m"

class AnsiColorTheme(object):
    def __getattr__(self, attr):
        if attr.startswith("__"):
            raise AttributeError(attr)
        s = "style_%s" % attr
        if s in self.__class__.__dict__:
            before = getattr(self, s)
            after = self.style_normal
        else:
            before = after = ""

        def do_style(val, fmt=None, before=before, after=after):
            if fmt is None:
                if type(val) is not str:
                    val = str(val)
            else:
                val = fmt % val
            return before+val+after
        return do_style

class DefaultTheme(AnsiColorTheme):
    style_normal = Color.normal
    style_prompt = Color.blue+Color.bold
    style_punct = Color.normal
    style_id = Color.blue+Color.bold
    style_not_printable = Color.grey
    style_class_name = Color.red+Color.bold
    style_field_name = Color.blue
    style_field_value = Color.purple
    style_emph_field_name = Color.blue+Color.uline+Color.bold
    style_emph_field_value = Color.purple+Color.uline+Color.bold
    style_watchlist_type = Color.blue
    style_watchlist_value = Color.purple
    style_fail = Color.red+Color.bold
    style_success = Color.blue+Color.bold
    style_even = Color.black+Color.bold
    style_odd = Color.black
    style_yellow = Color.yellow
    style_active = Color.black
    style_closed = Color.grey
    style_left = Color.blue+Color.invert
    style_right = Color.red+Color.invert

theme = default_theme = DefaultTheme()

#https://gist.github.com/tzuryby/1474991
class ColoredLogger(logging.Logger):

    PACKAGE = {'COMPUTE':theme.style_right,'API':theme.style_left,'NETWORK':theme.style_yellow,
               'CONDUCTOR':theme.style_id,'CERT':theme.style_even,'VIRT':theme.style_success,
               'SCHEDULER':theme.style_prompt,'OPENSTACK':theme.style_emph_field_name}

    def __init__(self,name='nova-test',filename='/tmp/nova.log'):
        logging.Logger.__init__(self,name,logging.DEBUG)
        formatter = formatter = logging.Formatter("%(asctime)s %(thread)d:%(pathname)s:%(funcName)s:%(lineno)d %(message)s","%H:%M:%S")
        fh = logging.FileHandler(filename)
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)
        self.addHandler(fh)

    def debug(self, msg, *args, **kwargs):
        m = '{}'
        _msg = ''
        if isinstance(msg,dict):
            _msg += m.format(type(msg))
            for k,b in msg.items():
                string = '\n' + theme.style_yellow + ''.join(m.format(i) for i in k) + theme.style_normal + ':' + m.format(b)
                _msg += string 
            msg = _msg
        elif hasattr(msg,"__iter__"):
            _msg += m.format(type(msg))
            for x in msg:
                if hasattr(x,"__iter__"):
                   _msg += "\n" + "NEST ITER"
                   for _x in x:
                       string = '\n' + m.format(_x)
                       _msg += string
                   _msg += "\n" + "NEST FINISH"
                   continue
                string = '\n' + m.format(x)
                _msg += string 
            msg = _msg
        if self.isEnabledFor(logging.DEBUG):             
           self._log(logging.DEBUG, msg, args, **kwargs)
        #logging.Logger.debug(self,msg,*args,**kwargs)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        i = fn.rfind('nova')
        fn = fn[i:]
        #msg = fn.split('/')[1].upper() + ":" + self.PACKAGE.get(fn.split('/')[1].upper(),"NONE")
        fn = self.PACKAGE.get(fn.split('/')[1].upper(),theme.style_normal) + ''.join(str(i) for i in fn) + theme.style_normal
        #fn = self.PACKAGE.get("OPENSTACK") + ''.join(str(i) for i in fn) + theme.style_normal
        #if args.('color')
        return logging.Logger.makeRecord(self,name, level, fn, lno, msg, args, exc_info, func, extra)

logger = ColoredLogger()
msg_logger = ColoredLogger("nova-msg","/tmp/nova-msg.log")

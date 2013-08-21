from nova.logger import ColoredLogger
def main():
   c = ColoredLogger("test","/tmp/test.log")
   c.debug("hello")

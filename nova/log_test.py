from logger import ColoredLogger,get_caller
def main():
   c = ColoredLogger("test","/tmp/test.log")
   c.info("hello")
   c.debug([1,2,3,[1,2]])
   c.debug({"HEllo":"world","hello":{'aaa'}})
   c.debug(get_caller())

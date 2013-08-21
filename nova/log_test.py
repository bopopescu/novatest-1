from logger import ColoredLogger
def main():
   c = ColoredLogger("test","/tmp/test.log")
   c.info("hello")
   c.debug([1,2,3,[1,2]])
   c.debug({"HEllo":"world","hello":{'aaa'}})

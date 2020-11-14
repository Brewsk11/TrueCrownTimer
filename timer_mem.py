import time
import sys
from ProcessMemoryReaders import Spelunky2MemReader

if __name__ == '__main__':

    spelunkyReader = Spelunky2MemReader()

    while(True):
        timer = spelunkyReader.readLevelTimer()
        print("\r{:.2f}".format(timer), end='')
        sys.stdout.flush()
        time.sleep(1.0 / 12)
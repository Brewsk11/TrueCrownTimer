from ctypes import *
from ctypes.wintypes import *
import pymem
import time
import sys

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle

PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_VM_READ  = 0x0010


class ProcessMemReader:

    def __init__(self):
        self.process_handle = None

    def attachByName(self, name):
        pid = self.__getPid(name)
        return self.attachByPID(pid)

    def attachByPID(self, pid):
        self.process_handle = OpenProcess(PROCESS_VM_READ, False, pid)
        return self.process_handle

    def isAttached(self):
        return self.process_handle is not None

    def __read(self, address, ptr_type, size):
        if self.process_handle == None:
            raise RuntimeError('Attach to a process first')

        buffer = (c_byte * size)() 
        buffer_size = size
        bytes_read = c_ulong(-1)

        res = ReadProcessMemory(self.process_handle, c_void_p(address), buffer, buffer_size, byref(bytes_read))
        if res:
            value = cast(buffer, ptr_type).contents.value
            return value
        else:
            e = windll.kernel32.GetLastError()
            raise RuntimeError(f'Couldnt read process memory, error code: {e}')

    def readUInt32(self, address):
        return self.__read(address, PUINT, 4)

    def readInt32(self, address):
        return self.__read(address, PINT, 4)

    def readUInt64(self, address):
        # Assuming little endian
        lo_address = address
        hi_address = address + 4

        lo_val = self.__read(lo_address, PUINT, 4)
        hi_val = self.__read(hi_address, PUINT, 4)

        return self.__i32x2_to_i64(hi_val, lo_val)

    # Utilities
    def __i32x2_to_i64(self, hi, lo):
        hi_ = hi << 32
        return hi_ + lo

    def __getPid(self, process_name):
        import psutil
        pids = psutil.pids()
        for pid in pids:
            ps = psutil.Process(pid)
            if process_name in ps.name():
                print(f"{process_name} found with PID {ps.pid}")
                return ps.pid
        raise ValueError(f'Process {process_name} not found')


class Spelunky2MemReader(ProcessMemReader):

    # These constants may change when Spelunky 2 version get's updated!
    # This version is guaranteed to be compatible with 1.16.1 version of the game.
    TIMER_BASE_ADDRESS_LOCATION = 0x7FF7091F2F60
    TIMER_OFFSET = 0x9FC

    def __init__(self):
        super().__init__()
        self.attachByName('Spel2.exe')
        self.level_timer_address = None
        self.acquireTimerAddress()

    def acquireTimerAddress(self):
        timer_base_address = self.readUInt64(self.TIMER_BASE_ADDRESS_LOCATION)
        self.level_timer_address = timer_base_address + self.TIMER_OFFSET

    def readLevelTimerValue(self):
        """
        This returns the number of frames elapsed from
        the start of the level.
        """
        if self.level_timer_address == None:
            raise RuntimeError("The timer address hasn't been acquired")

        frames_elapsed = self.readUInt32(self.level_timer_address)
        return frames_elapsed

    def readLevelTimer(self, fps=60):
        """
        This returns the seconds elapsed from the start of the level
        for specific game's frames per second. The frames are most likely physics frames
        so 60 fps should return consistent results, but leaving the option for
        potential future changes. 
        """
        frames_elapsed = self.readLevelTimerValue()
        return frames_elapsed / fps

if __name__ == '__main__':

    spelunkyReader = Spelunky2MemReader()

    while(True):
        timer = spelunkyReader.readLevelTimer()
        print("\r{:.2f}".format(timer), end='')
        sys.stdout.flush()
        time.sleep(1.0 / 12)
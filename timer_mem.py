from ctypes import *
from ctypes.wintypes import *
import psutil
import pymem
import time
import sys

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle

PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_VM_READ  = 0x0010

TIMER_BASE_ADDRESS = 0x7FF7091F2F60
TIMER_OFFSET = 0x9FC

def getPid(process_name):
    pids = psutil.pids()
    for pid in pids:
        ps = psutil.Process(pid)
        if process_name in ps.name():
            print(f"{process_name} found with PID {ps.pid}")
            return ps.pid
    raise ValueError(f'Process {process_name} not found')

def readInt32(process_handle, address):
    buffer = (c_byte * 4)() 
    buffer_size = 4
    bytes_read = c_ulong(-1)

    res = ReadProcessMemory(process_handle, c_void_p(address), buffer, buffer_size, byref(bytes_read))
    if res:
        value = cast(buffer, PUINT).contents.value
        return value
    else:
        e = windll.kernel32.GetLastError()
        raise RuntimeError(f'Couldnt read process memory, error code: {e}')

def merge2x32bit(hi, lo):
    hi_ = hi << 32
    return hi_ + lo


if __name__ == '__main__':

    ## INITIALIZATION

    # Get Spelunky 2 process ID and open handle
    pid = getPid('Spel2.exe')
    process_handle = OpenProcess(PROCESS_VM_READ, False, pid)


    ## GETTING TIMER ADDRESS

    base_timer_ptr_lo = TIMER_BASE_ADDRESS
    base_timer_ptr_hi = TIMER_BASE_ADDRESS + 4

    address_lo = readInt32(process_handle, base_timer_ptr_lo)
    address_hi = readInt32(process_handle, base_timer_ptr_hi)

    base_timer_address = merge2x32bit(address_hi, address_lo)

    timer_address = base_timer_address + TIMER_OFFSET

    while(True):
        timer = readInt32(process_handle, timer_address)
        print("\r{:.2f}".format(timer / 60), end='')
        sys.stdout.flush()
        time.sleep(1.0 / 12)
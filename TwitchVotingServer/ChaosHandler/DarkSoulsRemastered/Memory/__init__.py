import struct

from .AOBS import *


def packBytes(address):
    return struct.pack("<Q", address)


def bytesToHexString(byte_data):
    return "".join("\\x%02x" % i for i in byte_data)


def get_pointer_address(pm, base, offsets=False):
    addr = pm.read_ulonglong(base)

    if not offsets:  # No offsets, return address
        return addr

    for i in offsets[:-1]:  # Loop over all but the last
        addr = pm.read_ulonglong(addr + i)
    return addr + offsets[-1]

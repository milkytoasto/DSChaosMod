import struct

from DarkSoulsRemastered.Memory.AOBS import *


def packBytes(address):
    return struct.pack("<Q", address)


def bytesToHexString(byte_data):
    return "".join("\\x%02x" % i for i in byte_data)

import struct

from pymem import pattern


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


def __getBase(pm, module, AOB):
    GetBase = pattern.pattern_scan_module(pm.process_handle, module, AOB)
    Base = GetBase + pm.read_int(GetBase + 3) + 7
    return Base


class AOBS:
    BaseA = rb"\x48\x89\x05....\x8D\x42"
    BaseB = rb"\x48\x8B\x05....\x45\x33\xED\x48\x8B\xF1\x48\x85\xC0"
    BaseC = rb"\x48\x8B\x05....\x0F\x28\x01\x66\x0F\x7F\x80..\x00\x00\xC6\x80"
    BaseD = rb"\x48\x8B\x05....\x80\xB8\xB0\x00\x00\x00\x00\x0F\x84....\x8B\x51\x24\x48"
    BaseE = rb"\x48\x8B\x05....\x48\x8B\x88\x98\x0B\x00\x00\x8B\x41\x3C\xC3"
    BaseP = rb"\x4C\x8B\x05....\x48\x63\xC9\x48\x8D\x04\xC9"
    BaseX = rb"\x48\x8B\x05....\x48\x39\x48\x68\x0F\x94\xC0\xC3"
    BaseZ = rb"\x48\x8B\x05....\xFF\x40\x1C\x48\x8B\xC3\x4D\x85\xE4"

    BaseCAR = rb"\x48\x8B\x05....\x48\x89\x48\x60\xE8"

    HomewardCall = rb"\x48\x89\x5C\x24\x08\x57\x48\x83\xEC\x20\x48\x8B\xD9\x8B\xFA\x48\x8B\x49\x08\x48\x85\xC9\x0F\x84....\xE8....\x48\x8B\x4B\x08"
    EnableSlide = rb"\x44\x88\x81\xC4\x03\x00\x00"


class BaseAddress:
    BaseA = lambda pm, module: __getBase(pm, module, AOBS.BaseA)
    BaseB = lambda pm, module: __getBase(pm, module, AOBS.BaseB)
    BaseC = lambda pm, module: __getBase(pm, module, AOBS.BaseC)
    BaseD = lambda pm, module: __getBase(pm, module, AOBS.BaseD)
    BaseE = lambda pm, module: __getBase(pm, module, AOBS.BaseE)
    BaseP = lambda pm, module: __getBase(pm, module, AOBS.BaseP)
    BaseX = lambda pm, module: __getBase(pm, module, AOBS.BaseX)
    BaseZ = lambda pm, module: __getBase(pm, module, AOBS.BaseZ)

    BaseCAR = lambda pm, module: __getBase(pm, module, AOBS.BaseCAR)

    HomewardCall = lambda pm, module: pattern.pattern_scan_module(
        pm.process_handle, module, AOBS.HomewardCall
    )

import struct


def pack_bytes(address):
    return struct.pack("<Q", address)


def bytes_to_hex_string(byte_data):
    return "".join("\\x%02x" % i for i in byte_data)

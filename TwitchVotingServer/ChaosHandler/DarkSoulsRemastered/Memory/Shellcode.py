from .utils import packBytes


class ShellCode:
    def WarpShellcode(BaseB, HomewardCall):
        shellcode = bytearray(b"\x48\xB9" + packBytes(BaseB))  # movabs rcx, [BaseB]
        shellcode.extend(b"\xBA\x01\x00\x00\x00")  # mov edx, 1
        shellcode.extend(b"\x48\x83\xEC\x38")  # sub rsp, 38
        shellcode.extend(
            b"\xFF\x15\x02\x00\x00\x00\xEB\x08" + packBytes(HomewardCall)
        )  # call HomewardCall
        shellcode.extend(b"\x48\x83\xC4\x38")  # add rsp, 38
        shellcode.extend(b"\xC3")  # ret
        return shellcode

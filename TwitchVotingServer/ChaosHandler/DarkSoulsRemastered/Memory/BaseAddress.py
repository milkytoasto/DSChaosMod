from pymem import pattern


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
    @classmethod
    def get_aob(cls, pm, module, AOB):
        GetBase = pattern.pattern_scan_module(pm.process_handle, module, AOB)
        Base = GetBase + pm.read_int(GetBase + 3) + 7
        return Base

    @classmethod
    def BaseA(cls, pm, module):
        return cls.get_aob(pm, module, AOBS.BaseA)

    @classmethod
    def BaseB(cls, pm, module):
        return cls.get_aob(pm, module, AOBS.BaseB)

    @classmethod
    def BaseC(cls, pm, module):
        return cls.get_aob(pm, module, AOBS.BaseC)

    @classmethod
    def BaseD(cls, pm, module):
        return cls.get_aob(pm, module, AOBS.BaseD)

    @classmethod
    def BaseE(cls, pm, module):
        return cls.get_aob(pm, module, AOBS.BaseE)

    @classmethod
    def BaseP(cls, pm, module):
        return cls.get_aob(pm, module, AOBS.BaseP)

    @classmethod
    def BaseX(cls, pm, module):
        return cls.get_aob(pm, module, AOBS.BaseX)

    @classmethod
    def BaseZ(cls, pm, module):
        return cls.get_aob(pm, module, AOBS.BaseZ)

    @classmethod
    def BaseCAR(cls, pm, module):
        return cls.get_aob(pm, module, AOBS.BaseCAR)

    @classmethod
    def HomewardCall(cls, pm, module):
        return pattern.pattern_scan_module(
            pm.process_handle, module, AOBS.HomewardCall
        )

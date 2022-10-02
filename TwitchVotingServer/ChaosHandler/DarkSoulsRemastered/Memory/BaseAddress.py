from pymem import pattern

from .Constants import AOBS


class BaseAddress:
    @staticmethod
    def get(pm, module, AOB):
        GetBase = pattern.pattern_scan_module(pm.process_handle, module, AOB)
        Base = GetBase + pm.read_int(GetBase + 3) + 7
        return Base

    def BaseA(pm, module):
        return BaseAddress.get(pm, module, AOBS.BaseA)

    def BaseB(pm, module):
        return BaseAddress.get(pm, module, AOBS.BaseB)

    def BaseC(pm, module):
        return BaseAddress.get(pm, module, AOBS.BaseC)

    def BaseD(pm, module):
        return BaseAddress.get(pm, module, AOBS.BaseD)

    def BaseE(pm, module):
        return BaseAddress.get(pm, module, AOBS.BaseE)

    def BaseP(pm, module):
        return BaseAddress.get(pm, module, AOBS.BaseP)

    def BaseX(pm, module):
        return BaseAddress.get(pm, module, AOBS.BaseX)

    def BaseZ(pm, module):
        return BaseAddress.get(pm, module, AOBS.BaseZ)

    def BaseCAR(pm, module):
        return BaseAddress.get(pm, module, AOBS.BaseCAR)

    def HomewardCall(pm, module):
        return pattern.pattern_scan_module(pm.process_handle, module, AOBS.HomewardCall)

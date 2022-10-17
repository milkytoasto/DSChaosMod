class PointerOffsets:
    HUD = [0x58, 0x11]
    DrawDistance = [0x60, 0x60, 0x5C]
    Slide = [0x68, 0x68, 0x48, 0x45C]
    PlayerHP = [0x68, 0x3E8]
    PlayerHeadSize = [0x10, 0x388]


class Pointer:
    @classmethod
    def get(cls, pm, base, offsets=False):
        addr = pm.read_ulonglong(base)

        if not offsets:  # No offsets, return address
            return addr

        for i in offsets[:-1]:  # Loop over all but the last
            addr = pm.read_ulonglong(addr + i)
        return addr + offsets[-1]

    @classmethod
    def HUD(cls, pm, BaseB):
        return cls.get(pm, BaseB, PointerOffsets.HUD)

    @classmethod
    def DrawDistance(cls, pm, BaseCAR):
        return cls.get(pm, BaseCAR, PointerOffsets.DrawDistance)

    @classmethod
    def Slide(cls, pm, BaseX):
        return cls.get(pm, BaseX, PointerOffsets.Slide)

    @classmethod
    def PlayerHP(cls, pm, BaseX):
        return cls.get(pm, BaseX, PointerOffsets.PlayerHP)

    @classmethod
    def PlayerHeadSize(cls, pm, BaseB):
        return cls.get(pm, BaseB, PointerOffsets.PlayerHeadSize)

    @classmethod
    def Loading(cls, pm, module):
        base = module.lpBaseOfDll + 0x01D05270
        return cls.get(pm, base, [0xF4])

from .Constants import PointerOffsets


class PointerAddress:
    @staticmethod
    def get(pm, base, offsets=False):
        addr = pm.read_ulonglong(base)

        if not offsets:  # No offsets, return address
            return addr

        for i in offsets[:-1]:  # Loop over all but the last
            addr = pm.read_ulonglong(addr + i)
        return addr + offsets[-1]

    def HUD(pm, BaseB):
        return PointerAddress.get(pm, BaseB, PointerOffsets.HUD)

    def DrawDistance(pm, BaseCAR):
        return PointerAddress.get(pm, BaseCAR, PointerOffsets.DrawDistance)

    def Slide(pm, BaseX):
        return PointerAddress.get(pm, BaseX, PointerOffsets.Slide)

    def PlayerHP(pm, BaseX):
        return PointerAddress.get(pm, BaseX, PointerOffsets.PlayerHP)

    def PlayerHeadSize(pm, BaseB):
        return PointerAddress.get(pm, BaseB, PointerOffsets.PlayerHeadSize)

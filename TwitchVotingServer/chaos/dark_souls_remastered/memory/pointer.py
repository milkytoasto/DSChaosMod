def _get_pointer(pm, base, offsets=False):
    addr = pm.read_ulonglong(base)

    if not offsets:  # No offsets, return address
        return addr

    for i in offsets[:-1]:  # Loop over all but the last
        addr = pm.read_ulonglong(addr + i)
    return addr + offsets[-1]


class PointerOffsets:
    class Interface:
        HUD = [0x58, 0x11]

    class Settings:
        DRAW_DISTANCE = [0x60, 0x60, 0x5C]

    class Player:
        class Stat:
            HP = [0x68, 0x3E8]

        class Body:
            HEAD_SIZE = [0x10, 0x388]

        class Animations:
            SLIDE = [0x68, 0x68, 0x48, 0x45C]

    class GameState:
        IS_LOADING = [0x0, 0x850, 0x88, 0x10, 0x168, 0x2F8]


class Pointer:
    class Interface:
        def hud(pm, BaseB):
            return _get_pointer(pm, BaseB, PointerOffsets.Interface.HUD)

    class Settings:
        def draw_distance(pm, BaseCAR):
            return _get_pointer(pm, BaseCAR, PointerOffsets.Settings.DRAW_DISTANCE)

    class Player:
        class Stat:
            def hp(pm, BaseX):
                return _get_pointer(pm, BaseX, PointerOffsets.Player.Stat.HP)

        class Body:
            def head_size(pm, BaseB):
                return _get_pointer(pm, BaseB, PointerOffsets.Player.Body.HEAD_SIZE)

        class Animations:
            def slide(pm, BaseX):
                return _get_pointer(pm, BaseX, PointerOffsets.Player.Animations.SLIDE)

    class GameState:
        def is_loading(pm, BaseA):
            pointer = _get_pointer(pm, BaseA, PointerOffsets.GameState.IS_LOADING)
            return pointer

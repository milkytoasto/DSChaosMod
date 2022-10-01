from ChaosHandler.Effect import BaseEffect

from .Effects import WarpToBonfire


class DarkSoulsRemastered:
    name = "Dark Souls Remastered"
    process_title = "DarkSoulsRemastered.exe"
    effects = [WarpToBonfire, BaseEffect, BaseEffect]

class BaseEffect:
    name = "Base Effect"
    seconds: int

    @classmethod
    def start(cls, *args):
        pass

    @classmethod
    def stop(cls, *args):
        pass

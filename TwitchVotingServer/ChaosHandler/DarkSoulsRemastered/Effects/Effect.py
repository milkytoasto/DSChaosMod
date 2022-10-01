from abc import abstractclassmethod, abstractmethod


class BaseEffect:
    name = "Base Effect"

    @classmethod
    def start(cls, *args):
        pass

    @classmethod
    def stop(cls, *args):
        pass

from abc import abstractclassmethod, abstractmethod


class BaseEffect:
    @classmethod
    def start(cls, *args):
        pass

    @classmethod
    def stop(cls, *args):
        pass

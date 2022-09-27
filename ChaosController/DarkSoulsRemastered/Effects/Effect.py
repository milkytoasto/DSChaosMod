from abc import abstractclassmethod, abstractmethod


class BaseEffect:
    @classmethod
    def start(cls):
        pass

    @classmethod
    def stop(cls):
        pass

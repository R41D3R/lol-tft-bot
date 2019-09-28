from abc import ABC, abstractmethod


class Event(ABC):
    def __init__(self, trigger, source):
        self.trigger = trigger
        self.source = source
        self.used = False

    @abstractmethod
    def activate(self, champion):
        pass

from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


class Widget(ABC):
    __str__ = render = lambda self: BeautifulSoup(str(self.root), 'html.parser').prettify()
    root = property(abstractmethod(lambda self: None))

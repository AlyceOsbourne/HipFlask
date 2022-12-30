from abc import ABC, abstractmethod
from types import MappingProxyType

from bs4 import BeautifulSoup
from jinja2 import Template

loaded_widget_templates = {}


def add_widget(name, widget, *args, template_args = None, template_kwargs = None, **kwargs):
    if name in loaded_widget_templates:
        raise ValueError(f"Widget {name} already exists")
    loaded_widget_templates[name] = Template(widget(*args, **kwargs), *template_args, *template_kwargs)


def get_widget(name):
    return loaded_widget_templates.get(name, None)


def get_widgets():
    return MappingProxyType(loaded_widget_templates)


def remove_widget(cls, name):
    return loaded_widget_templates.pop(name, None)


def clear_widgets():
    loaded_widget_templates.clear()


class Widget(ABC):
    __str__ = lambda self: BeautifulSoup(str(self.root), 'html.parser').prettify()
    root = property(abstractmethod(lambda self: None))

    def __init__(self, register = False):
        if register:
            add_widget(
                    self.__class__.__name__,
                    str(self),
            )

    def add_attribute_to(self, name, **attributes):
        if hasattr(self, name):
            attr = getattr(self, name)
            if hasattr(attr, 'add_attrs'):
                attr.add_attrs(**attributes)
                return
        raise AttributeError(f"Cannot add attributes to {name}")

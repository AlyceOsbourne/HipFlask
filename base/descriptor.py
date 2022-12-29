from collections.abc import Generator

from .nodes import BaseNode
from .builder import Node


class ClassNode:
    def __set_name__(self, owner, name):
        self.name = name

    def __init__(self, tag_name, *args, **kwargs):
        self.tag_name = tag_name
        self.args = list(args)
        self.kwargs = kwargs

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.__dict__.setdefault(
                self.name,
                Node(
                        BaseNode.get(self.tag_name),
                        *self.args,
                        **self.kwargs
                )
        )

    def __set__(self, instance, value):
        if instance is None:
            if isinstance(value, BaseNode):
                self.tag_name = value.tag
            elif isinstance(value, str):
                self.tag_name = value
            else:
                raise ValueError("Invalid value")
        parent = instance.__dict__.setdefault(
                self.name,
                Node(
                        BaseNode.get(self.tag_name),
                        *self.args,
                        **self.kwargs)
        )
        if isinstance(value, (tuple, list, Generator)):
            for item in value:
                self.__set__(instance, item)
        else:
            parent.append(value)

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute")

    def add_attrs(self, *args, **kwargs):
        self.args.extend(args)
        self.kwargs.update(kwargs)
        return self

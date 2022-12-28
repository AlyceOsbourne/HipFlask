from enum import Enum
from typing import NamedTuple

from bs4 import BeautifulSoup


class Builder:
    def __init__(
            self,
            node_type,
            *args,
            children = None,
            parent = None,
            **kwargs,
    ):
        self.node = node_type if isinstance(node_type, Node) else Node.get(node_type)
        self.args = args or tuple()
        self.kwargs = kwargs or dict()
        self.children = children or list()
        self.parent = parent

    def add_child(self, _node, *args, **kwargs):
        if isinstance(_node, str):
            try:
                _node = Builder(Node.get(_node), *args, **kwargs)
            except ValueError:
                pass
        if isinstance(_node, Builder):
            _node.__dict__.update(parent = self)
        if _node is not None:
            self.children.append(_node)
        return self

    def add_sibling(self, _node, *args, **kwargs):
        if self.parent is None:
            raise ValueError("No parent node")
        self.parent.add_child(_node, *args, **kwargs)
        return self

    @staticmethod
    def _add_children(parent, *nodes):
        for node in nodes:
            parent.add_child(node)

    def add_children(self, *nodes):
        self._add_children(self, *nodes)
        return self

    def add_siblings(self, *nodes):
        if self.parent is None:
            raise ValueError("No parent node")
        self._add_children(self.parent, *nodes)
        return self

    def add_attr(self, name, value = None):
        if value is None:
            self.args = self.args + (name,)
        else:
            self.kwargs[name] = value
        return self

    def add_attrs(self, *args, **kwargs):
        self.args = self.args + args
        self.kwargs.update(kwargs)
        return self

    def __str__(self):
        return self.node.format(
                args = self.args,
                kwargs = self.kwargs,
                content = "".join(map(str, self.children))
        )

    def __repr__(self):
        return f"Builder({self.node}, args = {self.args}, kwargs = {self.kwargs}, children = {self.children})"


class Node(
        NamedTuple(
                "BaseNode",
                [
                        ("tag", str),
                        ("leading", str),
                        ("trailing", str),
                        ("use_trailing_tag", bool),
                ],
        ),
        Enum,
):
    # abstract Node enum, used to represent nodes in the tree
    def format(self, args, content, kwargs):
        raise NotImplementedError

    @staticmethod
    def get(tag_name):
        for member in (member for subclass in Node.__subclasses__() for member in subclass):
            if member.name == tag_name or member.tag == tag_name:
                return member


class NodeDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __init__(self, tag_name, *args, **kwargs):
        self.tag_name = tag_name
        self.args = args
        self.kwargs = kwargs

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.setdefault(
                self.name,
                Builder(
                        Node.get(self.tag_name),
                        *self.args,
                        **self.kwargs
                )
        )

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError("Cannot set class attribute")
        parent = instance.__dict__.setdefault(
                self.name,
                Builder(
                        Node.get(self.tag_name),
                        *self.args,
                        **self.kwargs)
        )
        if isinstance(value, (tuple, list)):
            parent.add_children(*value)
        else:
            parent.add_child(value)

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute")

    def add_attr(self, name, value = None):
        if value is None:
            self.args = self.args + (name,)
        else:
            self.kwargs[name] = value
        return self

    def add_attrs(self, *args, **kwargs):
        self.args = self.args + args
        self.kwargs.update(kwargs)
        return self

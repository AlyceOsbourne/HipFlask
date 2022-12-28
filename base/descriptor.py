from .nodes import Node
from .builder import NodeBuilder


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
                NodeBuilder(
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
                NodeBuilder(
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

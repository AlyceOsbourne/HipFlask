from .nodes import BaseNode


class Node:
    def __init__(
            self,
            tag_name,
            *args,
            children = None,
            parent = None,
            class_ = None,
            id_ = None,
            **kwargs,
    ):
        self.node = tag_name if isinstance(tag_name, BaseNode) else BaseNode.get(tag_name)
        self.args = list(args) if args else []
        self.kwargs = kwargs or dict()
        if class_ is not None:
            self.kwargs["class"] = class_
        if id_ is not None:
            self.kwargs["id"] = id_
        self.children = children or list()
        self.parent = parent

    def _append(self, _node, *args, **kwargs):
        if isinstance(_node, str):
            try:
                _node = Node(BaseNode.get(_node), *args, **kwargs)
            except ValueError:
                pass
        if isinstance(_node, Node):
            _node.__dict__.update(parent = self)
        self.children.append(_node)
        return _node

    def append(self, _node, *args, **kwargs):
        self._append(_node, *args, **kwargs)
        return self

    def add(self, _node, *args, **kwargs):
        return self._append(_node, *args, **kwargs)

    def extend(self, *nodes):
        for node in nodes:
            self.append(node)

    def add_attrs(self, *args, **kwargs):
        self.args.extend(args)
        self.kwargs.update(kwargs)
        return self

    def __str__(self):
        return self.node.format(
                args = self.args,
                kwargs = self.kwargs,
                content = "".join(map(str, (child for child in self.children if child is not None))),
        )

    def __repr__(self):
        return f"Node({self.node}, args = {self.args}, kwargs = {self.kwargs}, children = {self.children})"

    def traverse(self, include_self = True):
        if include_self:
            yield self
        for child in self.children:
            if hasattr(child, "traverse"):
                yield from child.traverse()



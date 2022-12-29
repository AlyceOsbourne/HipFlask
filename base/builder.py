from .nodes import BaseNode


class Node:
    def __init__(
            self,
            tag_name,
            *args,
            children = None,
            parent = None,
            _class = None,
            _id = None,
            **kwargs,
    ):
        self.node = tag_name if isinstance(tag_name, BaseNode) else BaseNode.get(tag_name)
        self.args = list(args) if args else []
        self.kwargs = kwargs or dict()
        if _class is not None:
            self.kwargs["class"] = _class
        if _id is not None:
            self.kwargs["id"] = _id
        self.children = children or list()
        self.parent = parent

    def append(self, _node, *args, **kwargs):
        if isinstance(_node, str):
            try:
                _node = Node(BaseNode.get(_node), *args, **kwargs)
            except ValueError:
                pass
        if isinstance(_node, Node):
            _node.__dict__.update(parent = self)
        self.children.append(_node)
        return self

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
                content = "".join(map(str, self.children))
        )

    def __repr__(self):
        return f"Node({self.node}, args = {self.args}, kwargs = {self.kwargs}, children = {self.children})"

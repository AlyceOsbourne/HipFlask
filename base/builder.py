from base import Node


class NodeBuilder:
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
                _node = NodeBuilder(Node.get(_node), *args, **kwargs)
            except ValueError:
                pass
        if isinstance(_node, NodeBuilder):
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
        return f"NodeBuilder({self.node}, args = {self.args}, kwargs = {self.kwargs}, children = {self.children})"


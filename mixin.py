from functools import wraps

from base import Builder, Node, NodeDescriptor


def _mixin_find_parent(value: "Builder"):
    if hasattr(value, "parent"):
        while value.parent is not None:
            value = value.parent
        return value
    return None


def _mixin_link_parents_deco(cls__init__):
    # makes the annotations work, and adds the children to the tree, used by the mixin
    @wraps(cls__init__)
    def wrapper(self, *args, **kwargs):
        for name, value in self.__annotations__.items():
            if isinstance(value, str) and hasattr(self, value):
                getattr(self, value).add_child(getattr(self, name))
        cls__init__(self, *args, **kwargs)

    return wrapper


def _mixin_init(self, **kwargs):
    # Dynamically created __init__ function to be applied to the class, created by the mixin.
    # Allows simple adding of children through naming convention.
    # You can add a child by prepending the name with the name of the parent with an underscore
    # example:
    # class HTML:
    #     root = node("DocType", is_class_node = True)
    #
    # page = HTML(
    #   root_head = node("head"),
    #   head_title = node("title"),
    #   head_meta = node("meta", charset = "utf-8"),
    # )
    #
    # this is for lazy throwing together of simple pages, and is not recommended for complex pages
    # when making more complex pages, use the node descriptor and the init to add children
    for name, value in kwargs.items():
        if isinstance(value, Node):
            value = Builder(value)
        if hasattr(self, name):
            setattr(self, name, value)
        else:
            while (_name := name).count("_") > 0:
                _name = _name[: _name.rfind("_")]
                if hasattr(self, _name):
                    if isinstance(value, (tuple, list)):
                        getattr(self, _name).add_children(*value)
                    else:
                        getattr(self, _name).add_child(value)
                    setattr(self, name[len(_name) + 1:], value)
                    break
            else:
                raise AttributeError(f"Unknown attribute {name}")


def _mixin_str(self):
    # dynamic str that searches for the root node, and then returns its str, created by the mixin
    # assumes that the class is properly annotated, hopes for a node called 'root,
    # falls back searches the instance, then the class for the first node, and then goes up the tree
    # until it finds a node with no parent, if not on instance, searches for descriptors on the class,
    # and gets the appropriate builder, else, raise an error
    root = None
    if hasattr(self, "root"):
        root = self.root

    if not root:
        for name, value in self.__dict__.items():
            if hasattr(value, "parent"):
                root = _mixin_find_parent(value)
                break

    if not root:
        for name, value in self.__class__.__dict__.items():
            if isinstance(value, NodeDescriptor):
                root = _mixin_find_parent(value.__get__(self, self.__class__))
                break

    if not root:
        raise ValueError("Root node not found")
    # return BeautifulSoup(str(root), "html.parser").prettify()
    return str(root)


class NodeMixin:
    def __init_subclass__(
            cls,
            init = True,
            string = True,
            **kwargs
    ):
        super().__init_subclass__(**kwargs)
        cls.__init__ = _mixin_link_parents_deco(cls.__init__ if not init else _mixin_init)
        if string:  cls.__str__ = _mixin_str


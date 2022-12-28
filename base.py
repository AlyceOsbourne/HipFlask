from collections import UserString
from enum import Enum
from functools import wraps
from typing import NamedTuple

from bs4 import BeautifulSoup


class Builder:
    def __init__(self, root, *args, children = None, parent = None, **kwargs, ):
        self.node = root
        self.args = args or tuple()
        self.kwargs = kwargs or dict()
        self.children = children or list()
        self.parent = parent

    def add_child(self, _node, *args, **kwargs):
        if isinstance(_node, str):
            try:
                _node = node(_node, *args, parent = self, **kwargs)
            except ValueError:
                pass
        if isinstance(_node, (Builder)):
            _node.__dict__.update(parent = self)
        if _node is not None:
            self.children.append(_node)
        return _node

    def add_sibling(self, _node, *args, **kwargs):
        if self.parent is None:
            raise ValueError("No parent node")
        return self.parent.add_child(_node, *args, **kwargs)

    @staticmethod
    def _add_children(parent, *nodes):
        for node in nodes:
            parent.add_child(node)

    def add_children(self, *nodes):
        self._add_children(self, *nodes)

    def add_siblings(self, *nodes):
        if self.parent is None:
            raise ValueError("No parent node")
        self._add_children(self.parent, *nodes)

    def __str__(self):
        return self.node.format(
                self.args, "".join(map(str, self.children)), self.kwargs
        )

    def __repr__(self):
        return f"Builder({self.node}, args = {self.args}, kwargs = {self.kwargs}, children = {self.children})"


class Node(NamedTuple(
        "BaseNode",
        [
                ("tag", str),
                ("leading", str),
                ("trailing", str),
                ("use_trailing_tag", bool),
        ],
), Enum):

    def format(self, args, content, kwargs):
        raise NotImplementedError


class NodeMixin:
    def __init_subclass__(cls, init = True, string = True, **kwargs):
        super().__init_subclass__(**kwargs)

        def __str__(self):
            for key, value in self.__dict__.items():
                if hasattr(value, "parent"):
                    if value.parent is None:
                        return BeautifulSoup(str(value), "html.parser").prettify()
            else:
                return "No Root Node"

        def wrap_init(init):
            @wraps(init)
            def wrapper(self, *args, **kwargs):
                for name, value in self.__annotations__.items():
                    if isinstance(value, str) and hasattr(self, value):
                        getattr(self, value).add_child(getattr(self, name))
                init(self, *args, **kwargs)

            return wrapper

        def __init__(self, **kwargs):
            for name, value in kwargs.items():
                if hasattr(self, name):
                    setattr(self, name, value)
                else:
                    while (_name := name).count("_") > 0:
                        _name = _name[:_name.rfind("_")]
                        if hasattr(self, _name):
                            if isinstance(value, (tuple, list)):
                                getattr(self, _name).add_children(*value)
                            else:
                                getattr(self, _name).add_child(value)
                            setattr(self, name, value)
                            break
                    else:
                        raise AttributeError(f"Unknown attribute {name}")

        cls.__init__ = wrap_init(cls.__init__ if not init else __init__)
        if string:
            cls.__str__ = __str__


class NodeDescriptor:
    def __init__(self, tag_name, *args, **kwargs):
        self.name = tag_name
        self.args = args
        self.kwargs = kwargs

    def __get__(self, instance, owner):
        if instance is None:
            return owner
        return instance.__dict__.setdefault(self.name, node(self.name, *self.args, **self.kwargs))

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError("Cannot set class attribute")
        parent = instance.__dict__.setdefault(self.name, node(self.name, *self.args, **self.kwargs))
        if isinstance(value, tuple):
            parent.add_children(*value)
        else:
            parent.add_child(value)

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute")


class _HTMLNode(Node):
    @staticmethod
    def create_html_node(tag: str, use_end_tag: bool = True):
        return tag, "<{tag}{attributes}>", "</{tag}>", use_end_tag

    DocType = create_html_node("!DOCTYPE html", False)
    Html = create_html_node("html")
    Head = create_html_node("head")

    # common head nodes
    Title = create_html_node("title")
    Meta = create_html_node("meta", False)
    Link = create_html_node("link", False)
    Style = create_html_node("style")
    StyleSheet = create_html_node("link", False)

    # common body nodes
    Body = create_html_node("body")
    Div = create_html_node("div")
    Span = create_html_node("span")
    P = create_html_node("p")
    H1 = create_html_node("h1")
    H2 = create_html_node("h2")
    H3 = create_html_node("h3")
    H4 = create_html_node("h4")
    H5 = create_html_node("h5")
    H6 = create_html_node("h6")
    Header = create_html_node("header")
    Footer = create_html_node("footer")
    A = create_html_node("a")
    Br = create_html_node("br", False)
    Nav = create_html_node("nav")

    # common form nodes
    Form = create_html_node("form")
    Input = create_html_node("input", False)
    Label = create_html_node("label")
    Button = create_html_node("button")
    Select = create_html_node("select")
    Option = create_html_node("option")
    TextArea = create_html_node("textarea")
    FieldSet = create_html_node("fieldset")
    Legend = create_html_node("legend")

    # common table nodes
    Table = create_html_node("table")
    THead = create_html_node("thead")
    TBody = create_html_node("tbody")
    TFoot = create_html_node("tfoot")
    TR = create_html_node("tr")
    TH = create_html_node("th")
    TD = create_html_node("td")
    Caption = create_html_node("caption")
    Col = create_html_node("col")
    ColGroup = create_html_node("colgroup")
    TableSection = create_html_node("tablesection")
    TableRow = create_html_node("tablerow")
    TableCell = create_html_node("tablecell")

    # common list nodes
    UL = create_html_node("ul")
    OL = create_html_node("ol")
    LI = create_html_node("li")
    DL = create_html_node("dl")
    DT = create_html_node("dt")
    DD = create_html_node("dd")
    Menu = create_html_node("menu")
    Menuitem = create_html_node("menuitem")
    Dir = create_html_node("dir")

    # common media nodes
    Audio = create_html_node("audio")
    Video = create_html_node("video")
    Source = create_html_node("source", False)
    Track = create_html_node("track", False)
    Canvas = create_html_node("canvas")
    Embed = create_html_node("embed", False)
    Object = create_html_node("object")
    Param = create_html_node("param", False)
    Picture = create_html_node("picture")
    Figure = create_html_node("figure")
    FigCaption = create_html_node("figcaption")
    Img = create_html_node("img", False)
    IFrame = create_html_node("iframe")
    NoScript = create_html_node("noscript")
    Script = create_html_node("script")

    def format(self, args, content, kwargs):
        attributes = (" " if args or kwargs else "") + " ".join(args) + " ".join(f"{k}={v}" for k, v in kwargs.items())

        try:
            leading = self.leading.format(tag = self.tag, attributes = attributes)
        except KeyError:
            leading = self.leading.format(tag = self.tag)

        trailing = self.trailing.format(tag = self.tag) if self.use_trailing_tag else ""

        return f"{leading}{content}{trailing}"


class _JinjaNode(Node):
    Block = "block", "{% block {attributes} %}", "{% endblock {attributes} %}", True
    Include = "include", "{% include {attributes} %}", "", False
    Extends = "extends", "{% extends {attributes} %}", "", False
    For = "for", "{% for {attributes} %}", "{% endfor %}", True
    If = "if", "{% if {attributes} %}", "{% endif %}", True
    Elif = "elif", "{% elif {attributes} %}", "", False
    Else = "else", "{% else %}", "", False
    Set = "set", "{% set {attributes} %}", "", False
    With = "with", "{% with {attributes} %}", "{% endwith %}", True
    Macro = "macro", "{% macro {attributes} %}", "{% endmacro %}", True
    Call = "call", "{% call {attributes} %}", "{% endcall %}", True

    def format(self, *args, content, **kwargs):
        attributes = ""
        attributes += " ".join(args)
        attributes += " ".join(f"{key}={value}" for key, value in kwargs.items())
        leading = self.leading.replace("{attributes}", attributes)
        trailing = (
                self.trailing.replace("{attributes}", attributes)
                if self.use_trailing_tag
                else ""
        )
        return f"{leading}{content}{trailing}"


def document(cls):
    return type(cls.__name__, (cls, NodeMixin), {})


def node(tag_name, *args, is_class_node = False, **kwargs):
    if is_class_node:
        return NodeDescriptor(tag_name, *args, **kwargs)
    for member in [member for subclass in Node.__subclasses__() for member in subclass]:
        if member.name == tag_name or member.tag == tag_name:
            return Builder(member, *args, **kwargs)
    raise ValueError(f"Node {tag_name} not found")

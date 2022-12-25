from flask_orm import HTMLTag, JinjaBlock, JinjaInclude, JinjaExtends
from functools import partial


def make_tag_class(tag, **kwargs):
    return type(
            tag,
            (HTMLTag,),
            {
                    "__init__": lambda self, **_kwargs: HTMLTag.__init__(
                            self, tag, **kwargs, **_kwargs
                    )
            },
    )


def make_block_class(tag, **kwargs):
    return type(
            tag,
            (JinjaBlock,),
            {
                    "__init__": lambda self, **_kwargs: JinjaBlock.__init__(
                            self, tag, **kwargs, **_kwargs
                    )
            },
    )


def make_include_class(tag, **kwargs):
    return type(
            tag,
            (JinjaInclude,),
            {
                    "__init__": lambda self, **_kwargs: JinjaInclude.__init__(
                            self, tag, **kwargs, **_kwargs
                    )
            },
    )


def make_extends_class(tag, **kwargs):
    return type(
            tag,
            (JinjaExtends,),
            {
                    "__init__": lambda self, **_kwargs: JinjaExtends.__init__(
                            self, tag, **kwargs, **_kwargs
                    )
            },
    )


Root = make_tag_class("!DOCTYPE html", uses_end_tag = False)
Html = make_tag_class("html")
Head = make_tag_class("head")
Body = make_tag_class("body")
Title = make_tag_class("title")
Meta = make_tag_class("meta", uses_end_tag = False)
Link = make_tag_class("link", uses_end_tag = False)
Script = make_tag_class("script")
Style = make_tag_class("style")
StyleSheet = make_tag_class("link", uses_end_tag = False, rel = "stylesheet")
Div = make_tag_class("div")
Span = make_tag_class("span")
P = make_tag_class("p")
H1 = make_tag_class("h1")
H2 = make_tag_class("h2")
H3 = make_tag_class("h3")
H4 = make_tag_class("h4")
H5 = make_tag_class("h5")
H6 = make_tag_class("h6")
A = make_tag_class("a")
Img = make_tag_class("img", uses_end_tag = False)
Ul = make_tag_class("ul")
Ol = make_tag_class("ol")
Li = make_tag_class("li")
Footer = make_tag_class("footer")
Header = make_tag_class("header")
Main = make_tag_class("main")
Nav = make_tag_class("nav")
Section = make_tag_class("section")
Article = make_tag_class("article")
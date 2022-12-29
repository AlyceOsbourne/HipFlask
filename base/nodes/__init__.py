from .base_node import BaseNode


class HTMLNode(BaseNode):
    @staticmethod
    def create_html_node(tag: str, use_end_tag: bool = True):
        # cause who wants to rewrite these every time
        return tag, "<{tag}{attributes}>", "</{tag}>", use_end_tag

    def format(self, args, content, kwargs):
        attributes = (
                (" " if args or kwargs else "")
                + " ".join(args)
                + " ".join(f"{k}={v}" for k, v in kwargs.items())
        )

        try:
            leading = self.leading.format(tag = self.tag, attributes = attributes)
        except KeyError:
            leading = self.leading.format(tag = self.tag)

        trailing = self.trailing.format(tag = self.tag) if self.use_trailing_tag else ""

        return f"{leading}{content}{trailing}"

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


class JinjaNode(BaseNode):

    def format(self, args, content, kwargs):
        start_tag = "{% "
        end_tag = " %}"

        attributes = (
                " ".join(args)
                + " ".join(f"{k}={v}" for k, v in kwargs.items())
        )

        leading = self.leading.format(attributes = attributes)
        try:
            trailing = self.trailing.format(attributes = attributes)
        except KeyError:
            trailing = self.trailing
        leading = start_tag + leading + end_tag
        trailing = start_tag + trailing + end_tag
        return f"{leading}{content}{trailing if self.use_trailing_tag else ''}"

    Includes = "include", "include '{attributes}'", "", False
    Extends = "extends", "extends '{attributes}'", "", False
    Block = "block", "block {attributes}", "endblock {attributes}", True

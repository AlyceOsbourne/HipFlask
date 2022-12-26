from flask_orm import HTMLTag, make_tag_class

Root = make_tag_class("!DOCTYPE html")
Html = make_tag_class("html")
Head = make_tag_class("head")
Body = make_tag_class("body")

# common head tags
Title = make_tag_class("title")
Meta = make_tag_class("meta")
Style = make_tag_class("style")
StyleSheet = make_tag_class("link", rel = "stylesheet")
Script = make_tag_class("script")

# common body tags
Nav = make_tag_class("nav")
Ul = make_tag_class("ul")
Li = make_tag_class("li")
A = make_tag_class("a")
Div = make_tag_class("div")
Span = make_tag_class("span")
P = make_tag_class("p")
H1 = make_tag_class("h1")
H2 = make_tag_class("h2")
H3 = make_tag_class("h3")
H4 = make_tag_class("h4")
H5 = make_tag_class("h5")
H6 = make_tag_class("h6")
Img = make_tag_class("img", src = "#")
Table = make_tag_class("table")
Tr = make_tag_class("tr")
Th = make_tag_class("th")
Td = make_tag_class("td")
Form = make_tag_class("form", method = "post")
Input = make_tag_class("input", type = "text")
Button = make_tag_class("button", type = "submit")
Label = make_tag_class("label")
Select = make_tag_class("select")
Option = make_tag_class("option")
Textarea = make_tag_class("textarea")
I = make_tag_class("i")
Br = make_tag_class("br")
Hr = make_tag_class("hr")
Footer = make_tag_class("footer")





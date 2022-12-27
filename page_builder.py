from base import document, node, class_node

@document
class HTML:
    root = class_node("html")
    head: "root" = class_node("head")
    body: "root" = class_node("body")
    title: "head" = class_node("title")


html = HTML()
html.title = "Hello World"
print(html)
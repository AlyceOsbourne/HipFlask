from base import document, node


@document
class HTML:
    root = node("DocType", is_class_node = True)
    html: "root" = node("html", is_class_node = True)

    head: "html" = node("head", is_class_node = True)
    body: "html" = node("body", is_class_node = True)

    title: "head" = node("title", is_class_node = True)


print(HTML())

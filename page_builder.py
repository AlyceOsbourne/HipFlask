from base import document, node


@document
class HTML:
    root = node("DocType", is_class_node = True)
    html: "root" = node("html", is_class_node = True)
    head: "html" = node("head", is_class_node = True)
    body: "html" = node("body", is_class_node = True)
    head_block: "head" = node("block", "head", is_class_node = True)
    body_block: "body" = node("block", "body", is_class_node = True)


if __name__ == "__main__":
    html = HTML()
    print(html)

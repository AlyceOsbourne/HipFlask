from base import node, document


@document(init = False)
class SimpleNavBar:
    root = node(
            "nav",
            is_class_node = True,
            _class = "navbar navbar-expand-lg navbar-light bg-light",
    )
    list: "root" = node("ul", is_class_node = True, _class = "navbar-nav mr-auto")

    def __init__(self, **items):
        self.list + [
                node(
                        "li",
                        _class = "nav-item",
                )
                + (
                        node(
                                "a",
                                href = href,
                                _class = "nav-link",
                        )
                        + text
                )
                for text, href in items.items()
        ]


__all__ = ["SimpleNavBar"]

if __name__ == "__main__":
    @document
    class Example:
        root = node("DocType", is_class_node = True)
        html: "root" = node("html", is_class_node = True)
        head: "html" = node("head", is_class_node = True)
        title: "head" = node("title", is_class_node = True)
        body: "html" = node("body", is_class_node = True)


    print(Example(
            title = "Example",
            body_nav = SimpleNavBar(
                    Home = "/",
                    About = "/about",
                    Contact = "/contact",
            ),
    ))

from base import *

__all__ = ["node", "document"]

if __name__ != "__main__":
    print(
            "Thanks for using HipFlask! Please report any bugs here: https://github.com/AlyceOsbourne/HipFlask/issues"
    )

else:

    @document
    class ExampleSite:
        doc_type = node("DocType")
        html: "doc_type" = node("html")
        head: "html" = node("head")
        title: "head" = node("title")
        body: "html" = node("body")

    print(ExampleSite())
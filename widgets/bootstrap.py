from base import Node


def bootstrap_css():
    return Node(
            "link",
            rel = "stylesheet",
            href = "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
            integrity = "sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
            crossorigin = "anonymous",
    )


def bootstrap_js():
    (
            Node(
                    "script",
                    src = "https://code.jquery.com/jquery-3.3.1.slim.min.js",
                    integrity = "sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
                    crossorigin = "anonymous",
            ),
            Node(
                    "script",
                    src = "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js",
                    integrity = "sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1",
                    crossorigin = "anonymous",
            ),
            Node(
                    "script",
                    src = "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js",
                    integrity = "sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM",
                    crossorigin = "anonymous",
            ),
    )


def bootstrap():
    return bootstrap_css(), bootstrap_js()


__all__ = 'bootstrap', 'bootstrap_css', 'bootstrap_js'

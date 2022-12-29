from enum import Enum
from functools import cache
from typing import NamedTuple


class BaseNode(
        NamedTuple(
                "BaseNode",
                [
                        ("tag", str),
                        ("leading", str),
                        ("trailing", str),
                        ("use_trailing_tag", bool),
                ],
        ),
        Enum,
):
    # abstract Node enum, used to represent nodes in the tree
    def format(self, args, content, kwargs):
        # we must implement this method, this structures the node so we can create a tree from it
        raise NotImplementedError

    @staticmethod
    @cache
    def get(tag_name):
        # we are caching the lookup as there are some 130~ nodes just between html and jinja2
        # and we don't want to have to do a linear search every time
        # on average users will use about 30 of these nodes
        for member in (member for subclass in BaseNode.__subclasses__() for member in subclass):
            if member.name == tag_name or member.tag == tag_name:
                return member
        raise ValueError(f"Invalid tag name: {tag_name}")

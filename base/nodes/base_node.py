from enum import Enum
from typing import NamedTuple


class Node(
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
        raise NotImplementedError

    @staticmethod
    def get(tag_name):
        for member in (member for subclass in Node.__subclasses__() for member in subclass):
            if member.name == tag_name or member.tag == tag_name:
                return member

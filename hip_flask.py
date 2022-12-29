from base import Node, ClassNode, Widget
from base.widget import get_widgets as _get_widgets


def init(target):
    if hasattr(target, 'jinja_env'):
        target = target.jinja_env  # is flask, get jinja environment
    target.globals.update(_get_widgets())  # add widgets to jinja environment


__all__ = 'Node', 'ClassNode', 'Widget',

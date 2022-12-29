from base import Node, ClassNode, Widget
from base.widget import get_widgets as _get_widgets


def init_env(env):
    # add to pure jinja2
    env.globals.update(_get_widgets())


def init_app(self, app):
    # add to flask
    init_env(app.jinja_env)


__all__ = 'init_env', 'init_app', 'Node', 'ClassNode', 'Widget',



from .nodes import BaseNode
from .builder import Node
from .descriptor import ClassNode
from .widget import Widget

# the Node represents nodes in the html tree
# the NodeDescriptor is a descriptor simple class definitions, similar to dataclass fields
# the Widget is a base class for widgets, which are html templates

__all__ = 'Node', 'ClassNode', 'Widget'









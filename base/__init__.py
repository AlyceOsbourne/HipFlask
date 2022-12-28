from .nodes import Node
from .builder import NodeBuilder
from .descriptor import NodeDescriptor
from .document_builder import document_init, document_string, link_document_nodes


def node(tag_name, *args, is_class_node = False, **kwargs):
    if is_class_node:
        return NodeDescriptor(tag_name, *args, **kwargs)
    return NodeBuilder(tag_name, *args, **kwargs)


def document(cls, /, init = True, link_annotations = True, string = True):
    if string:  cls.__str__ = document_string
    if init: cls.__init__ = document_init
    if link_annotations: cls.__init__ = link_document_nodes(cls.__init__)
    return cls


__all__ = ['node', 'document']

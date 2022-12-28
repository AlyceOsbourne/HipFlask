from .nodes import Node
from .builder import NodeBuilder
from .descriptor import NodeDescriptor
from .document_builder import document_init, document_string, wrap_init

def node(tag_name, *args, is_class_node = False, **kwargs):
    if "_class" in kwargs:
        kwargs["class"] = kwargs.pop("_class")
    if is_class_node:
        return NodeDescriptor(tag_name, *args, **kwargs)
    return NodeBuilder(tag_name, *args, **kwargs)


def document(cls = None, /,
             init = True,
             link_annotations = True,
             string = True,
             ):
    if cls is None:
        return lambda _cls: document(_cls, init = init, link_annotations = link_annotations, string = string)
    if string:  cls.__str__ = document_string
    if init: cls.__init__ = document_init
    if link_annotations and hasattr(cls, "__annotations__"): cls.__init__ = wrap_init(cls.__init__)
    return cls


__all__ = ['node', 'document']



from enum import Enum
from htmlnode import LeafNode,HTMLNode
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, content,type:TextType, url=None):
        self.text = content
        self.text_type = type
        self.url = url
    def __eq__(self, node):
        return( self.text == node.text and self.text_type == node.text_type and self.url == node.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node:TextNode):

   match text_node.text_type:
       case TextType.TEXT:
            leaf = LeafNode(None, text_node.text)
            return leaf
       case TextType.BOLD:
            leaf = LeafNode("b", text_node.text)
            return leaf
       case TextType.ITALIC:
            leaf = LeafNode("i", text_node.text)
            return leaf
       case TextType.CODE:
            leaf = LeafNode("c", text_node.text)
            return leaf
       case TextType.LINK:
            leaf = LeafNode("a", text_node.text,text_node.url)
            return leaf
       case TextType.IMAGE:
            leaf = LeafNode("img", text_node.text, text_node.url)
            return leaf
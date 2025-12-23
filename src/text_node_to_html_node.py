from textnode import TextNode, TextType
from htmlnode import LeafNode, NonClosingLeafNode

def text_node_to_html_node(text_node: TextNode):
    """
    Convert a TextNode to an HTML LeafNode.
    """
    if ((text_node.text is None) or (text_node.text == "")):
        raise ValueError("TextNode must have text to convert to HTMLNode.")
    
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            if ((text_node.url is None) or (text_node.url == "")):
                raise ValueError("TextNode of type LINK must have a URL.")
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            if ((text_node.url is None) or (text_node.url == "")):
                raise ValueError("TextNode of type IMAGE must have a URL.")
            return NonClosingLeafNode(tag="img", props={"src": text_node.url, "alt": text_node.text})
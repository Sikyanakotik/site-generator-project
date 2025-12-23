import unittest

from textnode import TextNode, TextType
from text_node_to_html_node import text_node_to_html_node
from htmlnode import LeafNode, NonClosingLeafNode
from split_nodes_delimiter import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different(self):
        node1 = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a different text node", TextType.BOLD, None)
        node3 = TextNode("This is a text node", TextType.ITALIC, None)
        node4 = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)
        
    def test_repr(self):
        node = TextNode("Sample", TextType.LINK, "http://example.com")
        expected_repr = "TextNode(Sample, TextType.LINK, http://example.com)"
        self.assertEqual(repr(node), expected_repr)

    def test_defaults(self):
        node1 = TextNode("Default test")
        node2 = TextNode("Default test", TextType.PLAIN, None)
        self.assertEqual(node1, node2)
        
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_bold_to_html(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic_to_html(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_code_to_html(self):
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")
        self.assertEqual(html_node.to_html(), "<code>Code snippet</code>")

    def test_link_to_html(self):
        node = TextNode("Example", TextType.LINK, "http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Example")
        self.assertEqual(html_node.props, {"href": "http://example.com"})
        self.assertEqual(html_node.to_html(), '<a href="http://example.com">Example</a>')

    def test_image_to_html(self):
        node = TextNode("An image", TextType.IMAGE, "http://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, NonClosingLeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "http://example.com/image.png", "alt": "An image"})
        self.assertEqual(html_node.to_html(), '<img src="http://example.com/image.png" alt="An image" />')

    def test_split_nodes_delimiter(self):
        nodes = [
            TextNode("Hello, world. _Here I come!_", TextType.PLAIN),
        ]
        delimiter = "_"
        split_nodes = split_nodes_delimiter(nodes, delimiter, TextType.ITALIC)
        expected_splits = [
            TextNode("Hello, world. ", TextType.PLAIN),
            TextNode("Here I come!", TextType.ITALIC),
        ]
        self.assertEqual(split_nodes, expected_splits)

    def test_split_nodes_on_starting_delimiter(self):
        nodes = [
            TextNode("_Start with italic_ and then plain.", TextType.PLAIN),
        ]
        delimiter = "_"
        split_nodes = split_nodes_delimiter(nodes, delimiter, TextType.ITALIC)
        expected_splits = [
            TextNode("Start with italic", TextType.ITALIC),
            TextNode(" and then plain.", TextType.PLAIN),
        ]
        self.assertEqual(split_nodes, expected_splits)

    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("Mixing _italic_ and _more italics_ here.", TextType.PLAIN),
        ]
        delimiter = "_"
        split_nodes = split_nodes_delimiter(nodes, delimiter, TextType.ITALIC)
        expected_splits = [
            TextNode("Mixing ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.PLAIN),
            TextNode("more italics", TextType.ITALIC),
            TextNode(" here.", TextType.PLAIN),
        ]
        self.assertEqual(split_nodes, expected_splits)

    def test_split_no_delimiter(self):
        nodes = [
            TextNode("No delimiters here.", TextType.PLAIN),
        ]
        delimiter = "_"
        split_nodes = split_nodes_delimiter(nodes, delimiter, TextType.ITALIC)
        expected_splits = [
            TextNode("No delimiters here.", TextType.PLAIN),
        ]
        self.assertEqual(split_nodes, expected_splits)

    def text_split_bold_and_italic(self):
        nodes = [
            TextNode("This is _italic_ and this is *bold*.", TextType.PLAIN),
        ]
        delimiter_italic = "_"
        delimiter_bold = "*"
        split_italic = split_nodes_delimiter(nodes, delimiter_italic, TextType.ITALIC)
        split_bold = split_nodes_delimiter(split_italic, delimiter_bold, TextType.BOLD)
        expected_splits = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and this is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertEqual(split_bold, expected_splits)

    def test_split_unmatched_delimiter(self):
        nodes = [
            TextNode("This is _unmatched italic.", TextType.PLAIN),
        ]
        delimiter = "_"
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, delimiter, TextType.ITALIC)

if __name__ == "__main__":
    unittest.main()
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, NonClosingLeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        expected_html = 'class="container" id="main"'
        self.assertEqual(node.props_to_html(), expected_html)

    def test_props_to_html_none(self):
        node = HTMLNode(tag="div", props=None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", children=None, props={"style": "color:red"})
        expected_repr = "HTMLNode(p, Hello, None, {'style': 'color:red'})"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_with_children(self):
        child1 = HTMLNode(tag="span", value="Child1")
        child2 = HTMLNode(tag="span", value="Child2")
        node = HTMLNode(tag="div", value=None, children=[child1, child2], props=None)
        expected_repr = f"HTMLNode(div, None, [{repr(child1)}, {repr(child2)}], None)"
        self.assertEqual(repr(node), expected_repr)

    def test_leaf_node_to_html(self):
        leaf = LeafNode(tag="p", value="This is a paragraph.", props={"class": "text"})
        expected_html = '<p class="text">This is a paragraph.</p>'
        self.assertEqual(leaf.to_html(), expected_html)

    def test_leaf_node_to_html_no_tag(self):
        leaf = LeafNode(tag=None, value="Just text", props=None)
        expected_html = "Just text"
        self.assertEqual(leaf.to_html(), expected_html)

    def test_leaf_node_to_html_no_value(self):
        leaf = LeafNode(tag="p", value=None, props=None)
        with self.assertRaises(ValueError):
            leaf.to_html()

    def test_leaf_node_to_html_no_props(self):
        leaf = LeafNode(tag="b", value="No props here", props=None)
        expected_html = "<b>No props here</b>"
        self.assertEqual(leaf.to_html(), expected_html)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_non_closing_leaf_node_to_html(self):
        non_closing_node = NonClosingLeafNode(tag="img", props={"src": "image.png", "alt": "An image"})
        expected_html = '<img src="image.png" alt="An image" />'
        self.assertEqual(non_closing_node.to_html(), expected_html)

    def test_non_closing_leaf_node_no_tag(self):
        with self.assertRaises(ValueError):
            NonClosingLeafNode(tag=None, props={"src": "image.png"})

    def test_parent_node_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_node_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_node_deep_children(self):
        grandchild1 = LeafNode("i", "grandchild1")
        grandchild2 = NonClosingLeafNode("img", props={"src": "pic.png"})
        child1 = ParentNode("span", [grandchild1, grandchild2])
        child2 = LeafNode("a", "child2")
        parent = ParentNode("div", [child1, child2])
        expected_html = "<div><span><i>grandchild1</i><img src=\"pic.png\" /></span><a>child2</a></div>"
        self.assertEqual(parent.to_html(), expected_html)

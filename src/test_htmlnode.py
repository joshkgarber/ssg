import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from textnode import TextNode
from textnode import TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "p",
            "the text inside a paragraph",
            None,
            {"class": "test"}
        )
        self.assertEqual(
            ' class="test"',
            node.props_to_html()
        )

    def test_props_to_html2(self):
        node = HTMLNode(
            "p",
            "the text inside a paragraph",
            None,
            {"class": "test", "id": "test"}
        )
        self.assertEqual(
            ' class="test" id="test"',
            node.props_to_html()
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "the text inside a paragraph",
            None,
            {"id": "test"}
        )
        self.assertEqual(
            'HTMLNode(tag="p", value="the text inside a paragraph", children=None, props={\'id\': \'test\'}',
            repr(node)
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")

    def test_empty_value(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_none_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as e:
            node.to_html()
        msg = str(e.exception)
        self.assertEqual(msg, "All leaf nodes must have a value")

    def test_props(self):
        node = LeafNode(
            "a",
            "Click Here!",
            {
                "href": "https://www.example.com",
                "target": "_blank",
                "class": "btn",
            },
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.example.com" target="_blank" class="btn">Click Here!</a>'
        )

    def test_no_tag(self):
        node = LeafNode(None, "Hello World")
        self.assertEqual(node.to_html(),"Hello World")

    def test_repr(self):
        node = LeafNode("span", "This is a span", {"id": "1"})
        self.assertEqual(
            repr(node),
            'LeafNode(tag="span", value="This is a span", props={\'id\': \'1\'})'
        )


class TestParentNode(unittest.TestCase):
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
        self.assertEqual(
            repr(parent_node),
            'ParentNode(tag="div", children=[ParentNode(tag="span", children=[LeafNode(tag="b", value="grandchild", props=None)], props=None)], props=None)'
        )

    def test_to_html_without_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()
        msg = str(e.exception)
        self.assertEqual(msg, "All parent nodes must have a tag")

    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()
        msg = str(e.exception)
        self.assertEqual(msg, "All parent nodes must have children")

    def test_to_html_span_in_p_with_props(self):
        text1 = LeafNode(None, "This is the first part of the paragraph, ")
        span_node = LeafNode("span", "this part is nested", {"id": "dk468", "class": "attention"})
        text2 = LeafNode(None, ", and this part isn't.")
        parent_node = ParentNode("p", [text1, span_node, text2], props={"id": "fa654", "class": "primary"})
        self.assertEqual(
            parent_node.to_html(),
            '<p id="fa654" class="primary">This is the first part of the paragraph, <span id="dk468" class="attention">this part is nested</span>, and this part isn\'t.</p>',
        )


if __name__ == "__main__":
    unittest.main()


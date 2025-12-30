import unittest

from htmlnode import HTMLNode,LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "hello world", [], {
    "href": "https://www.google.com",
    "target": "_blank",
})
        node2 = HTMLNode("p", "hello world", [], {
    "href": "https://www.google.com",
    "target": "_blank",
})
        self.assertEqual(node.tag, node2.tag)
    def test_repr(self):
        node = HTMLNode("p", "hello world", [], {
            "href": "https://www.google.com",
            "target": "_blank",}   )
        text = node.props_to_html()
        print(text)
        self.assertNotEqual(text, ' href=https://www.google.com target=_blank')
    def test_noteq(self):
        node = HTMLNode("p", "hello world", [], {
            "href": "https://www.google.com",
            "target": "_blank",}   )
        text = node.__repr__()
        self.assertEqual(text, "HTMLNODE: p, hello world, [], {'href': 'https://www.google.com', 'target': '_blank'}")
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_p2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=https://www.google.com>Click me!</a>")

if __name__ == "__main__":
    unittest.main()
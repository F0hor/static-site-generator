import unittest
from htmlnode import HTMLNode, LeafNode   

class TestHTMLNode(unittest.TestCase):
    def test_basic(self):
        node = HTMLNode('H1', 'This is headline')
        self.assertEqual(f"{node}", 'HTMLNode(H1, , This is headline, None)')

    def test_props(self):
        node = HTMLNode('a', 'This is link', prop={'href': 'www.boot.dev'})
        self.assertEqual(f'{node}', 'HTMLNode(a,  href="www.boot.dev", This is link, None)')


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode('a', 'Click me!', {'href': 'www.boot.dev'})
        self.assertEqual(node.to_html(), '<a href="www.boot.dev">Click me!</a>')


if __name__ == "__main__":
    unittest.main()

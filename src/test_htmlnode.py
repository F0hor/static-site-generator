import unittest
from htmlnode import HTMLNode   

class TestHTMLNode(unittest.TestCase):
    def test_basic(self):
        node = HTMLNode('H1', 'This is headline')
        self.assertEqual(f"{node}", 'HTMLNode(H1, , This is headline, None)')

    def test_props(self):
        node = HTMLNode('a', 'This is link', prop={'href': 'www.boot.dev'})
        self.assertEqual(f'{node}', 'HTMLNode(a,  href="www.boot.dev", This is link, None)')


if __name__ == "__main__":
    unittest.main()

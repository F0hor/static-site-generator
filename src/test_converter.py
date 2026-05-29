import unittest
import converter
from textnode import TextNode, TextType

class TestTextNodeToLeafNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        print(node)
        html_node = converter.text_node_to_html_node(node)
        print(html_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


class TestSplitNodesDelimeter(unittest.TestCase):
    def test_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = converter.split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)

        new_nodes = converter.split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

        new_nodes = converter.split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_closing_delimeter_missing(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("This is text with a code block` word", TextType.TEXT)
            new_nodes = converter.split_nodes_delimiter([node], "`", TextType.CODE),
        
        self.assertTrue("Invalid Markdown syntax" in str(context.exception))



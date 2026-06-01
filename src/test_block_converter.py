import unittest
import block_converter as converter
from textnode import TextNode, TextType, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = converter.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_whitespace(self):
        md = """
        This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line       

- This is a list
- with items
"""
        blocks = converter.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_empty_block(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = converter.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        
class TestBlocksToBlockTypes(unittest.TestCase):
    def test_heading(self):
        block = "# Heading"
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.HEADING
        )
    
    def test_heading2(self):
        block = "## Heading"
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.HEADING
        )
    
    def test_heading3(self):
        block = "### Heading"
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.HEADING
        )
    
    def test_heading4(self):
        block = "#### Heading"
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.HEADING
        )
    
    def test_heading5(self):
        block = "##### Heading"
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.HEADING
        )
    
    def test_heading6(self):
        block = "###### Heading"
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.HEADING
        )
    
    def test_heading7(self):
        block = "####### Heading"
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_heading_invalid(self):
        block = "#Heading"
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_code(self):
        block = """```
code
```"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.CODE
        )
    
    def test_code_missing_new_line(self):
        block = """```code
```"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_code_missing_tail(self):
        block = """```
code"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_code_few_backticks(self):
        block = """``
code
```"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_code_more_backticks(self):
        block = """````
code
```"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_quote(self):
        block = "> Quote here"
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.QUOTE
        )
    
    def test_quote1(self):
        block = ">Quote here"
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.QUOTE
        )
    
    def test_quote2(self):
        block = ">> Quote here"
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.QUOTE
        )
    
    def test_unordered_list(self):
        block = """- point
- second point
- point 3"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.UNLIST
        )
    
    def test_unordered_list_missing_dash(self):
        block = """ point
- second point
- point 3"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_unordered_list_missing_dash2(self):
        block = """- point
second point
- point 3"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_unordered_list_missing_space(self):
        block = """-point
- second point
- point 3"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_unordered_list_missing_space2(self):
        block = """- point
-second point
- point 3"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_unordered_list_empty_point(self):
        block = """- point
- second point
- point 3
-"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_unordered_list_empty_point2(self):
        block = """- point
-
- second point
- point 3"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_ordered_list(self):
        block = """1. point
2. second point
3. point 3"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.LIST
        )
    
    def test_ordered_list_not_start_with_one(self):
        block = """2. point
3. second point
4. point 3"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_ordered_list_wrong_increment(self):
        block = """1. point
3. second point
4. point 3"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_ordered_list_empty_line(self):
        block = """1. point

2. second point
3. point 3"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    
    def test_ordered_list_missing_space(self):
        block = """1.point
2. second point
3. point 3"""
        self.assertEqual(
            converter.block_to_block_type(block),
            BlockType.PARAGRAPH
        )


class TestMarkdownToHTLMNodes(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = converter.markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = converter.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


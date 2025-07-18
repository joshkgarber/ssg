import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_blocktype,
    BlockType,
)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
            markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(markdown)
            self.assertListEqual(
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items"
                ],
                blocks
            )


    def test_markdown_to_blocks_newlines(self):
        markdown = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
            ],
            blocks
        )


    def test_block_to_blocktype_p(self):
        block = "This is **bolded** paragraph"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)


    def test_block_to_blocktype_h(self):
        block = "# Title"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)


    def test_block_to_blocktype_code(self):
        block = "```py\nprint(\"hello world\")\n```"
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)


    def test_block_to_blocktype_quote(self):
        block = "> Whether you think you can\n> or you think you can't,\n> you're right."
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)


    def test_block_to_blocktype_ul(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_blocktype(block), BlockType.UL)


    def test_block_to_blocktype_ol(self):
        block = "1. item one\n2. item two\n3. item three"
        self.assertEqual(block_to_blocktype(block), BlockType.OL)


    def test_block_to_blocktype_ol_false(self):
        block = "1. item one\n3. item two\n4. item three"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()


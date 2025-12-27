import unittest

from blocks import BlockType, markdown_to_blocks, block_to_block_type
from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_extra_newlines(self):
        md = "  Whitespace is neat. \n\n\n\n\n\t\n\n Let's add a bunch!\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Whitespace is neat.", "Let's add a bunch!"]
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_btobt_paragraph(self):
        block = "I will devour you french fries."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_btobt_heading(self):
        good_blocks = [
            "# h1",
            "### h3",
            "###### h6"
        ]
        bad_blocks = [
            "Late #",
            "####### Too many!",
            "##No space"
            "#", # No text
        ]

        for block in good_blocks:
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        for block in bad_blocks:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_btobt_code(self):
        good_blocks = [
            "```\nprint('Hello, world!')\n```",
            "```for block in good_blocks:\n\tself.assertEqual(block_to_block_type(block), BlockType.CODE)```",
            "```\n> Don't quote me```",
            '``` ```',
        ]
        bad_blocks = [
            "`````", # 5 * '`'
            "``````",# 6 * '`'
        ]

        for block in good_blocks:
            self.assertEqual(block_to_block_type(block), BlockType.CODE)
        for block in bad_blocks:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_btobt_quote(self):
        good_blocks = [
            ">Greentext",
            "> What cursed spite\n> That I was ever born to set it right",
            ">",
            ">Help>How do I>Use this thing!?"
        ]
        bad_blocks = [
            "Luke\n> I am your father.",
            ">Yippee-ki-yay\nMother hubbard.",
            ">Now I have a machine gun\n>HO\nOH\n>HO",
            "\n>...we came in?",
        ]

        for block in good_blocks:
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        for block in bad_blocks:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_btobt_unordered(self):
        good_blocks = [
            "- Red\n- Yellow\n- Green",
            "- Buy milk",
            "- Twenty-three",
        ]
        bad_blocks = [
            "-Steal underpants",
            "- Eggs\n- Milk\nBattery acid",
            "- Bread\n-Baby\n- Bread",
            "- I forgor\n"
        ]

        for block in good_blocks:
            self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        for block in bad_blocks:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_btobt_ordered(self):
        good_blocks = [
            "1. is the loneliest number",
            "1. Nothing wrong with me\n2. Nothing wrong with me\n3. Nothing wrong with me\n4. Nothing wrong with me",
            "1. ", # The spec does no require anything after the space

        ]
        bad_blocks = [
            "0. Arrays start at 0\n 1. You silly goose!",
            "1. Steal underpants\n 3. Profit"
            "1.No space",
            "1. No space\n2.but later!",
            "1.", # It does, however, require the space
            "1. Wouldn't it be better\n2. to use one symbol\n4. number every time?\n3. instead of typing the",
            "2. Who needs 1?",
            "1. An honest mistake 2. But it needs to break \n3. For the program's sake",
        ]

        for block in good_blocks:
            self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        for block in bad_blocks:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
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

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_list_of_images_and_links(self):
        md = "- ![alt text](https://example.com/image.png)\n- [link text](https://example.com)"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><img src=\"https://example.com/image.png\" alt=\"alt text\" /></li><li><a href=\"https://example.com\">link text</a></li></ul></div>",
        )

    def test_ordered_list_of_images_and_links(self):
        md = "1. ![alt text](https://example.com/image.png)\n2. [link text](https://example.com)"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><img src=\"https://example.com/image.png\" alt=\"alt text\" /></li><li><a href=\"https://example.com\">link text</a></li></ol></div>",
        )

    def test_heading_and_quote(self):
        md = (
            "# First heading\n\n"
            + "## Second heading\n\n"
            + "### Third heading\n\n"
            + "#### Fourth heading\n\n"
            + "##### Fifth heading\n\n"
            + "###### Sixth heading\n\n"
            + "> Where are we heading anyway?"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>First heading</h1><h2>Second heading</h2><h3>Third heading</h3><h4>Fourth heading</h4><h5>Fifth heading</h5><h6>Sixth heading</h6><blockquote><p>Where are we heading anyway?</p></blockquote></div>",
        )
        
    def test_extract_title(self):
        md = "# I'm a little program\n# Short and stout\n# Here is my input\n# Here is my out."

        title = extract_title(md)
        self.assertEqual(title, "I'm a little program")

    def test_extract_title_none(self):
        md = ("This is not a title\n"
              + "#Neither is this\n"
              + "### Don't look at me\n"
              + "There is no # title here")
        
        with self.assertRaises(Exception):
            title = extract_title(md)

    def test_extract_title_late(self):
        md = ("Wait for it\n"
              + "#Waait for it\n"
              + "## Waaait for it\n"
              + "##Waaaait for it\n"
              + "# Now! ")
        
        title = extract_title(md)
        self.assertEqual(title, "Now!")
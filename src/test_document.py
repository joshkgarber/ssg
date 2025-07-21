import unittest
from document import markdown_to_html_node


class TestDocumentConversion(unittest.TestCase):
    def test_simple_heading(self):
        md = """
### Hello World
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Hello World</h3></div>"
        )


    def test_complex_heading(self):
        md = """
### Hello World with a [Link](https://example.com)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Hello World with a <a href=\"https://example.com\">Link</a></h3></div>"
        )


    def test_simple_paragraph(self):
        md = """
Hello World, my name is computer. Computers are machines.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Hello World, my name is computer. Computers are machines.</p></div>"
        )


    def test_two_paragraphs(self):
        md = """
Hello World, my name is computer. Computers are machines.

They are artificial.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Hello World, my name is computer. Computers are machines.</p><p>They are artificial.</p></div>"
        )


    def test_paragraph_broken_line(self):
        md = """
This paragraph
is broken over two lines.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This paragraph is broken over two lines.</p></div>"
        )


    def test_two_paragraphs_with_heading(self):
        md = """
# New Document

Hello World, my name is computer. Computers are machines.

They are artificial.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>New Document</h1><p>Hello World, my name is computer. Computers are machines.</p><p>They are artificial.</p></div>"
        )


    def test_two_paragraphs_with_formatting_and_heading(self):
        md = """
# New Document

Hello World, my name is **computer**. Computers are [machines](https://machines.com).

They are _artificial_.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>New Document</h1><p>Hello World, my name is <b>computer</b>. Computers are <a href=\"https://machines.com\">machines</a>.</p><p>They are <i>artificial</i>.</p></div>"
        )


    def test_simple_quote(self):
        md = """
> Whether you believe you can ...
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Whether you believe you can ...</blockquote></div>"
        )


    def test_quote_with_formatting(self):
        md = """
> Whether you believe you **can** or believe you **can't**, you're _right_. -- Henry ford
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Whether you believe you <b>can</b> or believe you <b>can't</b>, you're <i>right</i>. -- Henry ford</blockquote></div>"
        )


    def test_quote_two_lines(self):
        md = """
> Whether you believe you can or believe you can't, you're right.
> -- Henry Ford
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Whether you believe you can or believe you can't, you're right. -- Henry Ford</blockquote></div>"
        )


    def test_quote_three_lines_middle_none(self):
        md = """
> Whether you believe you can or believe you can't, you're right.
>
> -- Henry Ford
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Whether you believe you can or believe you can't, you're right.  -- Henry Ford</blockquote></div>"
        )


    def test_quote_two_lines_invalid(self):
        md = """
> Whether you believe you can or believe you can't, you're right.
-- Henry Ford
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>> Whether you believe you can or believe you can't, you're right. -- Henry Ford</p></div>"
        )


    def test_ul(self):
        md = """
- Take out the trash
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Take out the trash</li></ul></div>"
        )


    def test_ul_with_formatting(self):
        md = """
- Take out the **trash**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Take out the <b>trash</b></li></ul></div>"
        )


    def test_ul_multiple(self):
        md = """
- Take out the trash
- Make dinner
- Water the plants
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Take out the trash</li><li>Make dinner</li><li>Water the plants</li></ul></div>"
        )


    def test_simple_ol(self):
        md = """
1. Take out the trash
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Take out the trash</li></ol></div>"
        )


    def test_simple_ol_multiple(self):
        md = """
1. Take out the trash
2. Make dinner
3. Water the plants
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Take out the trash</li><li>Make dinner</li><li>Water the plants</li></ol></div>"
        )


    def test_codeblock(self):
        md = """
```py
print("hello world")
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>print(\"hello world\")</code></pre></div>"
        )


    def test_codeblock_multiple_with_formatting(self):
        md = """
```py
print("hello world")
static_text = "**This** is not bold, and _this_ is not italic."
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>print(\"hello world\")\nstatic_text = \"**This** is not bold, and _this_ is not italic.\"</code></pre></div>"
        )


    def test_try_to_cover_everything(self):
        md = """
# Hello World with a [Link](https://example.com)

My name is **computer**. Computers are [machines](https://machines.com).

They are _artificial_.

![A computer](https://i.imgur.com/computer.png)

## Lists over here

- Take out the trash
- Make dinner
- Water the plants

1. Take out the **trash**
2. Make dinner
3. Water the plants

```py
print("hello world")
static_text = "**This** is not bold, and _this_ is not italic."
```

> This is the best!
> ... Continued
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><h1>Hello World with a <a href=\"https://example.com\">Link</a></h1><p>My name is <b>computer</b>. Computers are <a href=\"https://machines.com\">machines</a>.</p><p>They are <i>artificial</i>.</p><p><img src=\"https://i.imgur.com/computer.png\" alt=\"A computer\"/></p><h2>Lists over here</h2><ul><li>Take out the trash</li><li>Make dinner</li><li>Water the plants</li></ul><ol><li>Take out the <b>trash</b></li><li>Make dinner</li><li>Water the plants</li></ol><pre><code>print(\"hello world\")\nstatic_text = \"**This** is not bold, and _this_ is not italic.\"</code></pre><blockquote>This is the best! ... Continued</blockquote></div>"
        )



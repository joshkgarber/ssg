from markdown_blocks import markdown_to_blocks, block_to_blocktype, BlockType
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import ParentNode
import re


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)


def block_to_html_node(block):
    blocktype = block_to_blocktype(block)
    match blocktype:
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.UL:
            return ul_to_html_node(block)
        case BlockType.OL:
            return ol_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.CODE:
            return codeblock_to_html_node(block)
        case _:
            raise ValueError("Unsupported blocktype")


def text_to_html(text):
    textnodes = text_to_textnodes(text)
    html = [text_node_to_html_node(textnode) for textnode in textnodes]
    return html


def heading_to_html_node(block):
    pattern = r"^#{1,6} "
    match = re.match(pattern, block)
    level = len(match[0]) - 1
    tag = f"h{level}"
    text = block.split(match[0], 1)[1]
    children = text_to_html(text)
    return ParentNode(tag, children)


def paragraph_to_html_node(block):
    text = block.split("\n")
    text = " ".join(text)
    children = text_to_html(text)
    return ParentNode("p", children)


def ul_to_html_node(block):
    items = block.split("\n")
    item_texts = [item[2:] for item in items]
    children = []
    for item_text in item_texts:
        item_children = text_to_html(item_text)
        list_item = ParentNode("li", item_children)
        children.append(list_item)
    return ParentNode("ul", children)


def ol_to_html_node(block):
    items = block.split("\n")
    item_texts = []
    pattern = r"^[1-9]\d*\. "
    for item in items:
        match = re.match(pattern, item)
        item_texts.append(item.split(match[0], 1)[1])
    children = []
    for item_text in item_texts:
        item_children = text_to_html(item_text)
        list_item = ParentNode("li", item_children)
        children.append(list_item)
    return ParentNode("ol", children)


def quote_to_html_node(block):
    texts = block.split("\n")
    texts = [text[2:] for text in texts]
    text = " ".join(texts)
    children = text_to_html(text)
    return ParentNode("blockquote", children)


def codeblock_to_html_node(block):
    text = block.split("\n")[1:-1]
    text = "\n".join(text)
    textnode = TextNode(text, TextType.CODE)
    htmlnode = text_node_to_html_node(textnode)
    return ParentNode("pre", [htmlnode])



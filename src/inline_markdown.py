from textnode import TextType
from textnode import TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            split_node = node.text.split(delimiter)
            n = len(split_node)
            if n % 2 == 0:
                raise Exception("invalid markdown syntax")
            for i in range(n):
                if i % 2 == 0:
                    if split_node[i]:
                        new_nodes.append(TextNode(split_node[i], TextType.PLAIN))
                else:
                    new_nodes.append(TextNode(split_node[i], text_type))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\[\]]*)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            original_text = node.text
            images = extract_markdown_images(original_text)
            if len(images) == 0:
                new_nodes.append(node)
                continue
            subject = original_text
            for img_txt, img_url in images:
                sections = subject.split(f"![{img_txt}]({img_url})", 1)
                if len(sections) != 2:
                    raise ValueError("invalid markdown, image section not closed")
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.PLAIN))
                new_nodes.append(TextNode(img_txt, TextType.IMAGE, img_url))
                subject = sections[1]
            if subject:
                new_nodes.append(TextNode(subject, TextType.PLAIN))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            original_text = node.text
            links = extract_markdown_links(original_text)
            if len(links) == 0:
                new_nodes.append(node)
                continue
            subject = original_text
            for lnk_txt, lnk_url in links:
                sections = subject.split(f"[{lnk_txt}]({lnk_url})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.PLAIN))
                new_nodes.append(TextNode(lnk_txt, TextType.LINK, lnk_url))
                subject = sections[1]
            if subject:
                new_nodes.append(TextNode(subject, TextType.PLAIN))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.PLAIN)
    return (
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_image(split_nodes_link([node])),
                    "`",
                    TextType.CODE
                ),
                "**",
                TextType.BOLD
            ),
            "_",
            TextType.ITALIC
        )
    )

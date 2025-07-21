from enum import Enum
import re


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda x: x.strip(), blocks))
    blocks = [block for block in blocks if block]
    return blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "ul"
    OL = "ol"


def block_to_blocktype(block):
    heading_pattern = r"^#{1,6} .+"
    if re.fullmatch(heading_pattern, block):
        return BlockType.HEADING
    code_pattern = r"^```.*?```$"
    if re.fullmatch(code_pattern, block, re.S):
        return BlockType.CODE
    quote_pattern = r"^>.*?$"
    lines = block.split("\n")
    quote_fail = [line for line in lines if not re.fullmatch(quote_pattern, line)]
    if not quote_fail:
        return BlockType.QUOTE
    ul_pattern = r"^- .*?$"
    ul_fail = [line for line in lines if not re.fullmatch(ul_pattern, line)]
    if not ul_fail:
        return BlockType.UL
    is_ol = check_is_ol(lines)
    if is_ol:
        return BlockType.OL
    return BlockType.PARAGRAPH


def check_is_ol(lines):
    ol_pattern = r"^[1-9]\d*\. .*?$"
    counter = 1
    for line in lines:
        if re.fullmatch(ol_pattern, line):
            num = int(line.split(". ", 1)[0])
            if num != counter:
                return False
            counter += 1
            continue
        return False
    return True


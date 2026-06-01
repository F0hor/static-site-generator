from textnode import BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_converter import text_to_htmlnodes


def markdown_to_blocks(markdown: str) ->list[str]:
    parts = markdown.split('\n\n')

    lst = []
    for p in parts:
        p = p.strip()
        if len(p) > 0:
            lst.append(p)

    return lst


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    lst = []

    for b in blocks:
        block_type = block_to_block_type(b)

        if block_type == BlockType.CODE:
            lst.append(
                ParentNode(
                    'pre',
                    [LeafNode('code', b[4:-3])]
                )
            )
            continue

        lst.append(text_to_child(b, block_type))
    
    return ParentNode('div', lst)

def text_to_child(text: str, block_type: BlockType) -> HTMLNode:
    if block_type == BlockType.LIST or block_type == BlockType.UNLIST:
        return list_to_child(text, block_type)

    if block_type == BlockType.QUOTE:
        return LeafNode('blockquote', text[1:].strip())

    if block_type == BlockType.HEADING:
        return heading_to_child(text)

    return ParentNode('p', text_to_htmlnodes(text.replace('\n', ' ')))


def heading_to_child(text: str) -> HTMLNode:
    num_hashtag = 0
    while text[num_hashtag] != '#':
        num_hashtag += 1

    return LeafNode(f'h{num_hashtag}', text[num_hashtag:].strip())


def list_to_child(text: str, block_type: BlockType) -> HTMLNode:
    lines = text.split('\n')
    lst = []

    for i, l in enumerate(lines):
        lst.append(LeafNode('li', l[l.index(' ')+1:]))

    return ParentNode(
        'ul' if block_type == BlockType.UNLIST else 'ol',
        lst
    )


def block_to_block_type(markdown: str) -> BlockType:
    if markdown[0] == '#':
        last_hashtag = 0
        for i in range(1, 7):
            if markdown[i] == '#':
                last_hashtag = i
        if last_hashtag < 6 and markdown[last_hashtag+1] == ' ':
            return BlockType.HEADING
    
    if markdown[:4] == "```\n" and markdown[-3:] == "```":
        return BlockType.CODE

    if markdown[0] == '>':
        return BlockType.QUOTE

    if markdown[0] == '-':
        valid = True
        for line in markdown.split('\n'):
            if line[:2] != "- ":
                valid = False
                break
        if valid:
            return BlockType.UNLIST

    if markdown[:3] == "1. ":
        valid = True
        lines = markdown.split('\n')
        for i, line in enumerate(lines):
            if not line.startswith(f'{i+1}. '):
                valid = False
                break
        if valid:
            return BlockType.LIST

    return BlockType.PARAGRAPH

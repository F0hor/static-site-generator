from textnode import TextType, TextNode
from htmlnode import LeafNode


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node is None or text_node.text_type is None or text_node.text_type not in TextType:
        raise Exception("Invalid text node tag")

    if text_node.text_type is TextType.TEXT:
        return LeafNode(None, text_node.text)

    if text_node.text_type is TextType.BOLD:
        return LeafNode('b', text_node.text)

    if text_node.text_type is TextType.ITALIC:
        return LeafNode('i', text_node.text)

    if text_node.text_type is TextType.CODE:
        return LeafNode('code', text_node.text)

    if text_node.text_type is TextType.LINK:
        return LeafNode('a', text_node.text, prop={'href': text_node.url})

    if text_node.text_type is TextType.IMAGE:
        return LeafNode('img', '', prop={'src': text_node.url, 'alt': text_node.text})


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 != 1:
            raise Exception("Invalid Markdown syntax")

        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


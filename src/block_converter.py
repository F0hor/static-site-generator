from textnode import BlockType

def markdown_to_blocks(markdown: str) ->list[str]:
    parts = markdown.split('\n\n')

    lst = []
    for p in parts:
        p = p.strip()
        if len(p) > 0:
            lst.append(p)

    return lst

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

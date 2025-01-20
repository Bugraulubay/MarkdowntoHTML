
def markdown_to_blocks(markdown):
    blocks = list(filter(None,markdown.split("\n\n")))
    result = list(map(lambda x:x.strip() , filter(lambda x:x!="",blocks)))
    return result

def blocks_to_block_type(blocks):
    if blocks == None:
        return None
    for block in blocks:
        if block.startswith("#"):
            return "heading"
        if block.startswith("```") and block.endswith("```"):
            return "code"
        if block.startswith(">"):
            return "quote"
        if block.startswith("* ") or block.startswith("- "):
            return "unordered_list"
        if block.startswith("1."):
            return "ordered_list"
        else: return "paragraph"
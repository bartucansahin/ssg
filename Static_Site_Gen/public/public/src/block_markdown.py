from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered = "unordered list"
block_type_ordered = "ordered list"

def markdown_to_blocks(markdown):
    lines = markdown.strip().split("\n")
    
    blocks = []
    current_block = ""
    for line in lines:
        line = line.strip()
        if line:
            current_block += line + "\n"
        else:
            if current_block:
                blocks.append(current_block.strip())
                current_block = ""

    if current_block:
        blocks.append(current_block.strip())
    
    return blocks

def block_to_block_type(md_block):
    if any(md_block.startswith(prefix) for prefix in ("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    
    if md_block.startswith("```") and md_block.endswith("```"):
        return block_type_code
    
    split = md_block.split("\n")
    for line in split:
        if line.startswith(">"):
            return block_type_quote
    
    for line in split:
        if any(line.startswith(prefix) for prefix in ("* ", "- ")):
            return block_type_unordered
    
    integer = 1
    is_ordered_list = False
    for line in split:
        if line.startswith(f"{integer}."):
            is_ordered_list = True
        integer += 1
    
    if is_ordered_list:
        return block_type_ordered
    
    else:
        return block_type_paragraph

def from_mdBlock_to_HTMLNode(md_block, block_type):
    if block_type == block_type_paragraph:
        leaf_node = LeafNode(None, md_block, None)
        return ParentNode("p", [leaf_node], None)
    
    if block_type == block_type_quote:
        for block in md_block:
            block = block[1:].strip()
        leaf_node = LeafNode(None, block, None)
        return ParentNode("blockquote", [leaf_node], None)

    if block_type == block_type_unordered:
        for block in md_block:
            lines = block.split('\n')
            li_covered = []
        for line in lines:
            new_line = line[1:].strip()
            li_covered.append(LeafNode("li", new_line, None))
        return ParentNode("ul", li_covered , None)

    if block_type == block_type_ordered:
        for block in md_block:
            lines = block.split('\n')
            li_covered = []
        for line in lines:
            new_line = line[line.index('.') + 1:].strip()
            li_covered.append(LeafNode("li", new_line, None))
        return ParentNode("ol", li_covered, None)
    
    if block_type == block_type_code:
        md_block = md_block.strip("```")
        pre_covered = LeafNode("pre", md_block, None)
        return ParentNode("code", [pre_covered], None)
    
    if block_type == block_type_heading:
        heading_prefixes = {
        "# ": "h1",
        "## ": "h2",
        "### ": "h3",
        "#### ": "h4",
        "##### ": "h5",
        "###### ": "h6"
        }
        leaf_node = []
        for prefix, tag in heading_prefixes.items():
            for block in md_block:
                if block.startswith(prefix):
                    block = block[len(prefix):]
                    leaf_node.append(LeafNode(None , block, None))
                    return ParentNode(tag, leaf_node, None)
    
def markdown_to_HTMLNode(markdown):
    block_by_block = markdown_to_blocks(markdown)
    children = []
    for block in block_by_block:
        block_type = block_to_block_type(block)
        text_nodes = text_to_textnodes(block)
        inline_leaf_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        leaf_nodes_to_html = [leaf_node.to_html() for leaf_node in inline_leaf_nodes]
        children.extend(from_mdBlock_to_HTMLNode(leaf_nodes_to_html, block_type))
    return ParentNode("div", children, None)
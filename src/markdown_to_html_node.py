import textnode
import htmlnode
import blocks
from split_nodes import text_to_textnodes
from text_node_to_html_node import text_node_to_html_node

def markdown_to_html_node(markdown: str) -> htmlnode.ParentNode:

    def block_to_html_node(block):
        block_type = (blocks.block_to_block_type(block))
        line_tag = None # Tag for each line of a multiline tag
        line_markdown = None # Markdown for each line of a multiline tag

        match (block_type):
            case blocks.BlockType.PARAGRAPH:
                block_node = htmlnode.ParentNode(tag='p', children=[])
                text = block

            case blocks.BlockType.HEADING:
                hashtag_count = 0
                while (hashtag_count < len(block)) and (block[hashtag_count] == '#'):
                    hashtag_count += 1
                block_node = htmlnode.ParentNode(tag=f'h{hashtag_count}', children=None)
                text = block[(hashtag_count + 1):]

            case blocks.BlockType.CODE:
                text = block[3:-3].lstrip()
                inner_node = htmlnode.LeafNode(tag='code', value=text)
                block_node = htmlnode.ParentNode(tag="pre", children=[inner_node])
                return block_node
            
            case blocks.BlockType.QUOTE:
                block_node = htmlnode.ParentNode(tag='blockquote', children=None)
                text = block
                line_tag = "p"
                line_markdown = ">"

            case blocks.BlockType.UNORDERED_LIST:
                block_node = htmlnode.ParentNode(tag='ul', children=None)
                text = block
                line_tag = "li"
                line_markdown = "-"

            case blocks.BlockType.ORDERED_LIST:
                block_node = htmlnode.ParentNode(tag='ol', children=None) # We'll need to add li tags for each entry.
                text = block
                line_tag = "li"
                line_markdown = "."
                
            case _:
                raise NotImplementedError(f"Unknown block type {block_type}.")
            
        
        if line_tag is None:
            text = text.replace('\n', ' ')
            child_text_nodes = text_to_textnodes(text)
            block_node.children = [text_node_to_html_node(text_node) for text_node in child_text_nodes]
            
        else:                   # If we have a multiline tag, break it into lines
            line_nodes = []
            text_list = text.split('\n')
            text_list = [text.strip() for text in text_list if text.strip() != ""]

            for line in text_list:
                line = line[line.find(line_markdown) + 1:]
                line = line.strip()
                if line == "":
                    continue
                line_text_nodes = text_to_textnodes(line)
                line_html_node = htmlnode.ParentNode(tag=line_tag, children=[text_node_to_html_node(text_node) for text_node in line_text_nodes])
                line_nodes.append(line_html_node)
            
            block_node.children = line_nodes

        return block_node 

    # ------ markdown_to_html_node function body begins

    markdown_blocks = blocks.markdown_to_blocks(markdown)
    child_nodes = []

    for block in markdown_blocks:
        child_nodes.append(block_to_html_node(block))
    
    return htmlnode.ParentNode(tag="div", children=child_nodes)

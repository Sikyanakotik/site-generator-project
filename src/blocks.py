import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 4
    QUOTE = 8
    UNORDERED_LIST = 16
    ORDERED_LIST = 32

def markdown_to_blocks(text: str) -> list:
    raw_blocks = text.split('\n\n')
    blocks = []
    for block in raw_blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            blocks.append(stripped_block)
    return blocks

def block_to_block_type(block: str) -> BlockType:
    match block[0]:
        case '#':
            if re.match(r'#{1,6} \S', block) != None:
                return BlockType.HEADING
            else:
                return BlockType.PARAGRAPH
        case "`":
            if (block[0:3] == "```") and (block[-3:] == "```") and len(block) > 6:
                return BlockType.CODE
            else:
                return BlockType.PARAGRAPH
        case ">":
            if re.search(r"\n[^>]", block) == None:
                return BlockType.QUOTE
            else:
                return BlockType.PARAGRAPH
        case "-":
            lines = block.split('\n')
            for line in lines:
                if line[0:2] != "- ":
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        
        case "1":
            lines = block.split('\n')
            for index, line in enumerate(lines):
                if (line[0] != f'{index + 1}') or (line[1:3] != ". "): # NOTE: Only works for fewer than 10 lines
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST

        case _:
            return BlockType.PARAGRAPH



if __name__ == "__main__":
    print(block_to_block_type("# "))
    print(block_to_block_type("### "))
    print(block_to_block_type("######## "))
    print(block_to_block_type("French fries"))
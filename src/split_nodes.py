from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits a list of TextNode objects into sublists based on a delimiter.
    Each time a TextNode with text equal to the delimiter is found, a new sublist is started.
    The delimiter nodes themselves are not included in the output.
    NOTE: This version does not handle nested delimiters within a single TextNode.

    Args:
        old_nodes (list of TextNode): The original list of TextNode objects.
        delimiter (str): The text value that indicates where to split the nodes.
        text_type (TextType): The TextType to assign to the new TextNode objects created from splits.

    Returns:
        list of list of TextNode: A list containing sublists of TextNode objects.
    """
    new_nodes = []
    
    for node in old_nodes:
        current_sublist = []

        if node.text_type != TextType.PLAIN:
            current_sublist.append(node)
        else:
            parts = node.text.split(delimiter)

            if len(parts) % 2 == 0:
                raise ValueError("Unmatched delimiter found in TextNode text.")

            for i, part in enumerate(parts):
                if (i % 2 == 0) and part != "":
                    current_sublist.append(TextNode(part, TextType.PLAIN))
                elif (part != ""):
                    current_sublist.append(TextNode(part, text_type))
        
        new_nodes.extend(current_sublist)
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
            continue

        sublist = [node]
        for image in images:
            new_sublist = []
            image_string = f"![{image[0]}]({image[1]})"
            for subnode in sublist:
                if image_string in subnode.text:
                    split_text = subnode.text.split(image_string, maxsplit=1)
                    if split_text[0] != "":
                        new_sublist.append(TextNode(split_text[0], TextType.PLAIN))
                    new_sublist.append(TextNode(text=image[0], url=image[1], text_type=TextType.IMAGE))
                    if split_text[1] != "":
                        new_sublist.append(TextNode(split_text[1], TextType.PLAIN))
                else:
                    new_sublist.append(subnode)
            sublist = new_sublist
        new_nodes.extend(sublist)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(node)
            continue

        sublist = [node]
        for link in links:
            new_sublist = []
            link_string = f"[{link[0]}]({link[1]})"
            for subnode in sublist:
                if link_string in subnode.text:
                    split_text = subnode.text.split(link_string, maxsplit=1)
                    if split_text[0] != "":
                        new_sublist.append(TextNode(split_text[0], TextType.PLAIN))
                    new_sublist.append(TextNode(text=link[0], url=link[1], text_type=TextType.LINK))
                    if split_text[1] != "":
                        new_sublist.append(TextNode(split_text[1], TextType.PLAIN))
                else:
                    new_sublist.append(subnode)
            sublist = new_sublist
        new_nodes.extend(sublist)

    return new_nodes

def text_to_textnodes(text) -> list:
    """
    Coverts mark text to TextNodes. Returns a list of nodes/
    
    :param text: The mark
    """
    text_nodes = [TextNode(text, TextType.PLAIN)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
    

if __name__ == "__main__":
    print(text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"))
    


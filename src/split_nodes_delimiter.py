from textnode import TextNode, TextType

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
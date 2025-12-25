import re

def extract_markdown(text, regex):
    """
    Converts a markdown text string into a list of strings or tuples.
    Each output matches the included regex string.

    :param text: The string to extract from, in markdown format.
    :param regex: The regular expression to match.
    """
    markdown_matches = re.findall(regex, text)

    output = []
    for match in markdown_matches:
        output.append(match)
    
    return output

def extract_markdown_images(text):
    """
    Converts a markdown text string into a list of tuples.
    Each tuple should contain the alt text and the URL of any markdown images.
    Markdown images are delineated by ![alt text](URL).

    :param text: The string to extract images from, in markdown format.
    """
    return extract_markdown(text, r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")

def extract_markdown_links(text):
    """
    Converts a markdown text string into a list of tuples.
    Each tuple should contain the text and the URL of any markdown links.
    Markdown links are delineated by [text](URL).

    :param text: The string to extract links from, in markdown format.
    """
    return extract_markdown(text, r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")

if __name__ == "__main__":
    print(extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"))
    print(extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"))
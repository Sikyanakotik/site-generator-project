from enum import Enum

class TextType(Enum):
    PLAIN = 1
    BOLD = 2
    ITALIC = 4
    CODE = 8
    LINK = 16
    IMAGE = 32

class TextNode:
    def __init__(self, text, text_type=TextType.PLAIN, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def main():
    tm = TextNode("example", TextType.LINK, "http://example.com")
    print(tm)

if __name__ == "__main__":
    main()
from textnode import TextNode, TextType

def main():
    tm = TextNode("example", TextType.LINK, "http://example.com")
    print(tm)

if __name__ == "__main__":
    main()
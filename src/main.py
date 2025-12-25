import os
import shutil

from textnode import TextNode, TextType

def copy_static_to_public():
    shutil.rmtree("/public")


def main():
    copy_static_to_public()

if __name__ == "__main__":
    main()
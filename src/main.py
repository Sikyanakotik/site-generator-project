import os
import shutil

from textnode import TextNode, TextType
from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node

PUBLIC_PATH = "public/"
STATIC_PATH = "static/"

def copy_static_to_public():
    def copy_dir_to_dir(source_path, dest_path):
        source_contents = os.scandir(source_path)
        for entry in source_contents:
            dest = os.path.join(dest_path, entry.name)
            if entry.is_dir():
                os.mkdir(dest)
                copy_dir_to_dir(entry.path, dest)
            else:
                shutil.copy(entry, dest)
    #----

    if os.path.exists(PUBLIC_PATH):
        shutil.rmtree(PUBLIC_PATH)
    os.mkdir(PUBLIC_PATH)
    
    copy_dir_to_dir(STATIC_PATH, PUBLIC_PATH)
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    
    with open(from_path, 'r') as markdown_file:
        markdown = markdown_file.read()

    with open(template_path, 'r') as template_file:
        template = template_file.read()

    title = extract_title(markdown)
    html_nodes = markdown_to_html_node(markdown)
    html_content = html_nodes.to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    with open(dest_path, 'w') as page_file:
        page_file.write(template)

def generate_pages_in_dir(source_path, template_path, dest_path):
    source_contents = os.scandir(source_path)    
    for entry in source_contents:
        print(entry.name)
        dest = os.path.join(dest_path, entry.name)
        if entry.is_dir():
            os.mkdir(dest)
            generate_pages_in_dir(entry.path, template_path, dest)
        elif entry.name[-3:] == ".md":
            generate_page(entry, template_path, dest[:-3] + ".html")

def main():
    template_path = "template.html"
    copy_static_to_public()
    generate_pages_in_dir("content/", template_path, "public/")


if __name__ == "__main__":
    main()
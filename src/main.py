import os
import shutil

from textnode import TextNode, TextType

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
    

    


def main():
    copy_static_to_public()

if __name__ == "__main__":
    main()
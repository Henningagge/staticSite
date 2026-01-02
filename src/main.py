from textnode import TextNode,TextType
from webside import copy_files_recursive, generate_page,generate_pages_recursive
import sys
import shutil
def main():
    shutil.rmtree("public")
    base = sys.argv[0]
    print("hello world")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node.__repr__())
    copy_files_recursive("./static","./docs")
    generate_pages_recursive(base, "template.html", "docs")
if __name__ == "__main__":
    main() 
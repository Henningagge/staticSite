from textnode import TextNode,TextType
from webside import copy_files_recursive, generate_page,generate_pages_recursive
import shutil
def main():
    shutil.rmtree("public")
    print("hello world")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node.__repr__())
    copy_files_recursive("./static","./public")
    generate_pages_recursive("content", "template.html", "public")
if __name__ == "__main__":
    main() 
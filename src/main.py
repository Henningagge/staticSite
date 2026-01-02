from textnode import TextNode,TextType
from webside import copy_files_recursive, generate_page
def main():
    print("hello world")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node.__repr__())
    copy_files_recursive("./static","./public")
    generate_page("content/index.md", "template.html", "public/index.html")
if __name__ == "__main__":
    main() 
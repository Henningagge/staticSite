from textnode import TextNode,TextType
from webside import copy_files_recursive
def main():
    print("hello world")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node.__repr__())
    copy_files_recursive("./static","./public")
if __name__ == "__main__":
    main() 
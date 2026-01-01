
from textnode import TextNode,TextType
import re
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    newNode = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            newNode.append(node)
            continue
        split2 = node.text.split(delimiter)
        splitNode = []
        if len(split2) %2 == 0:
            raise ValueError("no closing tag given")
        for i in range(len(split2)):
            if split2[i] == "":
                continue
            if i% 2 == 0:
                splitNode.append(TextNode(split2[i],TextType.TEXT))
            else:
                splitNode.append(TextNode(split2[i], text_type))
        newNode.extend(splitNode)

        

    return newNode

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches
def split_nodes_image(old_nodes:list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]  # Continue with the rest
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]  # Continue with the rest
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    delimited1 = split_nodes_delimiter(node, "**",TextType.BOLD)
    delimited2 = split_nodes_delimiter(delimited1, "_", TextType.ITALIC)
    delimited3 = split_nodes_delimiter(delimited2, "`", TextType.CODE)
    image1 = split_nodes_image(delimited3)
    link1 = split_nodes_link(image1)

    return link1
    #split nodes links(nodes)
    #split nodes images(nodes)
    #split nodes delimiter(oldnodes, delimieter, texttype)
    

def markdown_to_blocks(markdown):
        markdown2 = []
        splited_Markdown = markdown.split("\n\n")
        for markdonw in splited_Markdown:
            if markdonw != "":
                stripedMarkdonw = markdonw.strip()

                markdown2.append(stripedMarkdonw)
        return markdown2
from enum import Enum
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def block_to_block_type(markdown):
    heading_match = re.findall(r"^#{1,6}",markdown)
    if heading_match == "":
        return BlockType.HEADING
    code_match = re.findall(r"```[^`]*```",markdown)
    if code_match != "":
        return BlockType.CODE
    split_quote = markdown.split("\n")
    is_quote = True
    for quote in split_quote:
        if quote[0] != ">":
            is_quote = False
    if is_quote == True:
        return BlockType.QUOTE
    is_ulist = True
    for item in split_quote:
        if quote[:1] != "- ":
            is_ulist = False
    if is_ulist == True:
        return BlockType.ULIST
    is_olist = True
    for i in range(len(split_quote)):
        if split_quote[i][:2] != f"{i+1}. ":
            is_olist == False
    if is_olist == True:
        return BlockType.OLIST
    return BlockType.PARAGRAPH


#matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
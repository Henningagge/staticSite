
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

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


#matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)


def markdown_to_html_node(markdonw):
    blocks = markdown_to_blocks(markdonw)
    for block in blocks:
        blockType = block_to_block_type(block)
        
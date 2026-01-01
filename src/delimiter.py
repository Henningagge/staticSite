
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
from htmlnode import HTMLNode,ParentNode
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
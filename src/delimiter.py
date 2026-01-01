
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
    newNode = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            newNode.append(node)
            continue
        text = node.text
        matches = extract_markdown_images(text)
        for match in matches:
            text = text.replace(f"![{match[0]}]({match[1]})", "### hello ###")
        split2 = text.split("###")
        splitNode = []
        count = 0
        for i in range(len(split2)):
            if split2[i]== " hello ":
                splitNode.append(TextNode(matches[count][0],TextType.IMAGE, matches[count][1]))
                count+=1
            elif split2[i] == "":
                continue
            else:
                splitNode.append(TextNode(split2[i],TextType.TEXT))

        newNode.extend(splitNode)
        

    return newNode
def split_nodes_link(old_nodes):
    newNode = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            newNode.append(node)
            continue
        text = node.text
        matches = extract_markdown_links(text)
        for match in matches:
            text = text.replace(f"[{match[0]}]({match[1]})", "### hello ###")
        split2 = text.split("###")
        splitNode = []
        count = 0
        for i in range(len(split2)):
            if split2[i]== " hello ":
                splitNode.append(TextNode(matches[count],TextType.LINK))
                count+=1
            else:
                splitNode.append(TextNode(split2[i],TextType.TEXT))
        
        newNode.extend(splitNode)
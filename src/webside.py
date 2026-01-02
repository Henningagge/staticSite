import os
import os.path
import shutil


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            title = line[2:]
            title = title.strip()
            return title

from delimiter import markdown_to_html_node
def generate_page(from_path, template_path, dest_path):
    print(f"Generting page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdownText = file.read()
    with open(template_path, "r") as file:
        template_text = file.read()
    markdownHtml = markdown_to_html_node(markdownText).to_html()

    title = extract_title(markdownText)
    template_text = template_text.replace("{{ Title }}", title)
    template_text = template_text.replace("{{ Content }}", markdownHtml)

    writeHtmlPage(template_text, dest_path)

def writeHtmlPage(template, dest_path):
    pathParts = dest_path.split("/")
    path = "/".join(pathParts[:-1])
    if not os.path.exists(path):
        os.makedirs(path)
    with open(dest_path, "w") as file:
        file.write(template)
#todo make the public directory delete it sealf at the start of the main.sh



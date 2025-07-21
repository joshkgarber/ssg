import logging
from document import markdown_to_html_node
import os
from pathlib import Path


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def extract_title(markdown):
    first_line = markdown.split("\n\n", 1)[0].strip()
    if first_line[:2] != "# ":
        raise ValueError("title missing or invalid")
    return first_line[2:]


def generate_page(from_path, template_path, dest_path, basepath):
    logger.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    logger.info("Getting markdown content")
    with open(from_path) as f:
        markdown = f.read()
    logger.info("Getting html template")
    with open(template_path) as f:
        template = f.read()
    logger.info("Converting markdown to html")
    content = markdown_to_html_node(markdown).to_html()
    logger.info("Getting page title")
    title = extract_title(markdown)
    logger.info("Inserting title and page content into template")
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    logger.info(f"Writing {dest_path} to disk")
    path = os.path.dirname(dest_path)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files = os.listdir(dir_path_content)
    for file in files:
        from_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
            continue
        generate_pages_recursive(from_path, template_path, dest_path, basepath)



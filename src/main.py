import os
import shutil

from block_converter import markdown_to_blocks, markdown_to_html_node
from textnode import BlockType


def copy_content_to_folder(source: str, destination: str):
    for name in os.listdir(source):
        path = os.path.join(source, name)
        if not os.path.exists(path):
            continue

        if os.path.isfile(path):
            shutil.copy(path, destination)
            print(f'copied: {path} -> {destination}')

        else:
            dst = os.path.join(destination, name)
            os.mkdir(dst)
            print(f'created: {dst}')
            copy_content_to_folder(path, os.path.join(destination, name))


def extrect_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)

    for b in blocks:
        if b.startswith('# '):
            return b[2:]

    raise Exception('Missing title in form of h1 header')


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f:
        markdown = f.read()

    with open(template_path, 'r') as f:
        template = f.read()

    title = extrect_title(markdown)
    html_body = markdown_to_html_node(markdown).to_html()

    html = template.replace('{{ Title }}', title).replace('{{ Content }}', html_body)

    with open(dest_path, "w") as f:
        f.write(html)


def generate_content(source: str, template: str, dest: str):
    for name in os.listdir(source):
        source_path = os.path.join(source, name)
        dest_path = os.path.join(dest, name)

        if os.path.isfile(source_path):
            dest_path = dest_path.replace('.md', '.html')
            generate_page(source_path, template, dest_path)
        else:
            os.mkdir(dest_path)
            generate_content(source_path, template, dest_path)


def main():
    shutil.rmtree(PATH_TO_PUBLIC)
    os.mkdir(PATH_TO_PUBLIC)

    copy_content_to_folder(PATH_TO_STATIC, PATH_TO_PUBLIC)
    generate_content(PATH_TO_CONTENT, PATH_TO_TEMPLATE, PATH_TO_PUBLIC)
    

PATH_TO_PUBLIC = 'public/'
PATH_TO_STATIC = 'static/'
PATH_TO_CONTENT = 'content/'
PATH_TO_TEMPLATE = 'template.html'
main()


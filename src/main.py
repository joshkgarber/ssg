import os
import shutil
import logging
from copystatic import copy_contents
from gencontent import generate_page


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    if not os.path.exists(dir_path_static):
        raise ValueError("Source folder does not exist")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    os.mkdir(dir_path_public)
    logger.info("Start copying contents")
    copy_contents(dir_path_static, dir_path_public)
    logger.info("Finished copying contents")
    logger.info("Start generating index page")
    generate_page(
        os.path.join(dir_path_content, "index.md"),
        template_path,
        os.path.join(dir_path_public, "index.html")
    )
    logger.info("Finished generating index page")


if __name__ == "__main__":
    main()

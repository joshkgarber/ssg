import os
import shutil
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def copy_contents(source, destination):
    contents = os.listdir(source)
    for content in contents:
        content_path = os.path.join(source, content)
        if os.path.isfile(content_path):
            print(f"destination: {destination}")
            shutil.copy(content_path, destination)
            logger.info(f"Copying {content_path} to {destination}")
        else:
            new_dir = os.path.join(destination, content)
            os.makedirs(new_dir)
            copy_contents(content_path, new_dir)



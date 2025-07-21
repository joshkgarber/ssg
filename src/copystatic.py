import os
import shutil
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def copy_files_recursive(source_dir_path, dest_dir_path):
    files = os.listdir(source_dir_path)
    for file in files:
        filepath = os.path.join(source_dir_path, file)
        if os.path.isfile(filepath):
            logger.info(f"Copying {filepath} to {dest_dir_path}")
            shutil.copy(filepath, dest_dir_path)
        else:
            new_dir = os.path.join(dest_dir_path, file)
            os.makedirs(new_dir)
            copy_files_recursive(filepath, new_dir)



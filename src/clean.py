import shutil
from pathlib import Path

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json


class OrganizeFiles:
    """
    This class is used to organize files in a directory.
    """
   
    def __init__(self, directory):
        self.directory = Path(directory)
        if not self.directory.is_dir():
            raise FileExistsError(f'{self.directory} is not a directory')
        

        extensions = read_json(DATA_DIR / 'extensions.json')
        self.extensions_directories = {}
        for dir_name, exts in extensions.items():
            for ext in exts:
                self.extensions_directories[ext] = dir_name
        

    def __call__(self):
        """
        Organize files in the directory.
        regarding to file extentions
        """
        file_extentions = []

        for file_path in self.directory.iterdir():

            if file_path.is_dir():
                continue
            
            if str(file_path).startswith('.'):
                continue
                
            # get all file types    
            file_extentions.append(file_path.suffix)
            
            if file_path.suffix not in self.extensions_directories:
                DEST_DIR = self.directory / 'others'
            else:
                DEST_DIR = self.directory / self.extensions_directories[file_path.suffix]
            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f'Moving {file_path} to {DEST_DIR}')
            shutil.move(str(file_path), str(DEST_DIR))


if __name__ == '__main__':
    organize_files = OrganizeFiles('/mnt/c/Users/RAI/Desktop/CS-tutorial/Projects/clean-directory/src/data/files')
    organize_files()
       
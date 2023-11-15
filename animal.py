from configurator import Configurator
from typing import List
import os

configurator = Configurator()

class Animal:
    WIKI_PREFIX_URL = configurator.get_wiki_prefix()
    IMG_DIR_NAME = configurator.get_animals_img_dir_path()
    IMG_DIR_PATH = os.path.join(os.getcwd(), IMG_DIR_NAME)
    os.makedirs(IMG_DIR_PATH, exist_ok=True)
    
    def __init__(self, name: str, adjectives: List[str], link_extension: str) -> None:
        self.name = name
        self.adjectives = adjectives
        self.wiki_page_url = Animal.WIKI_PREFIX_URL.format(link_extension=link_extension)
        self.img_file_name = f"{self.name.replace(' ', '_')}.jpg"
        self.img_path = os.path.join(Animal.IMG_DIR_PATH, self.img_file_name)
        self.img_src = None
    
    def __repr__(self) -> str:
        return f"Name: {self.name}\n\t\tImage Path: {self.img_path}"
    

    def get_wiki_page_url(self):
        return self.wiki_page_url
    
    def get_img_path(self):
        return self.img_path
    
    def get_name(self):
        return self.name
    
    def set_img_src(self, img_src):
        self.img_src = img_src
    
    def get_img_src(self):
        return self.img_src
    
    def save_img(self, img):
        with open(self.img_path, 'wb') as image_file:
            image_file.write(img)
            print(f"{self.__class__.__name__} {self.name}- Image saved successfully")
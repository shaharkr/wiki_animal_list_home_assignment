from configurator import Configurator
from typing import List

configurator = Configurator()

class Animal:
    WIKI_PREFIX_URL = configurator.get_wiki_prefix()
    IMG_DIR_PATH = configurator.get_animals_img_dir_path()
    
    def __init__(self, name: str, adjectives: List[str], img_src: str = None) -> None:
        self.name = name
        self.wiki_page_url = Animal.WIKI_PREFIX_URL.format(link_extension=self.name.replace(' ', '_'))
        self.img_path = f"{Animal.IMG_DIR_PATH}\{self.name.replace(' ', '_')}.jpg"
        self.adjectives = adjectives
        self.img_src = img_src
    
    def __repr__(self) -> str:
        return f"Name: {self.name}\n\t\tImage path link: {self.img_path}"
    
    def get_wiki_page_url(self):
        return self.wiki_page_url
    
    def get_img_path(self):
        return self.img_path
    
    def set_img_src(self, img_src: str) -> None:
        self.img_src = img_src
    
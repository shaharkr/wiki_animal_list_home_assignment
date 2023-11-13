from configurator import Configurator

configurator = Configurator()

class Animal:
    WIKI_PREFIX_URL = configurator.get_wiki_prefix()
    IMG_DIR_PATH = configurator.get_animals_img_dir_path()
    
    def __init__(self, name: str) -> None:
        self.name = name.replace(' ', '_')
        self.wiki_page_url = Animal.WIKI_PREFIX_URL.format(link_extension=self.name)
        self.img_path = f"{Animal.IMG_DIR_PATH}/{self.name}"
    
    def __repr__(self) -> str:
        return f"Name: {self.name}/n Wiki link: {self.wiki_page_url}"
from configurator import Configurator
from animal import Animal
from dal.web_exetractor import WebExtractor
from bs4 import BeautifulSoup
from commonStr import ExecutorProperties, WikiDataHandlerProperties, HtmlElements
from typing import List

config = Configurator()

class WikiAnimalDataHandler:
    """This class is responsible for managing animal operations, like creation, download and saving image."""
    def __init__(self, animal_name: str, animal_adjectives: List[str], link_extension: str) -> None:
        self.__animal = Animal(name=animal_name, adjectives=animal_adjectives, link_extension=link_extension)
    
    def get_animal(self) -> Animal:
        return self.__animal
    
    def download_animal_img(self):
        img_content = None
        try:
            img_content = self.__extract_wiki_animal_img_content()  # Retrieves the text content of the animal wiki page
        except Exception as e:
            raise Exception(f"reason: {str(e)}")
        self.__animal.save_img(img_content)
    
    def __extract_wiki_animal_img_content(self) -> str:
        """Retrieves the content of the animal wiki img"""
        img_src = self.__get_animal_img_src()
        self.__animal.set_img_src(img_src)
        header = config.get_animal_img_header_request()
        res = WebExtractor.send_get_request(url=img_src, attribute_needed=ExecutorProperties.response_att_content, headers=header)
        return res
    
    def __extract_wiki_animal_page_text(self) -> str:
        """Retrieves the text content of the animal wiki page"""
        url = self.__animal.get_wiki_page_url()
        res = WebExtractor.send_get_request(url=url, attribute_needed=ExecutorProperties.response_att_txt)
        return res
    
    def __get_animal_img_src(self) -> str:
        txt = self.__extract_wiki_animal_page_text()  # Retrieves the text content of the animal wiki page
        soup = BeautifulSoup(txt, 'html.parser')
        animal_img_src = self.__extract_img_src_from_html_tree(soup=soup)
        return animal_img_src
    
    def __extract_img_src_from_html_tree(self, soup: BeautifulSoup):
        tbl = soup.find(HtmlElements.tbl,
                        class_=lambda classes: 
                            classes and WikiDataHandlerProperties.animal_tbl_class_substring_name in classes)
        img_container = None
        if tbl is None:
            img_container = soup.find(HtmlElements.a, 
                                      {HtmlElements.class_: WikiDataHandlerProperties.animal_img_class_substring_name})
        else:
            row = tbl.find_all(HtmlElements.tr)[1:][0]
            img_container = row
        img_row = img_container.find(HtmlElements.img)
        animal_img_src = f"https:{img_row.get(HtmlElements.src)}"
        return animal_img_src
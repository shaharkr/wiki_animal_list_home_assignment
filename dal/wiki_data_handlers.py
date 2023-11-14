from configurator import Configurator
from animal import Animal
from dal.web_exetractor import WebExtractor
from bs4 import BeautifulSoup, element
from commonStr import ExecutorProperties, WikiDataHandlerProperties, HtmlElements
from typing import Tuple, List
from itertools import takewhile


config = Configurator()
        
class WikiAnimalNamesListDataHandler:
    """This class is responsible for managing tasks 
    related to the extraction, parsing, and mapping of animal names and their adjectives from a list."""
    
    FAILED_MSG = 'failed to get list of animals names'
        
    def create_collateral_adjective_to_animal(self) -> dict:
        """
        Parses the list of animal names and their adjectives, creating a dictionary mapping adjectives to corresponding Animal objects and return it.
        """
        
        adjective_to_animals_dict = {}
        animals_rows, animal_th_indx, ca_th_indx = self.prepare_meta_data_for_parsing()
        
        # iter tables row, each row represent an animal.
        for row in animals_rows:
            # table is sorted alphabetically by default, these headers represent letters of the alphabet. We want to ignore these row.
            if row.find_all(HtmlElements.th).__len__() == 0:
                columns = row.find_all(HtmlElements.td)
                
                # using the right indexes to get animal data:
                    # get the name of the animal
                animal_name_text = columns[animal_th_indx].get_text()
                animal_name = self.clean_string_from_non_letters(animal_name_text)
                    # create the collateral adjective list
                adjectives_text_lst = [adj.get_text(strip=True) for adj in columns[ca_th_indx].contents]  
                adjectives_lst = self.clean_adjectives_list(adjectives_text_lst)
                
                new_animal = Animal(name=animal_name, adjectives=adjectives_lst)
                
                for adj in adjectives_lst:
                    if adj not in adjective_to_animals_dict:  # first time foud this adjective
                        adjective_to_animals_dict[adj] = []
                    adjective_to_animals_dict[adj].append(new_animal)
        return adjective_to_animals_dict
    
    
    def extract_wiki_animal_name_list_text(self) -> str:
        """Retrieves the text content of the list of animal names from a specified URL."""
        
        url = config.get_wiki_list_of_animals_url()
        res = WebExtractor.send_get_request(url=url, attribute_needed=ExecutorProperties.response_att_txt)
        return res
    
    def get_animal_table(self, soup: BeautifulSoup) -> element.Tag:
        """Finds and returns the HTML table element containing the list of animal names from the BeautifulSoup object."""
        
        title = soup.find(HtmlElements.span,
                          {HtmlElements.id: WikiDataHandlerProperties.id_of_animal_table_title})
        return title.find_next(HtmlElements.table)
    
    def get_animal_and_collateral_adjective_th_indexes(self, tbl: element.Tag) -> tuple:
        """Retrieves the column indexes for animal names and collateral adjectives from the table header."""
        
        columns_labels = tbl.find_all(HtmlElements.tr)[0].find_all(HtmlElements.th)  # get the headers row
        animal_idx, c_a_idx = None, None
        for index, col in enumerate(columns_labels):
            t = col.text
            if t == WikiDataHandlerProperties.collaretal_adjective_column_label:
                c_a_idx = index
            elif t == WikiDataHandlerProperties.animal_column_label:
                animal_idx = index
                
            if animal_idx is not None and c_a_idx is not None:
                break
        return animal_idx, c_a_idx
    
    def prepare_meta_data_for_parsing(self) -> Tuple[list, int, int]:
        """
        Prepares the necessary metadata for parsing, including the list of animal rows and relevant column indexes.
        """
         
        txt = None
        try:
            txt = self.extract_wiki_animal_name_list_text()  # Retrieves the text content of the list of animal names from a specified URL
        except Exception as e:
            raise Exception(f"{WikiAnimalNamesListDataHandler.FAILED_MSG}, reason: {str(e)}")
        
        soup = BeautifulSoup(txt, 'html.parser')
        
        animals_table = self.get_animal_table(soup)  # get the HTML table element containing the list of animal names from the BeautifulSoup object
        animal_th_indx, ca_th_indx = self.get_animal_and_collateral_adjective_th_indexes(tbl=animals_table)  # the column indexes for animal names and collateral adjectives
        
        animals_rows = animals_table.find_all(HtmlElements.tr)[1:]  # skip the header row
        return animals_rows, animal_th_indx, ca_th_indx
    
    def clean_adjectives_list(self, adjectives: List[str]) -> List[str]:
        """clean adjectives strings and drop invalid ones.
            examples: 
                'taurine (male)' -> 'taurine'
                '[d]' -> drop it
        """
        to_ret = []
        for adj in adjectives:
            new_adj = self.clean_string_from_non_letters(adj)
            if new_adj == '':
                continue
            to_ret.append(new_adj)
        return to_ret
    
    def clean_string_from_non_letters(self, name: str) -> str:
        str_to_ret = ''.join(takewhile(lambda char: char.isalpha() or char.isspace(), name))
        return str_to_ret



class WikiAnimalDataHandler:
    
    def extract_wiki_animal_page_text(self, animal: Animal) -> str:
        """Retrieves the text content of the list of animal names from a specified URL."""
        
        url = animal.get_wiki_page_url()
        res = WebExtractor.send_get_request(url=url, attribute_needed=ExecutorProperties.response_att_txt)
        return res

    def get_animal_img_url(self, animal: Animal) -> str:
        txt = None
        try:
            txt = self.extract_wiki_animal_page_text(animal)  # Retrieves the text content of the animal wiki page
        except Exception as e:
            raise Exception(f"{WikiAnimalNamesListDataHandler.FAILED_MSG}, reason: {str(e)}")
        
        soup = BeautifulSoup(txt, 'html.parser')
        # infobox biota
        animal_img_src = soup.find('table',{'class': 'infobox biota'}).find_all('tr')[1:][0].find('img').get('src')
        animal.set_img_src(animal_img_src)
        
        return
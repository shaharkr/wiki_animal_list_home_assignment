from configurator import Configurator
from dal.web_exetractor import WebExtractor
from bs4 import BeautifulSoup, element
from commonStr import ExecutorProperties, WikiDataHandlerProperties, HtmlElements
from typing import Tuple
from itertools import takewhile
import threading
from bll.wiki_animal_handler import WikiAnimalDataHandler

config = Configurator()
        
class WikiAnimalNamesListDataHandler:
    """This class is responsible for managing tasks 
    related to the extraction, parsing, and mapping of animal names and their adjectives from a list."""
    
    FAILED_MSG = 'failed to get list of animals names'
    
    def create_collateral_adjective_to_animal(self) -> dict:
        """
        Parses the list of animal names and their adjectives, creating a dictionary mapping adjectives to corresponding Animal objects and return it.
        Using threads to split the job.
        """
        print(f'{self.__class__.__name__} start prepare meta data')
        animals_rows, animal_th_indx, ca_th_indx = self.__prepare_meta_data_for_parsing()  # prepare data for row animal process
        adjective_to_animals_dict = {}  # the return value
        adjective_to_animals_dict_lock = threading.Lock()  # each thread needs to use adjective_to_animals_dict (read and write).
        
        def process_animal_row(row):
            columns = row.find_all(HtmlElements.td)
            # using the right indexes to get animal data:
                # get the name of the animal
            animal_name_text = columns[animal_th_indx].get_text()
            animal_name = self.__clean_string_from_non_letters(animal_name_text)
                # create the collateral adjective list
            adjectives_text_lst = [adj.get_text(strip=True) for adj in columns[ca_th_indx].contents]  
            adjectives_lst = [self.__clean_string_from_non_letters(adj) 
                              for adj in adjectives_text_lst 
                              if self.__clean_string_from_non_letters(adj) != '']
                # get animal page link extension
            animal_page_link_link_extension = columns[animal_th_indx].find(HtmlElements.a).get(HtmlElements.href)
            
            animal_data_handler = WikiAnimalDataHandler(animal_adjectives=adjectives_lst, animal_name=animal_name, link_extension=animal_page_link_link_extension) 
            
            for adj in adjectives_lst:
                with adjective_to_animals_dict_lock:
                    if adj not in adjective_to_animals_dict:  # first time foud this adjective
                        adjective_to_animals_dict[adj] = []
                    adjective_to_animals_dict[adj].append(animal_data_handler.get_animal())
            try:
                animal_data_handler.download_animal_img()
            except Exception as e:
                print(f'{self.__class__.__name__}: faild to download animal image- {animal_data_handler.get_animal()}')
                
        # split job- execute the rows processing by threads
        threads_lst = []
        print(f'from {self.__class__.__name__}: start processing')
        for row in animals_rows:
            # table is sorted alphabetically by default, these headers represent letters of the alphabet. We want to ignore these row.
            if row.find_all(HtmlElements.th).__len__() == 0:
                thread = threading.Thread(target=process_animal_row, args=(row,))
                thread.start()
                threads_lst.append(thread)
        print(f'from {self.__class__.__name__}: wait for all threads to complete their job. total thread amout- {threads_lst.__len__()}')
        for thread in threads_lst:
            thread.join()  # wait for all threads to complete their job.
        print(f'from {self.__class__.__name__}: finish. total amoit of adjective- {adjective_to_animals_dict.__len__()}')
        return adjective_to_animals_dict
    
    def __prepare_meta_data_for_parsing(self) -> Tuple[list, int, int]:
        """
        Prepares the necessary metadata for parsing, including the list of animal rows and relevant column indexes.
        """
        txt = None
        try:
            txt = self.__extract_wiki_animal_name_list_text()  # Retrieves the text content of the list of animal names from a specified URL
        except Exception as e:
            raise Exception(f"{WikiAnimalNamesListDataHandler.FAILED_MSG}, reason: {str(e)}")
        soup = BeautifulSoup(txt, 'html.parser')
        animals_table = self.__extract_animal_names_table_from_html_tree(soup)  # get the HTML table element containing the list of animal names from the BeautifulSoup object
        animal_th_indx, ca_th_indx = self.__get_animal_and_collateral_adjective_th_indexes(tbl=animals_table)  # the column indexes for animal names and collateral adjectives
        animals_rows = animals_table.find_all(HtmlElements.tr)[1:]  # skip the header row
        return animals_rows, animal_th_indx, ca_th_indx
    
    def __extract_wiki_animal_name_list_text(self) -> str:
        """Retrieves the text content of the list of animal names from a specified URL."""
        url = config.get_wiki_list_of_animals_url()
        res = WebExtractor.send_get_request(url=url, attribute_needed=ExecutorProperties.response_att_txt)
        return res
    
    def __extract_animal_names_table_from_html_tree(self, soup: BeautifulSoup) -> element.Tag:
        """Finds and returns the HTML table element containing the list of animal names from the BeautifulSoup object."""
        title = soup.find(HtmlElements.span,
                          {HtmlElements.id: WikiDataHandlerProperties.id_of_animal_table_title})
        return title.find_next(HtmlElements.table)
    
    def __get_animal_and_collateral_adjective_th_indexes(self, tbl: element.Tag) -> tuple:
        """Retrieves the column indexes for animal names and collateral adjectives from the table header."""
        columns_labels = tbl.find_all(HtmlElements.tr)[0].find_all(HtmlElements.th)  # get the headers row
        animal_idx, c_a_idx = None, None  # animal column index, collaretal adjective column index
        for index, col in enumerate(columns_labels):
            t = col.text  # column title
            if t == WikiDataHandlerProperties.collaretal_adjective_column_label:
                c_a_idx = index
            elif t == WikiDataHandlerProperties.animal_column_label:
                animal_idx = index
            if animal_idx is not None and c_a_idx is not None:
                # finish successfully- found both indexes
                break
        return animal_idx, c_a_idx
    
    def __clean_string_from_non_letters(self, str_to_clean: str) -> str:
        """clean wiki html strings. 
        -Filter out non-letter characters and spaces, remove stop words (example- 'See'/'Also')"""
        str_to_ret = str_to_clean.split('See', 1)[0].split('Also', 1)[0].rstrip()
        str_to_ret = ''.join(takewhile(lambda char: char.isalpha() or char.isspace(), str_to_ret))
        str_to_ret = str_to_ret.split('\n', 1)[0].split('\t', 1)[0].rstrip()
        return str_to_ret
from configurator import Configurator
from animal import Animal
from dal.web_exetractor import WebExtractor
from bs4 import BeautifulSoup, element
from commonStr import ExecutorProperties, WikiDataHandlerProperties, HtmlElements


config = Configurator()
        
class WikiAnimalNamesListDataHandler:
    FAILED_MSG = 'failed to get list of animals names'
    
    def extract_wiki_animal_name_list_text(self) -> str:
        url = config.get_wiki_list_of_animals_url()
        res = WebExtractor.send_get_request(url=url, attribute_needed=ExecutorProperties.response_att_txt)
        return res
    
    def get_animal_table(self, soup: BeautifulSoup) -> element.Tag:
        title = soup.find(HtmlElements.span,
                          {HtmlElements.id: WikiDataHandlerProperties.id_of_tables_title})
        return title.find_next(HtmlElements.table)
    
    def get_animal_and_collateral_adjective_th_indexes(self, tbl: element.Tag):
        columns_labels = tbl.find_all('tr')[0].find_all('th')  # get the headers row
        animal_idx = -1
        c_a_idx = -1
        counter = 0
        for index, cl in enumerate(columns_labels):
            t = cl.text
            if counter == 2:
                break
            if t == 'Collateral adjective':
                animal_idx = index
                counter += 1
            elif t == 'Animal':
                c_a_idx = index
                counter += 1
        return animal_idx, c_a_idx
    
    def create_collateral_adjective_to_animal(self) -> dict:
        txt = None
        try:
            txt = self.extract_wiki_animal_name_list_text()
        except Exception as e:
            raise Exception(f"{WikiAnimalNamesListDataHandler.FAILED_MSG}, reason: {str(e)}")
        
        soup = BeautifulSoup(txt, 'html.parser')
        adjective_to_animals_dict = {}
        
        animals_table = self.get_animals_table(soup)
        animal_th_indx, ca_th_indx = self.get_animal_and_collateral_adjective_th_indexes(tbl=animals_table)
        
        animals_rows = animals_table.find_all(HtmlElements.tr)[1:]  # skip the header row
        
        # iter tables row, each row represent an animal.
        for row in animals_rows:
            if row.find_all(HtmlElements.th).__len__() > 0:
                # table is sorted alphabetically by default, these headers represent letters of the alphabet. We want to ignore these row.
                columns = row.find_all(HtmlElements.td)
                # using the right indexes to get animal data:
                animal_name = columns[animal_th_indx].get_text()  # get the name of the animal
                adjectives = [adj.get_text(strip=True) for adj in columns[ca_th_indx].contents if adj.get_text() != '']  # create the collateral adjective list
                new_animal = Animal(name=animal_name, adjectives=adjectives)
                for adj in adjectives:
                    if adj not in adjective_to_animals_dict:
                        adjective_to_animals_dict[adj] = []
                    adjective_to_animals_dict[adj].append(new_animal)
        return adjective_to_animals_dict
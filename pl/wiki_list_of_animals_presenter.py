from bll.wiki_list_of_animal_handler import WikiAnimalNamesListDataHandler
from pl.html_creator import HtmlCreatorFromDict
from pl.wiki_html_objecs import AdjectiveToAnimalDictTolHtml

class WikiAnimalNamesListPresenter:
    def __init__(self):
        self.handler = WikiAnimalNamesListDataHandler()
        self.adjective_to_animals_dict = None
    
    def __get_adjective_to_animals_dict(self):
        try:
            self.adjective_to_animals_dict = self.handler.create_collateral_adjective_to_animal()
        except Exception as e:
            print()
            
    def output_wiki_adjectives_animals_to_html_file(self, html_file_path, html_file_name):
        if self.adjective_to_animals_dict is None:
            self.__get_adjective_to_animals_dict()
        try:
            html_data_dict = AdjectiveToAnimalDictTolHtml(self.adjective_to_animals_dict)
            HtmlCreatorFromDict.create_html_file_from_html_dict(dict_to_html_obj=html_data_dict, 
                                                                file_path=html_file_path,
                                                                file_name=html_file_name)
        except Exception as e:
            print(f"failed to get create html file. ERROR: {str(e)}")
    
    def present_adjectives_with_animals_data(self):
        """Present the adjectives with corresponding animals data."""
        if self.adjective_to_animals_dict is None:
            self.__get_adjective_to_animals_dict()
        for i, tup in enumerate(self.adjective_to_animals_dict.items()):
            ac, animals = tup[0], tup[1]
            print(f'{i+1}.Collateral Adjective-{ac}\n\tAnimals:')
            for j, animal in enumerate(animals):
                print(f'\t\t{i+1}.{j+1}.{animal}\n')
            print('---------------------')
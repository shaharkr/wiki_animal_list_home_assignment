from bll.wiki_list_of_animal_handler import WikiAnimalNamesListDataHandler
from pl.html_creator import HtmlCreatorFromDict
from pl.htmi_wiki_objects import AdjectiveToAnimalDictTolHtml

class WikiAnimalNamesListPresenter:
    def __init__(self):
        self.handler = WikiAnimalNamesListDataHandler()
        self.adjective_to_animals_dict = None
    
    def __get_adjective_to_animals_dict(self):
        try:
            print(f"from {self.__class__.__name__}: start get adjective_to_animals_dict")
            self.adjective_to_animals_dict = self.handler.create_collateral_adjective_to_animal()
            print(f"from {self.__class__.__name__}: get adjective_to_animals_dict completed.")
        except Exception as e:
            raise Exception(f"from {self.__class__.__name__}: failed to get adjective_to_animals_dict. ERROR: {str(e)}")
            
    def output_wiki_adjectives_animals_to_html_file(self, html_file_path, html_file_name):
        if self.adjective_to_animals_dict is None:
            self.__get_adjective_to_animals_dict()
        try:
            print(f"from {self.__class__.__name__}: start manage HTML output")
            html_data_dict = AdjectiveToAnimalDictTolHtml(self.adjective_to_animals_dict)
            HtmlCreatorFromDict.create_html_file_from_html_dict(dict_to_html_obj=html_data_dict, 
                                                                file_path=html_file_path,
                                                                file_name=html_file_name)
            print(f"from {self.__class__.__name__}: finish manage HTML output")
        except Exception as e:
            raise Exception(f"from {self.__class__.__name__}: failed to get create html file. ERROR: {str(e)}")
    
    def present_adjectives_with_animals_data(self):
        """Present the adjectives with corresponding animals data."""
        print(f"from {self.__class__.__name__}: Start to present data")
        if self.adjective_to_animals_dict is None:
            self.__get_adjective_to_animals_dict()
        for i, tup in enumerate(self.adjective_to_animals_dict.items()):
            ac, animals = tup[0], tup[1]
            print(f'{i+1}.Collateral Adjective-{ac}\n\tAnimals:')
            for j, animal in enumerate(animals):
                print(f'\t\t{i+1}.{j+1}.{animal}\n')
            print('---------------------')
        print(f"from {self.__class__.__name__}: finish to present data")
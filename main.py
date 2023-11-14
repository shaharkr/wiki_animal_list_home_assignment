from bll.wiki_list_of_animal_handler import WikiAnimalNamesListDataHandler
from pl.wiki_list_of_animals_presenter import WikiAnimalNamesListPresenter
from bll.html_creator import HtmlCreator
import os
from configurator import Configurator

config = Configurator()

def main():
    adjective_to_animals_dict = {}
    try:
        handler = WikiAnimalNamesListDataHandler()
        adjective_to_animals_dict = handler.create_collateral_adjective_to_animal()
    except Exception as e:
        print(f"failed to get collateral adjective and animals data. ERROR: {str(e)}")
    
    html_file_path = os.getcwd()
    html_file_name = config.get_html_file_name()
    try:
        HtmlCreator.create_html_for_adjective_to_animals(adjective_to_animals_data_dict=adjective_to_animals_dict, file_path=html_file_path, file_name=html_file_name)
    except Exception as e:
        print(f"failed to get create html file. ERROR: {str(e)}")
    
    presenter = WikiAnimalNamesListPresenter(adjective_to_animals_dict)
    try:
        presenter.present_adjectives_with_animals_data()
    except Exception as e:
        print(f"failed to present data. ERROR: {str(e)}")
        
    
if __name__ == '__main__':
        main()
    
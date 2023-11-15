from pl.wiki_list_of_animals_presenter import WikiAnimalNamesListPresenter
from configurator import Configurator
import os

if __name__ == '__main__':
    presenter = WikiAnimalNamesListPresenter()
    try:
        html_file_path = os.getcwd()
        html_file_name = Configurator().get_html_file_name()
        presenter.output_wiki_adjectives_animals_to_html_file(html_file_path=html_file_path, html_file_name=html_file_name)
        presenter.present_adjectives_with_animals_data()
    except Exception as e:
        print(f"failed to present data. ERROR: {str(e)}")
    
import os

class HtmlCreator:
    def create_html_for_adjective_to_animals(adjective_to_animals_data_dict, file_path, file_name):
        path = os.path.join(file_path, file_name)
        with open(path, 'w') as html_file:
            html_file.write(f"<h1>Total amount of collateral adjectives-{adjective_to_animals_data_dict.__len__()}</h1>")
            for adjective, animals in adjective_to_animals_data_dict.items():
                html_file.write(f"<h2>Animals with the collateral adjective '{adjective}':</h2>")
                for animal in animals:
                    html_file.write(f"<p>{animal.get_name()} -<br><img src={animal.get_img_src()} alt='{animal.get_name()}'></p>")
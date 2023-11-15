import os
from pl.html_objects import DictToHtml

class HtmlCreatorFromDict:
    def create_html_file_from_html_dict(dict_to_html_obj: DictToHtml, file_path: str, file_name: str) -> None:
        path = os.path.join(file_path, file_name)
        with open(path, 'w') as html_file:
            h1 = dict_to_html_obj.get_html_object()
            html_file.write(h1)
            for key_obj, val_obj_lst in dict_to_html_obj.get_data_dict().items():
                html_file.write(key_obj.get_html_object()) 
                for val_obj in val_obj_lst:
                    html_file.write(val_obj.get_html_object())
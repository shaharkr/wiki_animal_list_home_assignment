from pl.html_objects import ObjectToHtml, DictToHtml
from animal import Animal
from typing import Dict, List
from commonStr import HtmlElements

class AnimalHtmlObject(ObjectToHtml):
    """Adapter between ObjectToHtml and Animal"""
    def __init__(self, animal: Animal) -> None:
        super().__init__(e=animal)
        
    def get_html_object(self) -> str:
        name = self.element.get_name()
        img = f"<{HtmlElements.img} {HtmlElements.src}={self.element.get_img_src()} alt='{name}'>"
        title = f"<{HtmlElements.b}>{HtmlElements.dot} {name}<b><br>"
        p = f"<{HtmlElements.p} {HtmlElements.style}='font-family:courier;'>{title}{img}</{HtmlElements.p}>"
        return p

class AdjectivelHtmlObject(ObjectToHtml):
    """Adapter between ObjectToHtml and Adjective string"""
    def __init__(self, adjective: str) -> None:
        super().__init__(e=adjective)
        
    def get_html_object(self) -> str:
        title = f"Animals with the collateral adjective <{HtmlElements.mark}>{self.element}</{HtmlElements.mark}>"
        line = f"<{HtmlElements.h2} {HtmlElements.style}='font-family:courier;'>{title}:</{HtmlElements.h2}>"
        return line


class AdjectiveToAnimalDictTolHtml(DictToHtml):
    """Adapter between DictToHtml and Adjective to Animal dictionary"""
    def __init__(self, adjective_to_animals_dict: Dict[str, List[Animal]]) -> None:
        super().__init__(doc_title=f"Total amount of collateral adjectives -{adjective_to_animals_dict.__len__()}",
                       data_dict=adjective_to_animals_dict)
        
    def _prepare_data_dict(self, data_dict) -> Dict[AdjectivelHtmlObject, List[AnimalHtmlObject]]:
        to_ret = {}
        for adj, animals in data_dict.items():
            html_adj = AdjectivelHtmlObject(adj)
            html_animals_list = [AnimalHtmlObject(animal) for animal in animals]
            to_ret[html_adj] = html_animals_list
        return to_ret
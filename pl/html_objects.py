from commonStr import HtmlElements
from abc import ABC, abstractmethod
from typing import Dict, List

class ObjectToHtml(ABC):
    def __init__(self, e :object) -> None:
        self.element = e
    
    @abstractmethod
    def get_html_object(self) -> str:
        pass
    

class DictToHtml(ObjectToHtml, ABC):
    def __init__(self, doc_title: str, data_dict: dict) -> None:
        self.doc_title = doc_title
        self.data_dict = self._prepare_data_dict(data_dict)
        super().__init__(e=self._prepare_data_dict(data_dict))
    
    @abstractmethod
    def _prepare_data_dict(self, data_dict: dict) -> Dict[ObjectToHtml, List[ObjectToHtml]]:
        pass
    
    def get_data_dict(self):
        return self.data_dict
    
    def get_html_object(self) -> str:
        return f"<{HtmlElements.h1} {HtmlElements.style}='font-family:courier;'><{HtmlElements.ins}>{self.doc_title}</{HtmlElements.ins}></{HtmlElements.h1}>"
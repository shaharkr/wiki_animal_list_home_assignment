from configparser import ConfigParser
from commonStr import DomainConfig, UrlDomainConfig, ExtensionDomainConfig, LocationDomainConfig, RequestsDomainConfig
import json

class Configurator:
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read('config.ini')
    
    def get_wiki_prefix(self):
        return self.parser[DomainConfig.url][UrlDomainConfig.wiki]
    
    def get_animals_img_dir_path(self):
        return self.parser[DomainConfig.location][LocationDomainConfig.animals_imgs_dir]

    def get_wiki_list_of_animals_url(self):
        return self.get_wiki_prefix().format(link_extension=
            self.parser[DomainConfig.extension][ExtensionDomainConfig.wiki_list_of_animals_names])
    
    def get_animal_img_header_request(self):
        txt_dict = self.parser[DomainConfig.requests][RequestsDomainConfig.animal_img_header]
        return json.loads(txt_dict)
from configparser import ConfigParser

class Configurator:
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read('config.ini')
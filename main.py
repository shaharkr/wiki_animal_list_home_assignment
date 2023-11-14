from animal import Animal
from wik_data_extractor import WikiAnimalNamesListDataHandler

if __name__ == '__main__':
    dog = Animal(name='puppy')
    print(dog)
    wde = WikiAnimalNamesListDataHandler()
    dict = wde.create_collateral_adjective_to_animal()
    print(dict)
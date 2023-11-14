
class WikiAnimalNamesListPresenter:
    def __init__(self, adjective_to_animals_dict: dict):
        self.adjective_to_animals_dict = adjective_to_animals_dict
    
    def present_adjectives_with_animals_data(self):
        print(f'Total amount of collateral adjectives-{self.adjective_to_animals_dict.__len__()}\n')
        for i, tup in enumerate(self.adjective_to_animals_dict.items()):
            ac, animals = tup[0], tup[1]
            print(f'{i+1}.Collateral Adjective-{ac}\n\tAnimals:')
            for j, animal in enumerate(animals):
                print(f'\t\t{i+1}.{j+1}.{animal}\n')
            print('---------------------')
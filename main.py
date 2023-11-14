from animal import Animal
from dal.wiki_data_handlers import WikiAnimalNamesListDataHandler, WikiAnimalDataHandler

if __name__ == '__main__':
    
    zebra = Animal(name='Zebra', adjectives=['x'])
    print(zebra)
    wah = WikiAnimalNamesListDataHandler()
    dict = wah.create_collateral_adjective_to_animal()
    for i, tup in enumerate(dict.items()):
        ac, animals = tup[0], tup[1]
        print(f'{i+1}.Collateral Adjective-{ac}\n\tAnimals:')
        for j, animal in enumerate(animals):
            print(f'\t\t{i+1}.{j+1}.{animal}\n')
        print('---------------------')
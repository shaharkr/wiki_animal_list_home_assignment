from dal.wiki_list_of_animal_handler import WikiAnimalNamesListDataHandler
from dal.wiki_animal_handler import WikiAnimalDataHandler
import time

if __name__ == '__main__':
    x = WikiAnimalDataHandler('Dolphin', ['x'], '/wiki/Dolphin')
    dolphin = x.get_animal()
    print(dolphin)
    x.download_animal_img()
    
    
    
    wah = WikiAnimalNamesListDataHandler()
    start_time = time.time()
    dict = wah.create_collateral_adjective_to_animal()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n***********************Time taken: {elapsed_time} seconds********************")
    # for i, tup in enumerate(dict.items()):
    #     ac, animals = tup[0], tup[1]
    #     print(f'{i+1}.Collateral Adjective-{ac}\n\tAnimals:')
    #     for j, animal in enumerate(animals):
    #         print(f'\t\t{i+1}.{j+1}.{animal}\n')
    #     print('---------------------')
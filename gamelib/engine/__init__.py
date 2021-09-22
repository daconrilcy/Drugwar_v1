from gamelib.location import create_location, locations, actual_location
from gamelib.Drug import create_drugs_list, drugs
from gamelib.personna import Personna


def main_engine():
    create_drugs_list()
    create_location()
    actual_location = locations[0]
    to_exit = False

    georges = Personna(name='George')

    print ('Bonjour Georges, bienvenue dans Dope War !')
    print_actual_situation(actual_location)
    while not to_exit:
        rep = input()
        if (rep == 'x') | (rep == 'X'):
            to_exit = True
        elif (rep == 'm') | (rep == 'M'):
            actual_location = mouvement()
            print_actual_situation(actual_location)
        elif (rep == 'b') | (rep == 'B'):
            buy(actual_location)
        elif (rep == 's') | (rep == 'S'):
            sell()
    print('Tchao')


def print_actual_situation(loc):
    print(str(loc.name).upper())
    print('Objets à vendre :')
    print(loc.objects.print_stock_datas())
    print('******************')
    print('Drogues en vente :')
    print(loc.drugs.print_stock_datas())
    print('Quel action veux tu mener ?')
    print("'x' : exit, 'm' : mouvement, 'b': buy, 's': sell")


def mouvement():
    n = 0
    for loc in locations:
        print(str(n) + " : " + loc.name)
        n += 1

    print("tapez le numero de destination")
    new_loc = input()
    if int(new_loc) >= 0 & (int(new_loc) < len(locations)):
        return locations[int(new_loc)]
    else:
        mouvement()


def buy(loc):
    print("buy drug(1) or object(2) ?")
    drop = input()
    if drop == "1":
        "Which drug do you want to buy ?"
        loc.drugs.print_stock_datas()
    if drop == "2":
        "Which object do you want to buy ?"
        loc.objects.print_stock_datas()

    pass


def sell():
    pass

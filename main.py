from blackjack import *


# INITIALISATION

GDict = {
    'nbtour': 0,
    'pioche': [],
    'partieFinie': False
}

JDict = {
    'joueurs': {
        0: {
            'nom': '',
            'type': 0,
            'score': 0,
            'wallet': 100,
            'mise': 0,
            'ingame': True
        },
    },
    'croupier': {
        'score': 0,
        'wallet': 100,
        'mise': 0,
        'ingame': True
    },
    'victoires': {}
}


while True:
    try:
        nbjoueurs = int(input('Nombre de joueurs : '))
    except:
        print("Entrez une valeur correcte")
        continue
    else:
        break

initJoueurs(JDict, nbjoueurs)
# AJOUTER CHOIX DE STRATÉGIES DE JEU
initVictoires(JDict)
initScores(JDict, 'wallet', 100)


# PARTIE COMPLETE

rejouer = True
while rejouer:
    GDict['nbtour'] = 0
    initScores(JDict, 'score')
    GDict['pioche'] = initPioche(nbjoueurs+1)
    initScores(JDict, 'mise')
    initScores(JDict, 'ingame', True)

    # PREMIER TOUR

    premierTour(GDict, JDict)
    partieComplete(GDict, JDict)

    while True:
        rep = input("Voulez vous lancer une nouvelle partie ? (o/n)")
        if rep != 'o' and rep != 'n':
            continue
        else:
            break
    if rep == 'o':
        rejouer = True
    else:
        rejouer = False
    if rejouer:
        voulezVousPartir(JDict)


print("Vous avez terminé, le jeu va maintenant se fermer.")

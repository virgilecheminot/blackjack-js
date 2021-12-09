from blackjack import *


# INITIALISATION

GDict = {
    'pioche': [],
    'stratlist':['alea', 'risk', 'safe', 'intel', 'croupnormal','croupfacile','croupdifficile'],
    'joueurs': {
        0: {
            'nom': 'nomJoueur',
            'type': 0,
            'strat':'strategie',
            'stratmise':['miseAlea','miseFaible','miseForte'],
            'score': 0,
            'wallet': 100,
            'mise': 0,
            'ingame': True,
            'blackjack': False,
            'burst': False
        },
    },
    'croupier': {
        'score': 0,
        'wallet': 0,
        'ingame': True,
        'blackjack': False,
        'burst': False
    },
    'victoires': {}
}


while True:
    try:
        nbjoueurs = int(input('Nombre de joueurs : '))
    except:
        print("Entrez une valeur correcte")
        continue
    if nbjoueurs <= 0:
        continue
    else:
        break

initJoueurs(GDict, nbjoueurs)
# AJOUTER CHOIX DE STRATÉGIES DE JEU
initVictoires(GDict)
initData(GDict, 'wallet', 100)


# PARTIE COMPLETE

rejouer = True
while rejouer:
    initData(GDict, 'score')
    GDict['pioche'] = initPioche(nbjoueurs+1)
    initData(GDict, 'mise')
    initData(GDict, 'ingame', True)
    initData(GDict, 'blackjack', False)
    initData(GDict, 'burst', False)

    # PREMIER TOUR

    premierTour(GDict)
    partieComplete(GDict)

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
        voulezVousPartir(GDict)
        if len(GDict['joueurs']) == 0:
            rejouer = False

print("Résumé des victoires :")
for j in GDict['victoires']:
    print("-", j, ":", GDict['victoires'][j])

print("Vous avez terminé, le jeu va maintenant se fermer.")

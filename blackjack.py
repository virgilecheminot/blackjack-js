## PAQUET DE CARTES ##

from random import *

def paquet():
    return [
        'as de trefle', 'as de carreau', 'as de coeur', 'as de pic',
        '2 de trefle', '2 de carreau', '2 de coeur', 'as de pic',
        '3 de trefle', '3 de carreau', '3 de coeur', '3 de pic',
        '4 de trefle', '4 de carreau', '4 de coeur', '4 de pic',
        '5 de trefle', '5 de carreau', '5 de coeur', '5 de pic',
        '6 de trefle', '6 de carreau', '6 de coeur', '6 de pic', 
        '7 de trefle', '7 de carreau', '7 de coeur', '7 de pic', 
        '8 de trefle', '8 de carreau', '8 de coeur', '8 de pic', 
        '9 de trefle', '9 de carreau', '9 de coeur', '9 de pic', 
        '10 de trefle', '10 de carreau', '10 de coeur', '10 de pic', 
        'valet de trefle', 'valet de carreau', 'valet de coeur', 'valet de pic', 
        'dame de trefle', 'dame de carreau', 'dame de coeur', 'dame de pic', 
        'roi de trefle', 'roi de carreau', 'roi de coeur', 'roi de pic'
    ]

ValCartes = {
    'as' : [1, 11],
    '2' : 2,
    '3' : 3,
    '4' : 4,
    '5' : 5,
    '6' : 6,
    '7' : 7,
    '8' : 8,
    '9' : 9,
    '10' : 10,
    'valet' : 10,
    'dame' : 10,
    'roi' : 10
}

def valeurAs():
    val = int(input("Quelle valeur pour l'as ? (1 ou 11)"))
    if val == 1:
        return 0
    elif val == 11:
        return 1

def initPioche(n):
    pioche = []
    cartes = paquet()
    for i in range(n):
        shuffle(cartes)
        pioche.extend(cartes)
    return pioche

def valeurCartes(carte):
    carte_WO_couleur = carte.split()[0]
    if carte_WO_couleur == 'as':
        return ValCartes['as'][valeurAs()]
    else:
        return ValCartes[carte_WO_couleur]

def piocheCarte(p, x = 1):
    piochees = []
    for i in range(x):
        piochees.append(p.pop(0))
    return piochees
    # pick, p = piocheCarte(initPioche(2), 2)
    # print(pick, len(p))

## JOUEURS ET SCORES

def initJoueurs(n):
    nomsJoueurs = []
    for i in range(n):
        nomsJoueurs.append(input(f'Nom du joueur {i+1} : '))
    return nomsJoueurs

def initScores(joueurs, v=0):
    scores = {}
    for i in range(len(joueurs)):
        scores[joueurs[i]] = v
    return scores

def premierTour(joueurs):
    scores = initScores(joueurs)
    for i in joueurs:
        cartes2 = piocheCarte(initPioche(len(joueurs)), 2)
        for e in cartes2:
            scores[i] += valeurCartes(e)
    return scores

def gagnant(scores):
    scoreMax = 0
    gagnant = ''
    for i in scores:
        if 21 > scores[i] > scoreMax:
            gagnant = i
            scoreMax = scores[i]
        elif scores[i] == 21:
            return i
    return gagnant
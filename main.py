from blackjack import *


## INITIALISATION

nbjoueurs = int(input('Nombre de joueurs : '))
joueurs = initJoueurs(nbjoueurs)
# AJOUTER CHOIX DU TYPE DE JOUEUR
# AJOUTER CHOIX DE STRATÉGIES DE JEU
victoires = initVictoires(joueurs)
# AJOUTER CREATION DU PORTEFEUILLE


## PARTIE COMPLETE

rejouer = True
while rejouer:
    nbtour = 0
    scores = initScores(joueurs)
    joueursEnCours = joueurs.copy()
    pioche = initPioche(len(joueurs))

    ## PREMIER TOUR

    premierTour(joueursEnCours,scores,pioche)
    # PREMIER TOUR ORDINATEUR
    partieComplete(joueursEnCours,nbtour,scores,pioche,victoires)
    if input("Voulez vous lancer une nouvelle partie ? (o/n)") == 'o':
        rejouer = True
    else :
        rejouer = False
print("Vous avez terminé, le jeu va maintenant se fermer.")
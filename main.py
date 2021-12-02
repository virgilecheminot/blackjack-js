from blackjack import *


## INITIALISATION

nbjoueurs = int(input('Nombre de joueurs : '))
joueurs = initJoueurs(nbjoueurs)
# AJOUTER CHOIX DU TYPE DE JOUEUR
# AJOUTER CHOIX DE STRATÉGIES DE JEU
victoires = initScores(joueurs)
portefeuille = initScores(joueurs,100)


## PARTIE COMPLETE

rejouer = True
while rejouer:
    nbtour = 0
    scores = initScores(joueurs)
    joueursEnCours = joueurs.copy()
    pioche = initPioche(len(joueurs))
    mises = initScores(joueurs)

    ## PREMIER TOUR

    premierTour(joueursEnCours,scores,pioche,portefeuille,mises)
    # PREMIER TOUR ORDINATEUR
    partieComplete(joueursEnCours,nbtour,scores,pioche,victoires, portefeuille,mises)
    if input("Voulez vous lancer une nouvelle partie ? (o/n)") == 'o':
        rejouer = True
    else :
        rejouer = False
    if rejouer : voulezVousPartir(joueurs,portefeuille)
print("Vous avez terminé, le jeu va maintenant se fermer.")
## Jeu du Backjack

Ce jeu de Blackjack est un travail de groupe réalisé pour l'université dans le carde d'un projet de fin de semestre en INF101. Le but était de créer un jeu de Blackjack fonctionnel et se rapprochant le plus possible d'un jeu de Blackjack réel. 

Lors de la création du programme nous avons ajouté progressivements certaines fonctionnalités que nous allons détailler ici. La structure choisie a été de créer un fichier [`blackjack.py`](https://github.com/virgilecheminot/blackjack/blob/master/blackjack.py) pour stocker toutes les fonctions de jeu et un autre [`main.py`](https://github.com/virgilecheminot/blackjack/blob/master/main.py) pour les exécuter dans l'ordre.

### Déroulement de base du jeu

Le jeu de Blackjack est un jeu assez simple en soi, donc sa réalisation est plutôt simple à traduire en code. En simplifiant les règles du jeu officiel, nous en avons tiré un déroulement de jeu à peu près similaire à ceci :

- **Initialisation** :
  - Demande du nombre de joueurs
  - Création de la liste des joueurs
  - Choix du type de joueur (humain ou ordinateur)
  - Choix des stratégies de jeu des joueurs ordinateurs
  - Création du portefeuille de chaque joueur à 100 OtterCoins

- **Partie complète :** (tant que rejouer vrai)
  - Scores initialisés à 0 avec la liste des joueurs de base
  - Création de pioche avec nb joueurs × paquet
  - **Premier tour :** (× nb de joueurs)
    - Demande la mise au joueur (si portefeuille non vide)
    - Création de la main initiale des joueurs (2 cartes) & main du croupier
    - Ajout de la main aux scores
    - Affiche nom du joueur
    - Affiche main du joueur
  - **Premier tour ordinateur :**
    - Choix de la mise en fonction de la stratégie choisie
    - Affiche nom du joueur
    - Affiche main du joueur
  - **Tour global :** (× nb de joueurs en jeu)
    - Affiche nom du joueur
    - Affiche main du joueur
    - **Tour joueur :** (tant que je joueur pioche)
      - Propose de continuer à piocher
        - si non : statut "en jeu" du joueur faux → sortir
      - Pioche une carte et lit sa valeur
      - Rajouter valeur de la carte
        - si > 21 → défaite : statut "en jeu" faux
        - si < 21 → continuer
    - **Tour ordinateur :** (tant que le joueur pioche)
      - Choix de continuer ou pas en fonction de la stratégie de jeu
      - Même processus que joueur normal
  - **Tour du croupier :**
    - Tour similaire à un joueur      
  - Vérifier la victoire
  - Répartition des mises en fonction des scores
  - Afficher les vainqueurs
  - Demander pour une nouvelle partie
    - Si oui : demander à chaque joueur humain s'il veut quitter la partie

- **Fin de partie :**
  - Afficher les victoires
  - Afficher les OtterCoins restants dans chaque portefeuille


Les différentes parties distinctes du jeu sont exécutées avec les fonctions suivantes :

- `PremierTour()` : réalise le premier tour
- `partieComplete()` : exécute la fonction `tourComplet()` puis gère la répartition des mises
- `tourComplet()` : éxecute en boucle la fonction `tourJoueur()` pour chaque joueur puis éxecute le tour du croupier

### Structure des données de jeu

L'enjeu majeur de ce programme était de savoir comment stocker les données de jeu et poucoir y accéder facilement avant, durant et après la partie et pouvoir les modifier le plus facilement possible. Pour cela nous avons décidé de nous tourner vers les dictionnaires. Ne pouvant pas utiliser les classes et les objets, les dictionnaires semblaient être la meilleur alternative.

Nous avons donc décidé de rassembler les données en un seul dictionnaire : `GDict` où sont stockées toutes les données liées au jeu en lui-même, par exemple la pioche, l'état de la partie (terminée ou pas), etc. ainsi que toutes les informations liées aux joueurs et au croupier, comme le score actuel, ne nombre de victoires, la mise, etc.

Le dictionnaire prend la forme suivante :

```py
GDict = {
    'pioche': [],
    'joueurs': {
        0: {
            'nom': '',
            'type': 0,
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
```

Les informations liées au joueur comme le score ne sont pas stockées dans un dictionnaire pour chaque, mais dans le dictionnaire personnel du joueur. Cela rallonge quelque peu l'écriture du code mais offre une bien plus grande flexibilité dans l'ajout futur de nouvelles informations.

Les données joueurs sont :

- `nom` : stocke le nom du joueur car la clé du dictionnaire n'est pas le nom mais un index (plus facile pour le déroulement du jeu)
- `type` : stocke le type du joueur : soit humain (0), soit ordinateur (1)
- `score` : stocke le score courant du joueur
- `wallet` : stocke le portefeuille du joueur (initialisé à 100)
- `mise` : stocke la mise courante du joueur
- `ingame` : booléen définissant si le joueur est encore dans la partie et continue à piocher ou non
- `blackjack` : booléen définissant si le joueur a effectué un Blackjack au premier tour (utile pour la répartition des mises)
- `burst` : booléen définissant si le joueur a dépassé ou non le score de 21

À noter que le dictionnaire `victoires` n'est pas dans le dictionnaire du joueur : cela permet de potentiellement exporter le dictionnaire dans un fichier et pouvoir ré afficher le compte de victoires au nouveau lancement du programme.

Pour appeler une donnée dans une fonction particulière, seul les variables `GDict` et `GDict` sont nécessaires dans les paramètres. Une donnée s'appelle comme suit : `GDict['joueurs'][indexDuJoueur][cléDeLaDonnée]`. Les propriétés du dictionnaire permettent donc d'accéder facilement à toutes les données et d'être accédé via une boucle for, par ex :

```py
for j in GDict['joueurs']:
    GDict['joueurs'][j]['scores'] = 0
```

### Les fonctions de jeu

Le fonctionnement du jeu repose sur différentes fonctions créées dans le programme `blackjack.py`. Mise à part les fonctions de déroulement de jeu, elles servent à tout ce qui est gestion du jeu et calcul de différentes variables et données.

- `initPioche(n)` initialise une pioche composée de n paquets de 52 cartes, n étant le nombre de joueurs dans la partie. La pioche est mélangée avant d'être renvoyée grâce à la fonction `shuffle(pioche)`.

- `initJoueurs(GDict, n)` initialise les joueurs et une partie des données le concernant dans le dictionnaire `GDict['joueurs']`. La fonction demande à l'utilisateur : le nom du joueur, son type, et sa stratégie de jeu.

- `initData(GDict, valeur, v=0)` est une fonction multi-usage qui est utilisée pour initialiser notamment les scores, les mises et les portefeuilles des joueurs. Le paramètre `v` est la valeur initialisée (par ex : 0 pour les scores ou 100 pour les portefeuilles).

- `initVictoires(GDict)` est une fonction similaire à la précédente qui ne marche que pour les victoires, comme elles sont dans un dictionnaire à part.

- `valeurCartes(carte, score)` se base sur la chaine de caractère de la carte piochée et un dictionnaire de valeurs pour renvoyer la valeur entière de la carte.

- `valeurAs(score)` prend en compte le score du joueur et renvoie 1 si le score est trop haut ou 11 si le score est inférieur ou égal à 10.

- `piocheCarte(p, x=1)` prend la première carte de la liste `pioche`, la supprime de la pioche et la renvoie. Le paramètre `x` détermine le nombre de cartes à piocher.

- `gagnant(GDict)` détermine les joueurs qui ne perdent pas leur mise à la fin de la partie en cours et renvoie une liste avec les indexs des joueurs.

- `gain(j, GDict)` est une fonction composée d'une série de `if` qui se base sur les règles du jeu pour mettre à jour le portefeuille des joueurs en fonction de leur score (voir la section [Stratégies de choix de la mise](#mises))

### Stratégies de pioche

Les stratégies de pioches sont utilisées pour les joueurs ordinateur ou pour le croupier. Ce sont en fait des fonctions qui déterminent si le joueur doit continuer à piocher ou non, basé sur certains critères. 

- `continueHuman(j, GDict)` est la fonction de base qui interagie avec le joueur pour lui demander s'il veut continuer à piocher ou pas

- `continueAlea(j,GDict)` ne prend aucun critère en compte et donne juste au hasard une réponse positive ou négative avec une probabilité de 0.5. C'est la forme la moins "intelligente" des fonctions de choix :
```py
def continueAlea(j,GDict):
    if choice([False, True]):
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")
```

- `continuePara(j,GDict,p=0.5)` est similaire à la fonction précédente, mais les choix ont une probabilité différente (même si la probabilité par défaut est 0.5, ce qui revient à exactement la fonction précédente). Ce choix pondéré est effectué grâce au module numpy.random :
```py
def continuePara(j,GDict,p=0.5):
    if nprd.choice([False, True], p=[1-p, p]):
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")
```

- `continueIntel(j,GDict,p=0.5)` se base sur le score du joueur pour en tirer une probabilité qui est en suite injectée dans `continuePara()`. C'est la technique la plus "complexe" car elle rassemble le plus de paramètres, mais ça n'es pas forcément la plus logique ni la meilleure stratégie :
```py
def continueIntel(j,GDict):
    if GDict['joueurs'][j]['score'] <= 10:
        p = 1
    elif GDict['joueurs'][j]['score'] < 21:
        p = 1-((GDict['joueurs'][j]['score']-11)/10)
    else:
        p = 0
    continuePara(j,GDict,p)
```
- `continueCroupier(j,GDict)` est la méthode utilisée dans la plupart des casinos quand il s'agit de faire piocher le croupier. Tant que son score est inférieur à 17, le croupier continue à piocher, sinon il s'arrête :
```py
def continueCroupier(j,GDict):
    if GDict['croupier']['score'] < 17:
        GDict['croupier']['ingame'] = True
    else:
        GDict['croupier']['ingame'] = False
        print("\nLe croupier ne pioche pas")
```
- `continueCroupNormal(GDict)` est la même methode utilisé dans la fonction précédente, cependant elle est appliquée à un joueur qui voudrait jouer comme le croupier :
```py
def continueCroupNormal(j, GDict):
    if GDict['joueurs'][j]['score'] < 17:
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")
```
- `continueCroupFacil(j,GDict)`est la fonction qui definit un joueur qui ne pioche au dessus d'une certaine valeur de main:
```py
def continueCroupFacil(j, GDict):
    if GDict['joueurs'][j]['score'] < 15:
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")
```
- `continueCroupDifficile(j,GDict)`fonctionne comme celle au dessus mais avec un nombre de main plus grand avant d'arreter de piocher :
```py
def continueCroupDifficile(j, GDict):
    if GDict['joueurs'][j]['score'] < 19:
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")
```
### <a name="mises"></a> Stratégies de choix de la mise

Le fonctionnement des mises demandé ne correspond pas du tout au fonctionnement des mises du Blackjack classique, faisant jouer les joueurs contre eux et non contre le croupier. C'est pourquoi nous avons décidé de revoir le système avec les règles suivantes :

- Le croupier ne mise pas et comme il représente le casino, il a une ressource "infinie" d'OtterCoins

- Si le joueur dépasse, il perd sa mise instantanément sa mise qui va au croupier

- Si le joueur fait blackjack en un coup, il gagne 1,5 fois sa mise, sauf si le croupier fait aussi blackjack en un coup, au quel cas le joueur est payé à égalité

- Si le joueur a une main supérieure au croupier, il est payé à égalité, c'est à dire qu'il récupère sa mise et gagne la valeur de sa mise

- Si le croupier dépasse, il paye toutes les mains encore en jeu à égalité

- Si le joueur est a égalité avec le croupier, la main est considérée comme nulle et le joueur récupère juste sa mise

De même que les stratégie de pioche, les stratégies de mises peuvent être choisies au moment de l'inscription du joueur ordinateur dans le dictionnaire. Elles déterminenent donc combien d'OtterCoins le joueur va miser en fonction de différents critères.

- `choixMise(score)` se base sur le score du joueur et mise un pourcentage du portefeuille en fonction de ce dernier. Si le score du joueur après le premier tour est trop bas, le pourcentage va être faible, s'il se raproche de 10 ou 11, et donc du la possibilité de faire blackjack, le pourcentage est élevé :
```py
def choixMise(score):
    if score <= 10:
        p = score/10
    elif score < 21:
        p = 1-((score-11)/10)
    elif score == 21:
        p = 1
    return p
```

### Tournoi automatique et comparaison des stratégies

(partie à venir)

### Interface graphique du jeu 
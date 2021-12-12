//////////////////////
// FONCTIONS DE JEU //
//////////////////////

function fermer() {
    if (confirm('Voulez-vous vraiment quitter ?')) {
        window.close();
    }
}

var GDict = {
    'pioche': [],
    'stratlist': ['alea', 'risk', 'safe', 'intel', 'croupNormal', 'croupFacile', 'croupDiff'],
    'stratmiselist': ['miseAlea', 'miseFaible', 'miseForte'],
    'joueurs': {},
    'croupier': {
        'score': 0,
        'main': [],
        'wallet': 0,
        'ingame': true,
        'blackjack': false,
        'burst': false
    },
    'victoires': {}
};

const couleurs = ['pique', 'trèfle', 'cœur', 'carreau'];
const values = ['As', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi'];

const valCartes = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'Valet': 10,
    'Dame': 10,
    'Roi': 10
};

function paquet() {
    let paquet = [];
    couleurs.forEach(c => {
        values.forEach(v => {
            paquet.push(v + ' de ' + c);
        });
    });
    return paquet;
}

function initPioche() {
    let pioche = [];
    for (let i = 0; i < Object.keys(GDict['joueurs']).length; i++) {
        pioche = pioche.concat(paquet());
    }
    return pioche;
}

function valeurCartes(carte, score) {
    const carteVal = carte.split(' ')[0];
    if (carteVal == 'As') {
        return valeurAs(score);
    } else {
        return valCartes[carteVal];
    }
}

function valeurAs(score) {
    if (score + 11 <= 21) {
        return 11;
    } else {
        return 1;
    }
}

function piocheCarte(pioche, x = 1) {
    let piochées = [];
    for (let i = 0; i < x; i++) {
        piochées.push(pioche.pop());
    }
    return piochées;
}

///////////////
// MAIN MENU //
///////////////

function loadMainMenu() {
    var playerList = document.getElementById("player-list");
    var victoryList = document.getElementById("victory-list");
    playerList.innerHTML = '';
    victoryList.innerHTML = '';
    if (Object.keys(GDict['joueurs']).length == 0) {
        document.getElementById('remove-player-button').disabled = true;
        playerList.appendChild(document.createTextNode("Pas de joueurs"));
    } else {
        document.getElementById('remove-player-button').disabled = false;
        for (const joueur of Object.entries(GDict['joueurs'])) {
            if (GDict['joueurs'][joueur]['type'] == '1') {
                var str = joueur + " (ordinateur)";
            } else {
                var str = joueur;
            }
            const li = document.createElement("li");
            li.appendChild(document.createTextNode(str));
            playerList.appendChild(li);
        };
    }
    if (Object.keys(GDict['victoires']).length == 0) {
        victoryList.appendChild(document.createTextNode("Aucune victoire"));
    } else {
        for (const [joueur, vic] of Object.entries(GDict['victoires'])) {
            const li = document.createElement("li");
            li.appendChild(document.createTextNode(joueur + " : " + vic));
            victoryList.appendChild(li);
        };
    }
    document.getElementById('landingpage').classList.remove('hidden');
}

function openChoixMises() {
    if (Object.keys(GDict['joueurs']).length == 0) {
        window.alert("Vous devez ajouter des joueurs");
    } else {
        document.getElementById('landingpage').classList.add('hidden');
        loadChoixMises();
    }
}

function openRemovePlayer() {
    document.getElementById('landingpage').classList.add('hidden');
    loadRemovePlayer();
}

function openNewPlayer() {
    document.getElementById('landingpage').classList.add('hidden');
    loadCreatePlayer();
};

///////////////////
// REMOVE PLAYER //
///////////////////

function loadRemovePlayer() {
    var playerSelect = document.getElementById("player-list-select");
    playerSelect.innerHTML = '';
    for (const joueur of Object.entries(GDict['joueurs'])) {
        const opt = document.createElement("option");
        opt.value = joueur;
        opt.text = joueur;
        playerSelect.add(opt, null);
    }
    document.getElementById('removeplayer').classList.remove('hidden');
}

function removePlayer() {
    var playerSelected = document.getElementById("player-list-select").value;
    if (confirm("Voulez-vous vraiment retirer " + playerSelected + " ?")) {
        delete GDict['joueurs'][playerSelected];
        removeReturnToMenu();
    }
}

function removeReturnToMenu() {
    document.getElementById('removeplayer').classList.add('hidden');
    loadMainMenu();
}

///////////////////
// CREATE PLAYER //
///////////////////

function loadCreatePlayer() {
    document.getElementById('name').value = '';
    document.getElementById('createplayer').classList.remove('hidden');
}

function stoppedTypingCreate() {
    if (document.getElementById("name").value.length > 0) {
        document.getElementById("confirm-add-player-button").disabled = false;
    } else {
        document.getElementById("confirm-add-player-button").disabled = true;
    }
}

function stratOnChange() {
    if (document.getElementById('type').value == '0') {
        document.getElementById('strat').disabled = true;
        document.getElementById('stratmise').disabled = true;
    } else {
        document.getElementById('strat').disabled = false;
        document.getElementById('stratmise').disabled = false;
    }
}

function addPlayer() {
    var name = document.getElementById('name').value;
    if (Object.keys(GDict['joueurs']).includes(name)) {
        window.alert("Le nom est déjà pris, veuillez en entrer un autre");
    } else {
        var type = document.getElementById('type').value;
        var strat = document.getElementById('strat').value;
        var stratmise = document.getElementById('stratmise').value;
        GDict['joueurs'][name] = {};
        GDict['joueurs'][name]['type'] = type;
        if (type == '1') {
            GDict['joueurs'][name]['strat'] = strat;
            GDict['joueurs'][name]['stratmise'] = stratmise;
        };
        GDict['joueurs'][name]['score'] = 0;
        GDict['joueurs'][name]['main'] = [];
        GDict['joueurs'][name]['wallet'] = 100;
        GDict['joueurs'][name]['mise'] = 0;
        GDict['joueurs'][name]['ingame'] = true;
        GDict['joueurs'][name]['blackjack'] = false;
        GDict['joueurs'][name]['burst'] = false;
        createReturnToMenu();
    }
}

function createReturnToMenu() {
    document.getElementById('createplayer').classList.add('hidden');
    loadMainMenu();
}

/////////////////////
// CHOIX DES MISES //
/////////////////////

function loadChoixMises() {
    var listMise = document.getElementById("mises-list");
    listMise.innerHTML = '';
    for (const joueur of Object.entries(GDict['joueurs'])) {
        GDict['joueurs'][joueur]['mise'] = 0;
        var idstr = joueur + "-input-mises";
        var div = document.createElement('div');
        var label = document.createElement('label');
        var input = document.createElement('input');
        label.setAttribute("for", idstr);
        label.innerHTML = joueur + " :";
        input.setAttribute('type', 'text');
        input.id = idstr;
        input.setAttribute('size', '5');
        input.onchange = function () { stoppedTypingMises(idstr); };
        input.value = '';
        div.appendChild(label);
        div.appendChild(input);
        listMise.appendChild(div);
        if (GDict['joueurs'][joueur]['type'] == '1') {
            var mise = choixMisesOrdi(GDict['joueurs'][joueur]['stratmise'], GDict['joueurs'][joueur]['wallet']);
            input.value = mise;
            input.disabled = true;
        }
        stoppedTypingMises(idstr);
    }
    document.getElementById('choixmises').classList.remove('hidden');
}


function choixMisesOrdi(strat, wallet) {
    switch (strat) {
        case 'miseAlea':
            return miseAlea(wallet);
        case 'miseFaible':
            return miseFaible(wallet);
        case 'miseForte':
            return miseForte(wallet);
        default:
            console.log('erreur choix mise');
    }
}


function miseAlea(wallet) {
    let mise = Math.floor(Math.random() * Math.floor(wallet)) + 1;
    return mise;
}


function miseFaible(wallet) {
    let mise = Math.floor(Math.random() * Math.floor(wallet)) + 1;
    while (mise > (0.25 * wallet)) {
        mise = Math.floor(Math.random() * Math.floor(wallet)) + 1;
    }
    return mise;
}


function miseForte(wallet) {
    let mise = Math.floor(Math.random() * Math.floor(wallet)) + 1;
    while (mise < (0.75 * wallet)) {
        mise = Math.floor(Math.random() * Math.floor(wallet)) + 1;
    }
    return mise;
}


function stoppedTypingMises(input_id) {
    if (document.getElementById(input_id).value.length > 0) {
        document.getElementById('first-round-button').disabled = false;
    } else {
        document.getElementById('first-round-button').disabled = true;
    }
}

function misesReturnToMenu() {
    document.getElementById('choixmises').classList.add('hidden');
    loadMainMenu();
}

function openFirstRound() {
    for (const joueur of Object.entries(GDict['joueurs'])) {
        var idstr = joueur + "-input-mises";
        const mise = parseInt(document.getElementById(idstr).value);
        if (!Number.isInteger(mise) || mise > GDict['joueurs'][joueur]['wallet'] || mise < 1) {
            window.alert('Mise de ' + joueur + ' incorrecte');
            return;
        }
    }
    for (const [joueur] of Object.entries(GDict['joueurs'])) {
        var idstr = joueur + "-input-mises";
        const mise = parseInt(document.getElementById(idstr).value);
        GDict['joueurs'][joueur]['mise'] = mise;
        GDict['joueurs'][joueur]['wallet'] -= mise;
    }
    document.getElementById('choixmises').classList.add('hidden');
    loadPremierTour();
}

//////////////////
// PREMIER TOUR //
//////////////////

function loadPremierTour() {
    var scoreZone = document.getElementById('player-score-zone');
    scoreZone.innerHTML = '';

    GDict['pioche'] = initPioche();

    for (const joueur of Object.entries(GDict['joueurs'])) {
        GDict['joueurs'][joueur]['score'] = 0;
        GDict['joueurs'][joueur]['ingame'] = true;
        GDict['joueurs'][joueur]['blackjack'] = false;
        GDict['joueurs'][joueur]['burst'] = false;
        GDict['joueurs'][joueur]['main'] = [];

        var idstr = joueur + "-score-zone";
        var div = document.createElement('div');
        var label = document.createElement('label');
        var p = document.createElement('p');
        label.setAttribute("for", idstr);
        label.innerHTML = joueur + " :";
        p.id = idstr;
        // p.innerHTML = premierTour(joueur);
        div.appendChild(label);
        div.appendChild(p);
        scoreZone.appendChild(div);
    }
    GDict['croupier']['score'] = 0;
    GDict['croupier']['ingame'] = true;
    GDict['croupier']['blackjack'] = false;
    GDict['croupier']['burst'] = false;
    GDict['croupier']['main'] = [];
    // document.getElementById('coupier-score-first').innerHTML = premierTourCroup();

    document.getElementById('premiertour').classList.remove('hidden');
}
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
        'wallet': 0,
        'ingame': true,
        'blackjack': false,
        'burst': false
    },
    'victoires': {}
};

// MAIN MENU

function loadMainMenu() {
    var playerList = document.getElementById("player-list");
    var victoryList = document.getElementById("victory-list");
    playerList.innerHTML = '';
    victoryList.innerHTML = '';
    if (Object.keys(GDict['joueurs']).length == 0) {
        document.getElementById('remove-player-button').disabled = true;
        playerList.appendChild(document.createTextNode("Pas de joueurs"))
    } else {
        document.getElementById('remove-player-button').disabled = false;
        for (const [joueur] of Object.entries(GDict['joueurs'])) {
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
        victoryList.appendChild(document.createTextNode("Aucune victoire"))
    } else {
        for (const [joueur, vic] of Object.entries(GDict['victoires'])) {
            const li = document.createElement("li");
            li.appendChild(document.createTextNode(joueur + " : " + vic))
            victoryList.appendChild(li)
        };
    }
    document.getElementById('landingpage').classList.remove('hidden');
}

function openChoixMises() {
    if (Object.keys(GDict['joueurs']).length == 0) {
        window.alert("Vous devez ajouter des joueurs")
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


// REMOVE PLAYER

function loadRemovePlayer() {
    var playerSelect = document.getElementById("player-list-select");
    playerSelect.innerHTML = '';
    for (const [joueur] of Object.entries(GDict['joueurs'])) {
        const opt = document.createElement("option");
        opt.value = joueur
        opt.text = joueur
        playerSelect.add(opt, null)
    }
    document.getElementById('removeplayer').classList.remove('hidden');
}

function removePlayer() {
    var playerSelected = document.getElementById("player-list-select").value;
    if (confirm("Voulez-vous vraiment retirer " + playerSelected + " ?")) {
        delete GDict['joueurs'][playerSelected]
        removeReturnToMenu();
    }
}

function removeReturnToMenu() {
    document.getElementById('removeplayer').classList.add('hidden');
    loadMainMenu();
}


// CREATE PLAYER

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
    var type = document.getElementById('type').value;
    var strat = document.getElementById('strat').value;
    var stratmise = document.getElementById('stratmise').value;
    GDict['joueurs'][name] = {};
    GDict['joueurs'][name]['type'] = type;
    if (type == '1') {
        GDict['joueurs'][name]['strat'] = strat;
        GDict['joueurs'][name]['stratmise'] = stratmise;
    };
    GDict['joueurs'][name]['score'] = 0
    GDict['joueurs'][name]['wallet'] = 100;
    GDict['joueurs'][name]['mise'] = 0;
    GDict['joueurs'][name]['ingame'] = true;
    GDict['joueurs'][name]['blackjack'] = false;
    GDict['joueurs'][name]['burst'] = false;
    createReturnToMenu();
}

function createReturnToMenu() {
    document.getElementById('createplayer').classList.add('hidden');
    loadMainMenu();
}

// NEW GAME

function loadChoixMises() {
    var listMise = document.getElementById("mises-list");
    listMise.innerHTML = '';
    for (const[joueur] of Object.entries(GDict['joueurs'])) {
        var idstr = joueur + "-input-mises"
        var div = document.createElement('div');
        var label = document.createElement('label');
        var input = document.createElement('input');
        label.setAttribute("for", idstr);
        label.innerHTML = joueur + " :";
        input.setAttribute('type', 'text');
        input.id = idstr;
        input.setAttribute('size', '5')
        if (GDict['joueurs'][joueur]['type'] == '1') {
            input.disabled = true;
            // Ajouter choix des mises
        }
        input.onkeyup = function(){stoppedTypingMises(idstr)};
        div.appendChild(label);
        div.appendChild(input);
        listMise.appendChild(div);

        // GDict['joueurs'][joueur]['score'] = 0;
        GDict['joueurs'][joueur]['mise'] = 0;
        // GDict['joueurs'][joueur]['ingame'] = true;
        // GDict['joueurs'][joueur]['blackjack'] = false;
        // GDict['joueurs'][joueur]['burst'] = false;
    }
    document.getElementById('choixmises').classList.remove('hidden')
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
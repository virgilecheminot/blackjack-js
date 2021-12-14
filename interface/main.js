//////////////////////
// FONCTIONS DE JEU //
//////////////////////

function fermer() {
    if (confirm("Voulez-vous vraiment quitter ?")) {
        window.close();
    }
}

var GDict = {
    pioche: [],
    stratlist: [
        "alea",
        "risk",
        "safe",
        "intel",
        "croupNormal",
        "croupFacile",
        "croupDiff",
    ],
    stratmiselist: ["miseAlea", "miseFaible", "miseForte"],
    joueurs: {},
    croupier: {
        score: 0,
        main: [],
        wallet: 0,
        ingame: true,
        blackjack: false,
        burst: false,
    },
    victoires: {},
    playlist: [],
};

var cheatMode = false;

const couleurs = ["pique", "trèfle", "cœur", "carreau"];
const values = [
    "As",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Valet",
    "Dame",
    "Roi",
];

const valCartes = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    Valet: 10,
    Dame: 10,
    Roi: 10,
};

function paquet() {
    let paquet = [];
    couleurs.forEach((c) => {
        values.forEach((v) => {
            paquet.push(v + " de " + c);
        });
    });
    return paquet;
}

function initPioche() {
    let pioche = [];
    for (let i = 0; i < Object.keys(GDict["joueurs"]).length; i++) {
        pioche = pioche.concat(paquet());
    }
    const mélange = (array) => {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            const temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }
    };
    mélange(pioche);
    return pioche;
}

function valeurCartes(carte, score) {
    const carteVal = carte.split(" ")[0];
    if (carteVal == "As") {
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
    playerList.innerHTML = "";
    victoryList.innerHTML = "";
    if (Object.keys(GDict["joueurs"]).length == 0) {
        document.getElementById("remove-player-button").disabled = true;
        playerList.appendChild(document.createTextNode("Pas de joueurs"));
    } else {
        document.getElementById("remove-player-button").disabled = false;
        for (const [joueur] of Object.entries(GDict["joueurs"])) {
            if (GDict["joueurs"][joueur]["type"] == "1") {
                var str =
                    joueur +
                    " (ordinateur) - " +
                    GDict["joueurs"][joueur]["wallet"] +
                    " OC";
            } else {
                var str =
                    joueur + " - " + GDict["joueurs"][joueur]["wallet"] + " OC";
            }
            const li = document.createElement("li");
            li.appendChild(document.createTextNode(str));
            playerList.appendChild(li);
        }
    }
    if (Object.keys(GDict["victoires"]).length == 0) {
        victoryList.appendChild(document.createTextNode("Aucune victoire"));
    } else {
        for (const [joueur, vic] of Object.entries(GDict["victoires"])) {
            const li = document.createElement("li");
            li.appendChild(document.createTextNode(joueur + " : " + vic));
            victoryList.appendChild(li);
        }
    }
    document.getElementById("landingpage").classList.remove("hidden");
}

function openChoixMises() {
    if (Object.keys(GDict["joueurs"]).length == 0) {
        window.alert("Vous devez ajouter des joueurs");
    } else {
        document.getElementById("landingpage").classList.add("hidden");
        loadChoixMises();
    }
}

function openRemovePlayer() {
    document.getElementById("landingpage").classList.add("hidden");
    loadRemovePlayer();
}

function openNewPlayer() {
    document.getElementById("landingpage").classList.add("hidden");
    loadCreatePlayer();
}

///////////////////
// REMOVE PLAYER //
///////////////////

function loadRemovePlayer() {
    var playerSelect = document.getElementById("player-list-select");
    playerSelect.innerHTML = "";
    for (const [joueur] of Object.entries(GDict["joueurs"])) {
        const opt = document.createElement("option");
        opt.value = joueur;
        opt.text = joueur;
        playerSelect.add(opt, null);
    }
    document.getElementById("removeplayer").classList.remove("hidden");
}

function removePlayer() {
    var playerSelected = document.getElementById("player-list-select").value;
    if (confirm("Voulez-vous vraiment retirer " + playerSelected + " ?")) {
        delete GDict["joueurs"][playerSelected];
        removeReturnToMenu();
    }
}

function removeReturnToMenu() {
    document.getElementById("removeplayer").classList.add("hidden");
    loadMainMenu();
}

///////////////////
// CREATE PLAYER //
///////////////////

function loadCreatePlayer() {
    document.getElementById("name").value = "";
    document.getElementById("createplayer").classList.remove("hidden");
}

function stoppedTypingCreate() {
    if (document.getElementById("name").value.length > 0) {
        document.getElementById("confirm-add-player-button").disabled = false;
    } else {
        document.getElementById("confirm-add-player-button").disabled = true;
    }
}

function stratOnChange() {
    if (document.getElementById("type").value == "0") {
        document.getElementById("strat").disabled = true;
        document.getElementById("stratmise").disabled = true;
    } else {
        document.getElementById("strat").disabled = false;
        document.getElementById("stratmise").disabled = false;
    }
}

function addPlayer() {
    var name = document.getElementById("name").value;
    if (Object.keys(GDict["joueurs"]).includes(name)) {
        window.alert("Le nom est déjà pris, veuillez en entrer un autre");
    } else {
        var type = document.getElementById("type").value;
        var strat = document.getElementById("strat").value;
        var stratmise = document.getElementById("stratmise").value;
        GDict["joueurs"][name] = {};
        GDict["joueurs"][name]["type"] = type;
        if (type == "1") {
            GDict["joueurs"][name]["strat"] = strat;
            GDict["joueurs"][name]["stratmise"] = stratmise;
        }
        GDict["joueurs"][name]["score"] = 0;
        GDict["joueurs"][name]["main"] = [];
        GDict["joueurs"][name]["wallet"] = 100;
        GDict["joueurs"][name]["mise"] = 0;
        GDict["joueurs"][name]["ingame"] = true;
        GDict["joueurs"][name]["blackjack"] = false;
        GDict["joueurs"][name]["burst"] = false;
        createReturnToMenu();
    }
}

function createReturnToMenu() {
    document.getElementById("createplayer").classList.add("hidden");
    loadMainMenu();
}

/////////////////////
// CHOIX DES MISES //
/////////////////////

function loadChoixMises() {
    var listMise = document.getElementById("mises-list");
    listMise.innerHTML = "";
    for (const [joueur] of Object.entries(GDict["joueurs"])) {
        if (GDict["joueurs"][joueur]["wallet"] < 1) {
            delete GDict["joueurs"][joueur];
        } else {
            GDict["joueurs"][joueur]["mise"] = 0;
            var idstr = joueur + "-input-mises";
            var div = document.createElement("div");
            var label = document.createElement("label");
            var input = document.createElement("input");
            label.setAttribute("for", idstr);
            label.innerHTML = joueur + " (" + GDict['joueurs'][joueur]['wallet'] + " OC) :";
            input.setAttribute("type", "text");
            input.id = idstr;
            input.setAttribute("size", "5");
            input.onchange = function () {
                stoppedTypingMises(idstr);
            };
            input.value = "";
            div.style = "display: flex; margin: 0.5rem";
            div.appendChild(label);
            div.appendChild(input);
            listMise.appendChild(div);
            if (GDict["joueurs"][joueur]["type"] == "1") {
                var mise = choixMisesOrdi(
                    GDict["joueurs"][joueur]["stratmise"],
                    GDict["joueurs"][joueur]["wallet"]
                );
                input.value = mise;
                input.disabled = true;
            }
            stoppedTypingMises(idstr);
        }
    }
    document.getElementById("choixmises").classList.remove("hidden");
}

function choixMisesOrdi(strat, wallet) {
    switch (strat) {
        case "miseAlea":
            return miseAlea(wallet);
        case "miseFaible":
            return miseFaible(wallet);
        case "miseForte":
            return miseForte(wallet);
        default:
            console.log("erreur choix mise");
    }
}

function miseAlea(wallet) {
    let mise = Math.floor(Math.random() * Math.floor(wallet)) + 1;
    return mise;
}

function miseFaible(wallet) {
    let mise = Math.floor(Math.random() * Math.floor(wallet)) + 1;
    while (mise > 0.25 * wallet) {
        mise = Math.floor(Math.random() * Math.floor(wallet)) + 1;
    }
    return mise;
}

function miseForte(wallet) {
    let mise = Math.floor(Math.random() * Math.floor(wallet)) + 1;
    while (mise < 0.75 * wallet) {
        mise = Math.floor(Math.random() * Math.floor(wallet)) + 1;
    }
    return mise;
}

function stoppedTypingMises(input_id) {
    if (document.getElementById(input_id).value.length > 0) {
        document.getElementById("first-round-button").disabled = false;
    } else {
        document.getElementById("first-round-button").disabled = true;
    }
}

function misesReturnToMenu() {
    document.getElementById("choixmises").classList.add("hidden");
    loadMainMenu();
}

function openFirstRound() {
    for (const [joueur] of Object.entries(GDict["joueurs"])) {
        var idstr = joueur + "-input-mises";
        const mise = parseInt(document.getElementById(idstr).value);
        if (
            !Number.isInteger(mise) ||
            mise > GDict["joueurs"][joueur]["wallet"] ||
            mise < 1
        ) {
            window.alert("Mise de " + joueur + " incorrecte");
            return;
        }
    }
    for (const [joueur] of Object.entries(GDict["joueurs"])) {
        var idstr = joueur + "-input-mises";
        const mise = parseInt(document.getElementById(idstr).value);
        GDict["joueurs"][joueur]["mise"] = mise;
        GDict["joueurs"][joueur]["wallet"] -= mise;
    }
    document.getElementById("choixmises").classList.add("hidden");
    GDict["playlist"] = Object.keys(GDict["joueurs"]);
    loadPremierTour();
}

//////////////////
// PREMIER TOUR //
//////////////////

function loadPremierTour() {
    var scoreZone = document.getElementById("player-score-zone");
    scoreZone.innerHTML = "";

    GDict["pioche"] = initPioche();

    for (const [joueur] of Object.entries(GDict["joueurs"])) {
        GDict["joueurs"][joueur]["score"] = 0;
        GDict["joueurs"][joueur]["ingame"] = true;
        GDict["joueurs"][joueur]["blackjack"] = false;
        GDict["joueurs"][joueur]["burst"] = false;
        GDict["joueurs"][joueur]["main"] = [];

        var idstr = joueur + "-score-zone";
        var div = document.createElement("div");
        var h3 = document.createElement("h3");
        var p = document.createElement("p");
        var phand = document.createElement("p");
        h3.innerHTML = joueur + " :";
        p.id = idstr;
        p.innerHTML = premierTour(joueur);
        main = GDict["joueurs"][joueur]["main"];
        handStr = "";
        for (let i = 0; i < main.length - 1; i++) {
            const element = main[i];
            handStr += element + ", ";
        }
        handStr += main[main.length - 1];
        phand.innerHTML = handStr;
        div.appendChild(h3);
        div.appendChild(p);
        div.appendChild(phand);
        scoreZone.appendChild(div);
    }
    GDict["croupier"]["score"] = 0;
    GDict["croupier"]["ingame"] = true;
    GDict["croupier"]["blackjack"] = false;
    GDict["croupier"]["burst"] = false;
    GDict["croupier"]["main"] = [];
    document.getElementById("coupier-score-first").innerHTML =
        premierTourCroup();
    main = GDict["croupier"]["main"];
    handStr = "";
    for (let i = 0; i < main.length - 1; i++) {
        const element = main[i];
        handStr += element + ", ";
    }
    handStr += main[main.length - 1];
    document.getElementById("main-croup-first").innerHTML = handStr;

    document.getElementById("premiertour").classList.remove("hidden");
}

function premierTour(joueur) {
    let cartes2 = piocheCarte(GDict["pioche"], 2);
    var returnStr = "";
    for (const key in cartes2) {
        if (Object.hasOwnProperty.call(cartes2, key)) {
            GDict["joueurs"][joueur]["score"] += valeurCartes(
                cartes2[key],
                GDict["joueurs"][joueur]["score"]
            );
            GDict["joueurs"][joueur]["main"].push(cartes2[key]);
        }
    }
    returnStr += GDict["joueurs"][joueur]["score"];
    if (GDict["joueurs"][joueur]["score"] == 21) {
        GDict["joueurs"][joueur]["blackjack"] = true;
        GDict["joueurs"][joueur]["ingame"] = false;
        returnStr += " Blackjack !";
    }
    return returnStr;
}

function premierTourCroup() {
    let cartes2 = piocheCarte(GDict["pioche"], 2);
    var returnStr = "";
    for (const key in cartes2) {
        if (Object.hasOwnProperty.call(cartes2, key)) {
            GDict["croupier"]["score"] += valeurCartes(
                cartes2[key],
                GDict["croupier"]["score"]
            );
            GDict["croupier"]["main"].push(cartes2[key]);
        }
    }
    returnStr += GDict["croupier"]["score"];
    if (GDict["croupier"]["score"] == 21) {
        GDict["croupier"]["blackjack"] = true;
        GDict["croupier"]["ingame"] = false;
        returnStr += " : Blackjack !";
    }
    return returnStr;
}

function openTourJoueur() {
    document.getElementById("premiertour").classList.add("hidden");
    loadTourJoueur();
}

//////////////////
// TOUR JOUEURS //
//////////////////

var playerindex;

function loadTourJoueur() {
    playerindex = 0;
    document.getElementById("tourjoueur").classList.remove("hidden");
    tourJoueur();
}

function tourJoueur() {
    document.getElementById("rester-button").classList.add("hidden");
    document.getElementById("piocher-button").classList.add("hidden");
    document.getElementById("suivant-ordi-button").classList.add("hidden");
    document.getElementById("title-tour-joueur").innerHTML =
        "Tour de " + GDict["playlist"][playerindex];
    listeAutres = document.getElementById("list-score-autres");
    listeAutres.innerHTML = "";
    for (const [j] of Object.entries(GDict["joueurs"])) {
        if (j != GDict["playlist"][playerindex]) {
            var idstr = j + "-score-autres";
            var li = document.createElement("li");
            li.id = idstr;
            var spanT = document.createElement("span");
            var spanS = document.createElement("span");
            var spanM = document.createElement("span");
            spanT.innerHTML = j + " : ";
            spanS.innerHTML = GDict["joueurs"][j]["score"] + " ";
            main = GDict["joueurs"][j]["main"];
            handStr = "";
            for (let i = 0; i < main.length - 1; i++) {
                const element = main[i];
                handStr += element + ", ";
            }
            handStr += main[main.length - 1];
            spanM.innerHTML = " - " + handStr;
            li.appendChild(spanT);
            li.appendChild(spanS);
            li.appendChild(spanM);
            listeAutres.appendChild(li);
        }
    }
    var li = document.createElement("li");
    li.id = "croup-score-autres";
    var spanT = document.createElement("span");
    var spanS = document.createElement("span");
    var spanM = document.createElement("span");
    spanT.innerHTML = "Croupier : ";
    spanS.innerHTML = GDict["croupier"]["score"] + " ";
    main = GDict["croupier"]["main"];
    handStr = "";
    for (let i = 0; i < main.length - 1; i++) {
        const element = main[i];
        handStr += element + ", ";
    }
    handStr += main[main.length - 1];
    spanM.innerHTML = " - " + handStr;
    li.appendChild(spanT);
    li.appendChild(spanS);
    li.appendChild(spanM);
    listeAutres.appendChild(li);

    scoreStr = GDict["joueurs"][GDict["playlist"][playerindex]]["score"];
    if (GDict["joueurs"][GDict["playlist"][playerindex]]["burst"]) {
        scoreStr += " Perdu !";
    }
    document.getElementById("score-joueur").innerHTML = scoreStr;

    if (
        GDict["joueurs"][GDict["playlist"][playerindex]]["type"] == "1" &&
        GDict["joueurs"][GDict["playlist"][playerindex]]["ingame"]
    ) {
        document.getElementById("rester-button").classList.add("hidden");
        document.getElementById("piocher-button").classList.add("hidden");
        tourOrdinateur();
    } else if (!GDict["joueurs"][GDict["playlist"][playerindex]]["ingame"]) {
        document.getElementById("rester-button").classList.add("hidden");
        document.getElementById("piocher-button").classList.add("hidden");
        document
            .getElementById("suivant-ordi-button")
            .classList.remove("hidden");
    } else if (GDict["joueurs"][GDict["playlist"][playerindex]]["ingame"]) {
        document.getElementById("rester-button").classList.remove("hidden");
        document.getElementById("piocher-button").classList.remove("hidden");
        document.getElementById("suivant-ordi-button").classList.add("hidden");
    } else {
        document.getElementById("rester-button").classList.add("hidden");
        document.getElementById("piocher-button").classList.add("hidden");
        document
            .getElementById("suivant-ordi-button")
            .classList.remove("hidden");
    }
}

function tourCroupier() {
    continueCroupier();
    while (GDict["croupier"]["ingame"]) {
        let carte = piocheCarte(GDict["pioche"])[0];
        GDict["croupier"]["main"].push(carte);
        GDict["croupier"]["score"] += valeurCartes(
            carte,
            GDict["croupier"]["score"]
        );
        if (GDict["croupier"]["score"] == 21) {
            GDict["croupier"]["ingame"] = false;
        } else if (GDict["croupier"]["score"] > 21) {
            GDict["croupier"]["ingame"] = false;
            GDict["croupier"]["burst"] = true;
        } else {
            continueCroupier();
        }
    }

    document.getElementById("title-tour-joueur").innerHTML =
        "Tour de du croupier";
    listeAutres = document.getElementById("list-score-autres");
    listeAutres.innerHTML = "";
    for (const [j] of Object.entries(GDict["joueurs"])) {
        var idstr = j + "-score-autres";
        var li = document.createElement("li");
        li.id = idstr;
        var spanT = document.createElement("span");
        var spanS = document.createElement("span");
        var spanM = document.createElement("span");
        spanT.innerHTML = j + " : ";
        spanS.innerHTML = GDict["joueurs"][j]["score"] + " ";
        main = GDict["joueurs"][j]["main"];
        handStr = "";
        for (let i = 0; i < main.length - 1; i++) {
            const element = main[i];
            handStr += element + ", ";
        }
        handStr += main[main.length - 1];
        spanM.innerHTML = " - " + handStr;
        li.appendChild(spanT);
        li.appendChild(spanS);
        li.appendChild(spanM);
        listeAutres.appendChild(li);
    }

    scoreStr = GDict["croupier"]["score"];
    if (GDict["croupier"]["burst"]) {
        scoreStr += " Perdu !";
    }
    document.getElementById("score-joueur").innerHTML = scoreStr;
    document.getElementById("rester-button").classList.add("hidden");
    document.getElementById("piocher-button").classList.add("hidden");
    document.getElementById("suivant-ordi-button").classList.remove("hidden");
}

function continueCroupier() {
    const score = GDict["croupier"]["score"];
    if (score < 17) {
        GDict["croupier"]["ingame"] = true;
    } else {
        GDict["croupier"]["ingame"] = false;
    }
}

function piocherHumain() {
    const joueur = GDict["playlist"][playerindex];
    let carte = piocheCarte(GDict["pioche"])[0];
    GDict["joueurs"][joueur]["main"].push(carte);
    GDict["joueurs"][joueur]["score"] += valeurCartes(
        carte,
        GDict["joueurs"][joueur]["score"]
    );
    if (GDict["joueurs"][joueur]["score"] == 21) {
        GDict["joueurs"][joueur]["ingame"] = false;
    } else if (GDict["joueurs"][joueur]["score"] > 21) {
        GDict["joueurs"][joueur]["ingame"] = false;
        GDict["joueurs"][joueur]["burst"] = true;
    }
    tourJoueur();
}

function tourOrdinateur() {
    const joueur = GDict["playlist"][playerindex];
    selectContinue(joueur);
    var cont = GDict["joueurs"][joueur]["ingame"];
    while (cont == true) {
        let carte = piocheCarte(GDict["pioche"])[0];
        GDict["joueurs"][joueur]["main"].push(carte);
        GDict["joueurs"][joueur]["score"] += valeurCartes(
            carte,
            GDict["joueurs"][joueur]["score"]
        );
        if (GDict["joueurs"][joueur]["score"] == 21) {
            GDict["joueurs"][joueur]["ingame"] = false;
        } else if (GDict["joueurs"][joueur]["score"] > 21) {
            GDict["joueurs"][joueur]["ingame"] = false;
            GDict["joueurs"][joueur]["burst"] = true;
        } else {
            selectContinue(joueur);
        }
        cont = GDict["joueurs"][joueur]["ingame"];
    }
    document.getElementById("suivant-ordi-button").classList.remove("hidden");
    tourJoueur();
}

function selectContinue(joueur) {
    const strat = GDict["joueurs"][joueur]["strat"];
    switch (strat) {
        case "alea":
            continueAlea(joueur);
            break;
        case "risk":
            continuePara(joueur, 0.8);
            break;
        case "safe":
            continuePara(joueur, 0.2);
            break;
        case "intel":
            continueIntel(joueur);
            break;
        case "croupNormal":
            continueCroupNormal(joueur);
            break;
        case "croupFacile":
            continueCroupFacile(joueur);
            break;
        case "croupDiff":
            continueCroupDifficile(joueur);
            break;
        default:
            console.log("erreur choix pioche");
            break;
    }
}

function continueAlea(joueur) {
    var choice = Math.random() < 0.5 ? true : false;
    if (choice) {
        GDict["joueurs"][joueur]["ingame"] = true;
    } else {
        GDict["joueurs"][joueur]["ingame"] = false;
    }
}

function continuePara(joueur, p) {
    var choice = Math.random() < p ? true : false;
    if (choice) {
        GDict["joueurs"][joueur]["ingame"] = true;
    } else {
        GDict["joueurs"][joueur]["ingame"] = false;
    }
}

function continueIntel(joueur) {
    const score = GDict["joueurs"][joueur]["score"];
    var p;
    if (score <= 10) {
        p = 1;
    } else if (score < 21) {
        p = 1 - (score - 11) / 10;
    } else {
        p = 0;
    }
    continuePara(joueur, p);
}

function continueCroupNormal(joueur) {
    const score = GDict["joueurs"][joueur]["score"];
    if (score < 17) {
        GDict["joueurs"][joueur]["ingame"] = true;
    } else {
        GDict["joueurs"][joueur]["ingame"] = false;
    }
}

function continueCroupFacile(joueur) {
    const score = GDict["joueurs"][joueur]["score"];
    if (score < 16) {
        GDict["joueurs"][joueur]["ingame"] = true;
    } else {
        GDict["joueurs"][joueur]["ingame"] = false;
    }
}

function continueCroupDifficile(joueur) {
    const score = GDict["joueurs"][joueur]["score"];
    if (score < 19) {
        GDict["joueurs"][joueur]["ingame"] = true;
    } else {
        GDict["joueurs"][joueur]["ingame"] = false;
    }
}

function rester() {
    if (playerindex >= GDict["playlist"].length - 1) {
        tourCroupier();
        playerindex += 1;
    } else if (playerindex >= GDict["playlist"].length) {
        openResumePartie();
    } else {
        const joueur = GDict["playlist"][playerindex];
        GDict["joueurs"][joueur]["ingame"] = false;
        playerindex += 1;
        tourJoueur();
    }
}

function suivant() {
    if (playerindex == GDict["playlist"].length - 1) {
        tourCroupier();
        playerindex += 1;
    } else if (playerindex >= GDict["playlist"].length) {
        openResumePartie();
    } else {
        const joueur = GDict["playlist"][playerindex];
        GDict["joueurs"][joueur]["ingame"] = false;
        playerindex += 1;
        tourJoueur();
    }
}

function openResumePartie() {
    document.getElementById("tourjoueur").classList.add("hidden");
    loadResume();
}

///////////////////
// RÉSUMÉ PARTIE //
///////////////////

function loadResume() {
    var scoreZone = document.getElementById("player-score-zone-resume");
    var scoreZoneCroup = document.getElementById("croupier-score-zone-resume");
    scoreZoneCroup.innerHTML = "";
    scoreZone.innerHTML = "";

    for (const [joueur] of Object.entries(GDict["joueurs"])) {
        if (cheatMode && joueur.toLowerCase() == "virgile") {
            GDict["joueurs"]["Virgile"]["score"] = 21;
            GDict["joueurs"][joueur]["blackjack"] = true;
            GDict["joueurs"][joueur]["burst"] = false;
        }
        var idstr = joueur + "-score-zone-resume";
        var div = document.createElement("div");
        var h3 = document.createElement("h3");
        var p = document.createElement("p");
        var phand = document.createElement("p");
        var pgain = document.createElement("p");
        h3.innerHTML = joueur + " :";

        div.id = idstr;

        scoreStr = "Score : " + GDict["joueurs"][joueur]["score"];
        if (GDict["joueurs"][joueur]["blackjack"]) {
            scoreStr += " - Blackjack !";
        } else if (GDict["joueurs"][joueur]["burst"]) {
            scoreStr += " - Dépassé...";
        }
        p.innerHTML = scoreStr;

        main = GDict["joueurs"][joueur]["main"];
        handStr = "Main : ";
        for (let i = 0; i < main.length - 1; i++) {
            const element = main[i];
            handStr += element + ", ";
        }
        handStr += main[main.length - 1];
        phand.innerHTML = handStr;

        pgain.innerHTML = "Gain : " + gain(joueur) + " OC";

        div.appendChild(h3);
        div.appendChild(p);
        div.appendChild(phand);
        div.appendChild(pgain);
        scoreZone.appendChild(div);
    }
    var h3 = document.createElement("h3");
    var p = document.createElement("p");
    var phand = document.createElement("p");
    h3.innerHTML = "Croupier :";

    scoreStr = "Score : " + GDict["croupier"]["score"];
    if (GDict["croupier"]["blackjack"]) {
        scoreStr += " - Blackjack !";
    } else if (GDict["croupier"]["burst"]) {
        scoreStr += " - Dépassé...";
    }
    p.innerHTML = scoreStr;

    main = GDict["croupier"]["main"];
    handStr = "Main : ";
    for (let i = 0; i < main.length - 1; i++) {
        const element = main[i];
        handStr += element + ", ";
    }
    handStr += main[main.length - 1];
    phand.innerHTML = handStr;

    scoreZoneCroup.appendChild(h3);
    scoreZoneCroup.appendChild(p);
    scoreZoneCroup.appendChild(phand);

    document.getElementById("resumepartie").classList.remove("hidden");
}

function gain(joueur) {
    const mise = GDict["joueurs"][joueur]["mise"];
    const score = GDict["joueurs"][joueur]["score"];
    const blackjack = GDict["joueurs"][joueur]["blackjack"];
    const burst = GDict["joueurs"][joueur]["burst"];
    var gain = 0;

    if (cheatMode && joueur.toLowerCase() == "virgile") {
        GDict["joueurs"]["Virgile"]["wallet"] += 1000;
    }

    if (burst) {
        GDict["croupier"]["wallet"] += mise;
        gain -= mise;
    } else if (GDict["croupier"]["burst"]) {
        if (blackjack) {
            GDict["joueurs"][joueur]["wallet"] += 2.5 * mise;
            GDict["croupier"]["wallet"] -= 1.5 * mise;
            gain += 1.5 * mise;
        } else {
            GDict["joueurs"][joueur]["wallet"] += 2 * mise;
            GDict["croupier"]["wallet"] -= mise;
            gain += mise;
        }
    } else if (GDict["croupier"]["blackjack"]) {
        if (blackjack) {
            GDict["joueurs"][joueur]["wallet"] += 2 * mise;
            GDict["croupier"]["wallet"] -= mise;
            gain += mise;
        } else {
            GDict["croupier"]["wallet"] += mise;
            gain -= mise;
        }
    } else {
        if (blackjack) {
            GDict["joueurs"][joueur]["wallet"] += 2.5 * mise;
            GDict["croupier"]["wallet"] -= 1.5 * mise;
            gain += 1.5 * mise;
        } else if (score > GDict["croupier"]["score"]) {
            GDict["joueurs"][joueur]["wallet"] += 2 * mise;
            GDict["croupier"]["wallet"] -= mise;
            gain += mise;
        } else if (score == GDict["croupier"]["score"]) {
            GDict["joueurs"][joueur]["wallet"] += mise;
        } else {
            GDict["croupier"]["wallet"] += mise;
            gain -= mise;
        }
    }
    if (gain >= 0) {
        if (!(joueur in GDict["victoires"])) {
            GDict["victoires"][joueur] = 0;
        }
        GDict["victoires"][joueur] += 1;
    }
    return gain;
}

function returnToMenu() {
    document.getElementById("resumepartie").classList.add("hidden");
    clearData();
    loadMainMenu();
}

function clearData() {
    for (const [joueur] of Object.entries(GDict["joueurs"])) {
        GDict["joueurs"][joueur]["score"] = 0;
        GDict["joueurs"][joueur]["main"] = [];
        GDict["joueurs"][joueur]["mise"] = 0;
        GDict["joueurs"][joueur]["ingame"] = true;
        GDict["joueurs"][joueur]["blackjack"] = false;
        GDict["joueurs"][joueur]["burst"] = false;
        if (GDict["joueurs"][joueur]["wallet"] < 1) {
            delete GDict["joueurs"][joueur];
        }
    }
    GDict["croupier"]["score"] = 0;
    GDict["croupier"]["main"] = [];
    GDict["croupier"]["ingame"] = true;
    GDict["croupier"]["blackjack"] = false;
    GDict["croupier"]["burst"] = false;
}

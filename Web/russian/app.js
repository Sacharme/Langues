// ============== DICTIONARY LOADING ==============
// Dictionaries embedded from text files - loaded at startup
const DICT_COMPLETE_URL = '../../Dictionnaires/russian.txt';
const DICT_SAMPLE_URL = '../../Dictionnaires/russian_sample.txt';

let motsFrancais = [];
let motsRusses = [];

// ============== STATE ==============
let dictionnaire = 2;      // 1=complet, 2=échantillon
let trainingType = 1;       // 0=mixte, 1=traduction, 2=conjugaison, 3=révision
let verbMode = 2;           // 0=tous, 1=irréguliers, 2=réguliers

let modeActuel = null;
let bonneReponse = null;
let verbeChoisi = null;
let pronomIndex = null;
let genreIndex = null;
let tempsChoisi = null;
let indexAleatoire = null;

let totalQuestions = 0;
let correctAnswers = 0;

// Revision state
let revisionQueue = [];
let revisionErrors = [];
let revisionCurrentIdx = 0;
let revisionRound = 0;

let isWaiting = false;

// ============== DOM ELEMENTS ==============
const feedbackOverlay = document.getElementById('feedbackOverlay');
const correctAnswerEl = document.getElementById('correctAnswer');
const revisionInfoEl = document.getElementById('revisionInfo');
const questionTranslation = document.getElementById('questionTranslation');
const questionConjugation = document.getElementById('questionConjugation');
const wordDisplay = document.getElementById('wordDisplay');
const conjIrregular = document.getElementById('conjIrregular');
const conjVerb = document.getElementById('conjVerb');
const conjTense = document.getElementById('conjTense');
const conjPronoun = document.getElementById('conjPronoun');
const answerInput = document.getElementById('answerInput');
const validateBtn = document.getElementById('validateBtn');
const scorePercentage = document.getElementById('scorePercentage');
const scoreDetail = document.getElementById('scoreDetail');
const dictBtn = document.getElementById('dictBtn');
const dictStatus = document.getElementById('dictStatus');
const trainingBtn = document.getElementById('trainingBtn');
const trainingStatus = document.getElementById('trainingStatus');
const verbBtn = document.getElementById('verbBtn');
const verbStatus = document.getElementById('verbStatus');
const questionArea = document.getElementById('questionArea');

// ============== LOAD DICTIONARY ==============
async function loadDictionary(type) {
    const url = type === 1 ? DICT_COMPLETE_URL : DICT_SAMPLE_URL;
    try {
        const resp = await fetch(url);
        const text = await resp.text();
        motsFrancais = [];
        motsRusses = [];
        for (const line of text.split('\n')) {
            const trimmed = line.trim();
            if (trimmed.includes('%')) {
                const parts = trimmed.split(' % ');
                if (parts.length === 2) {
                    motsFrancais.push(parts[0].trim());
                    motsRusses.push(parts[1].trim());
                }
            }
        }
        if (motsFrancais.length === 0) {
            motsFrancais.push("Erreur");
            motsRusses.push("Dictionnaire vide");
        }
    } catch (e) {
        motsFrancais = ["Erreur"];
        motsRusses = ["Fichier introuvable"];
    }
}

// ============== TEXT NORMALIZATION ==============
function normaliserTexte(texte) {
    return texte.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
}

// ============== RANDOM HELPERS ==============
function randInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
function randChoice(arr) {
    return arr[randInt(0, arr.length - 1)];
}

// ============== UPDATE UI ==============
function updateStatuts() {
    if (dictionnaire === 1) {
        dictStatus.textContent = "Complet";
        dictStatus.className = "control-status dict-complet";
    } else {
        dictStatus.textContent = "Échantillon";
        dictStatus.className = "control-status dict-sample";
    }

    if (trainingType === 0) {
        trainingStatus.textContent = "Mixte (25/75)";
        trainingStatus.className = "control-status train-mixte";
    } else if (trainingType === 1) {
        trainingStatus.textContent = "Traduction";
        trainingStatus.className = "control-status train-trad";
    } else if (trainingType === 2) {
        trainingStatus.textContent = "Conjugaison";
        trainingStatus.className = "control-status train-conj";
    } else {
        trainingStatus.textContent = "Révision";
        trainingStatus.className = "control-status train-revision";
    }

    if (verbMode === 1) {
        verbStatus.textContent = "Irréguliers";
        verbStatus.className = "control-status verb-irreg";
    } else if (verbMode === 2) {
        verbStatus.textContent = "Réguliers";
        verbStatus.className = "control-status verb-reg";
    } else {
        verbStatus.textContent = "Tous";
        verbStatus.className = "control-status verb-all";
    }
}

function updateScore() {
    if (totalQuestions > 0) {
        const pct = (correctAnswers / totalQuestions * 100).toFixed(1);
        scorePercentage.textContent = `${pct}%`;
        scoreDetail.textContent = `${correctAnswers}/${totalQuestions}`;
    } else {
        scorePercentage.textContent = "0%";
        scoreDetail.textContent = "0/0";
    }
}

// ============== QUESTION GENERATION ==============
function nouvelleQuestion() {
    answerInput.value = '';
    answerInput.disabled = false;
    validateBtn.disabled = false;
    correctAnswerEl.className = 'correct-answer';
    correctAnswerEl.textContent = '';
    revisionInfoEl.textContent = '';
    isWaiting = false;

    // Animate question area
    questionArea.style.animation = 'none';
    questionArea.offsetHeight; // trigger reflow
    questionArea.style.animation = 'slideIn 0.35s cubic-bezier(0.4, 0, 0.2, 1)';

    if (trainingType === 3) {
        modeActuel = 'revision';
        genererQuestionRevision();
        answerInput.focus();
        return;
    }

    if (trainingType === 0) {
        modeActuel = Math.random() < 0.25 ? 'conjugaison' : 'traduction';
    } else if (trainingType === 1) {
        modeActuel = 'traduction';
    } else {
        modeActuel = 'conjugaison';
    }

    if (modeActuel === 'traduction') {
        genererQuestionTraduction();
    } else {
        genererQuestionConjugaison();
    }
    answerInput.focus();
}

function genererQuestionTraduction() {
    indexAleatoire = randInt(0, motsFrancais.length - 1);
    bonneReponse = motsRusses[indexAleatoire];

    questionTranslation.classList.remove('hidden');
    questionConjugation.classList.add('hidden');
    wordDisplay.textContent = motsFrancais[indexAleatoire];
}

function initRevision() {
    revisionQueue = Array.from({ length: motsFrancais.length }, (_, i) => i);
    revisionErrors = [];
    revisionCurrentIdx = 0;
    revisionRound = 1;
    totalQuestions = 0;
    correctAnswers = 0;
    updateScore();
}

function genererQuestionRevision() {
    if (revisionQueue.length === 0) initRevision();

    if (revisionCurrentIdx >= revisionQueue.length) {
        if (revisionErrors.length > 0) {
            revisionQueue = [...revisionErrors];
            revisionErrors = [];
            revisionCurrentIdx = 0;
            revisionRound++;
        } else {
            // Revision complete
            questionTranslation.classList.remove('hidden');
            questionConjugation.classList.add('hidden');
            wordDisplay.textContent = `Révision terminée !\n${correctAnswers}/${totalQuestions}`;
            wordDisplay.style.color = '#2bc46c';
            bonneReponse = null;
            validateBtn.disabled = true;
            answerInput.disabled = true;
            return;
        }
    }

    const wordIndex = revisionQueue[revisionCurrentIdx];
    bonneReponse = motsRusses[wordIndex];
    indexAleatoire = wordIndex;

    questionTranslation.classList.remove('hidden');
    questionConjugation.classList.add('hidden');

    const position = revisionCurrentIdx + 1;
    const total = revisionQueue.length;
    const tourInfo = revisionRound > 1 ? `Tour ${revisionRound} — ` : '';
    revisionInfoEl.textContent = `${tourInfo}${position}/${total}`;
    wordDisplay.textContent = motsFrancais[wordIndex];
    wordDisplay.style.color = '';
}

function genererQuestionConjugaison() {
    let tousVerbes;
    if (verbMode === 1) tousVerbes = verbesIrreguliers;
    else if (verbMode === 2) tousVerbes = [...verbes1ereConj, ...verbes2emeConj];
    else tousVerbes = [...verbes1ereConj, ...verbes2emeConj, ...verbesIrreguliers];

    verbeChoisi = randChoice(tousVerbes);
    tempsChoisi = randChoice(temps);

    let genreChoisi;

    if (tempsChoisi === "passé") {
        genreIndex = randInt(0, genresPasse.length - 1);
        pronomIndex = 0;
        genreChoisi = genresPasse[genreIndex];
        bonneReponse = conjuguerVerbe(verbeChoisi, pronomIndex, tempsChoisi, genreIndex);
    } else if (tempsChoisi === "participe passé") {
        genreIndex = randInt(0, genresParticipe.length - 1);
        pronomIndex = 0;
        genreChoisi = genresParticipe[genreIndex];
        bonneReponse = conjuguerVerbe(verbeChoisi, pronomIndex, tempsChoisi, genreIndex);
    } else if (tempsChoisi === "impératif") {
        genreIndex = null;
        const pronomChoisi = randChoice(["ty", "vy"]);
        pronomIndex = pronoms.indexOf(pronomChoisi);
        bonneReponse = conjuguerVerbe(verbeChoisi, pronomIndex, tempsChoisi);
    } else {
        genreIndex = null;
        const pronomChoisi = randChoice(pronoms);
        pronomIndex = pronoms.indexOf(pronomChoisi);
        bonneReponse = conjuguerVerbe(verbeChoisi, pronomIndex, tempsChoisi);
    }

    questionTranslation.classList.add('hidden');
    questionConjugation.classList.remove('hidden');

    if (verbesIrreguliers.includes(verbeChoisi)) {
        conjIrregular.classList.remove('hidden');
    } else {
        conjIrregular.classList.add('hidden');
    }

    const trad = traductionsVerbes[verbeChoisi] || '';
    conjVerb.textContent = trad ? `${verbeChoisi} (${trad})` : verbeChoisi;
    conjTense.textContent = tempsChoisi;

    if (tempsChoisi === "passé" || tempsChoisi === "participe passé") {
        conjPronoun.textContent = genreChoisi;
    } else {
        conjPronoun.textContent = pronoms[pronomIndex];
    }
}

// ============== ANSWER VERIFICATION ==============
function evaluerTraduction(reponse) {
    const idx = motsRusses.indexOf(reponse);
    if (idx === indexAleatoire) return "succes";

    const repNorm = normaliserTexte(reponse);
    const bonNorm = normaliserTexte(bonneReponse);
    if (repNorm === bonNorm) return "presque";
    return "echec";
}

function verifierReponse() {
    if (isWaiting) return;

    let reponseUtilisateur = answerInput.value.trim();
    if (!reponseUtilisateur) return;

    // Cyrillic detection and conversion
    if (isCyrillic(reponseUtilisateur)) {
        reponseUtilisateur = cyrillicToLatin(reponseUtilisateur);
    }

    let resultat;

    if (modeActuel === 'revision') {
        resultat = evaluerTraduction(reponseUtilisateur);
        if (resultat === "echec") {
            const wordIndex = revisionQueue[revisionCurrentIdx];
            if (!revisionErrors.includes(wordIndex)) {
                revisionErrors.push(wordIndex);
            }
        }
        revisionCurrentIdx++;
    } else if (modeActuel === 'traduction') {
        resultat = evaluerTraduction(reponseUtilisateur);
    } else {
        if (reponseUtilisateur.toLowerCase() === bonneReponse.toLowerCase()) {
            resultat = "succes";
        } else {
            const repNorm = normaliserTexte(reponseUtilisateur);
            const bonNorm = normaliserTexte(bonneReponse);
            resultat = repNorm === bonNorm ? "presque" : "echec";
        }
    }

    afficherResultat(resultat);

    answerInput.value = '';
    // answerInput.disabled = true; // Désactivé pour garder le clavier ouvert sur mobile
    validateBtn.disabled = true;
    isWaiting = true;

    setTimeout(nouvelleQuestion, 750);
}

function afficherResultat(resultat) {
    totalQuestions++;
    if (resultat === "succes" || resultat === "presque") correctAnswers++;
    updateScore();

    // Clear previous feedback
    feedbackOverlay.className = 'feedback-overlay';

    if (resultat === "succes") {
        feedbackOverlay.classList.add('show', 'success');
        correctAnswerEl.textContent = 'Juste !';
        correctAnswerEl.className = 'correct-answer visible success-text';
    } else if (resultat === "presque") {
        feedbackOverlay.classList.add('show', 'warning');
        correctAnswerEl.textContent = `Bonne réponse : ${bonneReponse}`;
        correctAnswerEl.className = 'correct-answer visible warning-text';
    } else {
        feedbackOverlay.classList.add('show', 'error');
        correctAnswerEl.textContent = `Bonne réponse : ${bonneReponse}`;
        correctAnswerEl.className = 'correct-answer visible error-text';
        questionArea.classList.add('shake');
        setTimeout(() => questionArea.classList.remove('shake'), 400);
    }
}

// ============== CONTROL HANDLERS ==============
dictBtn.addEventListener('click', async () => {
    dictionnaire = dictionnaire === 1 ? 2 : 1;
    await loadDictionary(dictionnaire);
    updateStatuts();
    if (trainingType === 3) initRevision();
    nouvelleQuestion();
});

trainingBtn.addEventListener('click', () => {
    trainingType = (trainingType + 1) % 4;
    if (trainingType === 3) initRevision();
    totalQuestions = 0;
    correctAnswers = 0;
    updateScore();
    updateStatuts();
    nouvelleQuestion();
});

verbBtn.addEventListener('click', () => {
    verbMode = (verbMode + 1) % 3;
    totalQuestions = 0;
    correctAnswers = 0;
    updateScore();
    updateStatuts();
    nouvelleQuestion();
});

// ============== INPUT HANDLERS ==============
answerInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        verifierReponse();
    }
});

validateBtn.addEventListener('mousedown', (e) => {
    // Empêche le bouton de prendre le focus et de fermer le clavier
    e.preventDefault();
});

validateBtn.addEventListener('click', (e) => {
    verifierReponse();
    // S'assure que le focus reste sur l'input
    answerInput.focus();
});

// ============== BACKGROUND PARTICLES ==============
function createParticles() {
    const container = document.getElementById('bgParticles');
    for (let i = 0; i < 12; i++) {
        const p = document.createElement('div');
        p.className = 'particle';
        const size = Math.random() * 4 + 2;
        p.style.width = size + 'px';
        p.style.height = size + 'px';
        p.style.left = Math.random() * 100 + '%';
        p.style.animationDuration = (Math.random() * 15 + 10) + 's';
        p.style.animationDelay = (Math.random() * 10) + 's';
        p.style.opacity = Math.random() * 0.3 + 0.1;
        container.appendChild(p);
    }
}

// ============== INIT ==============
async function init() {
    createParticles();
    await loadDictionary(dictionnaire);
    updateStatuts();
    updateScore();
    nouvelleQuestion();
}

init();

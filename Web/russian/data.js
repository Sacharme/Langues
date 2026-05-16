// ============== CYRILLIC TO LATIN MAPPING ==============
const CYRILLIC_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
    'е': 'ye', 'ё': 'yo', 'ж': 'j', 'з': 'z', 'и': 'i',
    'й': 'î', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
    'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
    'у': 'ou', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
    'ш': 'sh', 'щ': 'shsh', 'ъ': '"', 'ы': 'y', 'ь': "'",
    'э': 'e', 'ю': 'yu', 'я': 'ya'
};

function isCyrillic(text) {
    return /[а-яёА-ЯЁ]/.test(text);
}

function cyrillicToLatin(text) {
    let result = '';
    for (const ch of text.toLowerCase()) {
        result += CYRILLIC_MAP[ch] !== undefined ? CYRILLIC_MAP[ch] : ch;
    }
    return result;
}

// ============== VERB TRANSLATIONS ==============
const traductionsVerbes = {
    "dyelat'": "faire", "znat'": "savoir", "doumat'": "penser",
    "rabotat'": "travailler", "jdat'": "attendre", "pisat'": "écrire",
    "tchitat'": "lire", "otvyetchat'": "répondre", "pokoupat'": "acheter",
    "prodavat'": "vendre", "ponimat'": "comprendre", "pokazyvat'": "montrer",
    "ostanavlivat'": "arrêter", "zabyvat'": "oublier", "vybirat'": "choisir",
    "myenyat'": "changer", "pomogat'": "aider", "prinimat'": "prendre (une douche, un taxi)",
    "imyet'": "avoir", "khodit'": "marcher", "vidyet'": "voir",
    "outchit'": "apprendre", "lyubit'": "aimer", "govorit'": "parler / dire",
    "prosit'": "demander (to request)", "platit'": "payer", "pomnit'": "se souvenir",
    "poloutchit'": "obtenir", "vyerit'": "croire", "prikhodit'": "venir / arriver",
    "sprosit'": "demander (to ask)",
    "byt'": "être", "yest'": "manger", "pit'": "boire", "motch'": "pouvoir",
    "dat'": "donner", "idti": "aller", "khotyet'": "vouloir",
    "brat'": "prendre (un objet)", "klast'": "mettre",
    "stanovit'sya": "devenir", "noujdat'sya": "avoir besoin",
    "soglachat'sya": "être d'accord", "dvigat'sya": "bouger"
};

// ============== VERB LISTS ==============
const verbes1ereConj = [
    "dyelat'", "znat'", "doumat'", "rabotat'", "jdat'", "pisat'", "tchitat'",
    "otvyetchat'", "pokoupat'", "prodavat'", "ponimat'", "pokazyvat'",
    "ostanavlivat'", "zabyvat'", "vybirat'", "myenyat'", "pomogat'", "prinimat'"
];

const verbes2emeConj = [
    "imyet'", "khodit'", "vidyet'", "outchit'", "lyubit'", "govorit'",
    "prosit'", "platit'", "pomnit'", "poloutchit'", "vyerit'", "prikhodit'",
    "sprosit'"
];

const verbesIrreguliers = [
    "byt'", "yest'", "pit'", "motch'", "dat'", "idti", "khotyet'",
    "brat'", "klast'", "stanovit'sya", "noujdat'sya",
    "soglachat'sya", "dvigat'sya"
];

const temps = ["présent", "passé", "gérondif"];
const pronoms = ["ya", "ty", "on/ona", "my", "vy", "oni"];
const genresPasse = ["Masculin (Ya/Ty/On)", "Féminin (Ya/Ty/Ona)", "Neutre (Ono)", "Pluriel (My/Vy/Oni)"];
const genresParticipe = ["Masculin", "Féminin", "Neutre", "Pluriel"];

// ============== REGULAR ENDINGS ==============
const terminaisons = {
    "1ere": {
        "présent": ["yu", "yech'", "yet", "yem", "yetye", "yut"],
        "passé": ["l", "la", "lo", "li"],
        "futur": ["boudou", "boudyech'", "boudyet", "boudyem", "boudyetye", "boudout"],
        "impératif": ["", "î", "", "", "îtye", ""],
        "participe passé": ["nnyî", "nnaya", "nnoye", "nnyye"],
        "gérondif": ["ya", "ya", "ya", "ya", "ya", "ya"]
    },
    "2eme": {
        "présent": ["yu", "ich'", "it", "im", "itye", "yat"],
        "passé": ["l", "la", "lo", "li"],
        "futur": ["boudou", "boudyech'", "boudyet", "boudyem", "boudyetye", "boudout"],
        "impératif": ["", "i", "", "", "itye", ""],
        "participe passé": ["nnyî", "nnaya", "nnoye", "nnyye"],
        "gérondif": ["ya", "ya", "ya", "ya", "ya", "ya"]
    }
};

// ============== IRREGULAR VERB CONJUGATIONS ==============
const irregulierConj = {
    "byt'": {
        "présent": ["-", "-", "-", "-", "-", "-"],
        "passé": ["byl", "byla", "bylo", "byli"],
        "futur": ["boudou", "boudyech'", "boudyet", "boudyem", "boudyetye", "boudout"],
        "impératif": ["", "boud'", "", "", "boud'tye", ""],
        "participe passé": ["byvchiî", "byvchaya", "byvchyeye", "byvchiye"],
        "gérondif": ["boudoutchi", "boudoutchi", "boudoutchi", "boudoutchi", "boudoutchi", "boudoutchi"]
    },
    "yest'": {
        "présent": ["yem", "yech'", "yest", "yedim", "yeditye", "yedyat"],
        "passé": ["yel", "yela", "yelo", "yeli"],
        "futur": ["boudou yest'", "boudyech' yest'", "boudyet yest'", "boudyem yest'", "boudyetye yest'", "boudout yest'"],
        "impératif": ["", "yech'", "", "", "yech'tye", ""],
        "participe passé": ["yevchiî", "yevchaya", "yevchyeye", "yevchiye"],
        "gérondif": ["yedya", "yedya", "yedya", "yedya", "yedya", "yedya"]
    },
    "pit'": {
        "présent": ["p'yu", "p'yoch'", "p'yot", "p'yom", "p'yotye", "p'yut"],
        "passé": ["pil", "pila", "pilo", "pili"],
        "futur": ["boudou pit'", "boudyech' pit'", "boudyet pit'", "boudyem pit'", "boudyetye pit'", "boudout pit'"],
        "impératif": ["", "pyeî", "", "", "pyeîtye", ""],
        "participe passé": ["pivchiî", "pivchaya", "pivchyeye", "pivchiye"],
        "gérondif": ["piya", "piya", "piya", "piya", "piya", "piya"]
    },
    "dat'": {
        "présent": ["dayu", "dayoch'", "dayot", "dadim", "daditye", "dadout"],
        "passé": ["dal", "dala", "dalo", "dali"],
        "futur": ["dam", "dach'", "dast", "dadim", "daditye", "dadout"],
        "impératif": ["", "daî", "", "", "daîtye", ""],
        "participe passé": ["davchiî", "davchaya", "davchyeye", "davchiye"],
        "gérondif": ["dav", "dav", "dav", "dav", "dav", "dav"]
    },
    "idti": {
        "présent": ["idou", "idyoch'", "idyot", "idyom", "idyotye", "idout"],
        "passé": ["chyol", "chla", "chlo", "chli"],
        "futur": ["boudou idti", "boudyech' idti", "boudyet idti", "boudyem idti", "boudyetye idti", "boudout idti"],
        "impératif": ["", "idi", "", "", "iditye", ""],
        "participe passé": ["chyedchiî", "chyedchaya", "chyedchyeye", "chyedchiye"],
        "gérondif": ["idya", "idya", "idya", "idya", "idya", "idya"]
    },
    "motch'": {
        "présent": ["mogou", "mojyech'", "mojyet", "mojyem", "mojyetye", "mogout"],
        "passé": ["mog", "mogla", "moglo", "mogli"],
        "futur": ["smogou", "smojyech'", "smojyet", "smojyem", "smojyetye", "smogout"],
        "impératif": ["", "", "", "", "", ""],
        "participe passé": ["mogchiî", "mogchaya", "mogchyeye", "mogchiye"],
        "gérondif": ["mogya", "mogya", "mogya", "mogya", "mogya", "mogya"]
    },
    "khotyet'": {
        "présent": ["khotchou", "khotchyech'", "khotchyet", "khotim", "khotitye", "khotyat"],
        "passé": ["khotyel", "khotyela", "khotyelo", "khotyeli"],
        "futur": ["boudou khotyet'", "boudyech' khotyet'", "boudyet khotyet'", "boudyem khotyet'", "boudyetye khotyet'", "boudout khotyet'"],
        "impératif": ["", "khoti", "", "", "khotitye", ""],
        "participe passé": ["khotyevchiî", "khotyevchaya", "khotyevchyeye", "khotyevchiye"],
        "gérondif": ["khotya", "khotya", "khotya", "khotya", "khotya", "khotya"]
    },
    "brat'": {
        "présent": ["byerou", "byeryoch'", "byeryot", "byeryom", "byeryotye", "byerout"],
        "passé": ["bral", "brala", "bralo", "brali"],
        "futur": ["boudou brat'", "boudyech' brat'", "boudyet brat'", "boudyem brat'", "boudyetye brat'", "boudout brat'"],
        "impératif": ["", "byeri", "", "", "byeritye", ""],
        "participe passé": ["bravchiî", "bravchaya", "bravchyeye", "bravchiye"],
        "gérondif": ["byerya", "byerya", "byerya", "byerya", "byerya", "byerya"]
    },
    "klast'": {
        "présent": ["kladou", "kladyoch'", "kladyot", "kladyom", "kladyotye", "kladout"],
        "passé": ["klal", "klala", "klalo", "klali"],
        "futur": ["boudou klast'", "boudyech' klast'", "boudyet klast'", "boudyem klast'", "boudyetye klast'", "boudout klast'"],
        "impératif": ["", "kladi", "", "", "kladitye", ""],
        "participe passé": ["kladchiî", "kladchaya", "kladchyeye", "kladchiye"],
        "gérondif": ["kladya", "kladya", "kladya", "kladya", "kladya", "kladya"]
    },
    "stanovit'sya": {
        "présent": ["stanovlyous'", "stanovich'sya", "stanovitsya", "stanovimsya", "stanovites'", "stanovyatsya"],
        "passé": ["stanovilsya", "stanovilas'", "stanovilos'", "stanovilis'"],
        "futur": ["boudou stanovit'sya", "boudyech' stanovit'sya", "boudyet stanovit'sya", "boudyem stanovit'sya", "boudyetye stanovit'sya", "boudout stanovit'sya"],
        "impératif": ["", "stanovis'", "", "", "stanovites'", ""],
        "participe passé": ["stanovivchiîsya", "stanovivchayasya", "stanovivchyeyesya", "stanovivchiyesya"],
        "gérondif": ["stanovyas'", "stanovyas'", "stanovyas'", "stanovyas'", "stanovyas'", "stanovyas'"]
    },
    "noujdat'sya": {
        "présent": ["noujdayous'", "noujdayech'sya", "noujdayetsya", "noujdayemsya", "noujdayetes'", "noujdayutsya"],
        "passé": ["noujdalsya", "noujdalas'", "noujdalos'", "noujdalis'"],
        "futur": ["boudou noujdat'sya", "boudyech' noujdat'sya", "boudyet noujdat'sya", "boudyem noujdat'sya", "boudyetye noujdat'sya", "boudout noujdat'sya"],
        "impératif": ["", "noujdaîsya", "", "", "noujdaîtes'", ""],
        "participe passé": ["noujdavchiîsya", "noujdavchayasya", "noujdavchyeyesya", "noujdavchiyesya"],
        "gérondif": ["noujdayas'", "noujdayas'", "noujdayas'", "noujdayas'", "noujdayas'", "noujdayas'"]
    },
    "soglachat'sya": {
        "présent": ["soglachayous'", "soglachayech'sya", "soglachayetsya", "soglachayemsya", "soglachayetes'", "soglachayutsya"],
        "passé": ["soglachalsya", "soglachalas'", "soglachalos'", "soglachalis'"],
        "futur": ["boudou soglachat'sya", "boudyech' soglachat'sya", "boudyet soglachat'sya", "boudyem soglachat'sya", "boudyetye soglachat'sya", "boudout soglachat'sya"],
        "impératif": ["", "soglacha îsya", "", "", "soglacha îtes'", ""],
        "participe passé": ["soglachavchiîsya", "soglachavchayasya", "soglachavchyeyesya", "soglachavchiyesya"],
        "gérondif": ["soglachayas'", "soglachayas'", "soglachayas'", "soglachayas'", "soglachayas'", "soglachayas'"]
    },
    "dvigat'sya": {
        "présent": ["dvigayous'", "dvigayech'sya", "dvigayetsya", "dvigayemsya", "dvigayetes'", "dvigayutsya"],
        "passé": ["dvigalsya", "dvigalas'", "dvigalos'", "dvigalis'"],
        "futur": ["boudou dvigat'sya", "boudyech' dvigat'sya", "boudyet dvigat'sya", "boudyem dvigat'sya", "boudyetye dvigat'sya", "boudout dvigat'sya"],
        "impératif": ["", "dvigaîsya", "", "", "dvigaîtes'", ""],
        "participe passé": ["dvigavchiîsya", "dvigavchayasya", "dvigavchyeyesya", "dvigavchiyesya"],
        "gérondif": ["dvigayas'", "dvigayas'", "dvigayas'", "dvigayas'", "dvigayas'", "dvigayas'"]
    }
};

// ============== CONJUGATION FUNCTION ==============
function conjuguerVerbe(verbe, pronomIndex, tempsChoisi, genreIndex = null) {
    const idxGenre = (tempsChoisi === "passé" || tempsChoisi === "participe passé") && genreIndex !== null ? genreIndex : pronomIndex;

    // Irregular verb
    if (irregulierConj[verbe]) {
        const conj = irregulierConj[verbe];
        if (tempsChoisi === "participe passé") return conj[tempsChoisi][idxGenre];
        if (tempsChoisi === "gérondif") return conj[tempsChoisi][0];
        if (tempsChoisi === "impératif" && pronomIndex === 0) return "Forme inexistante à l'impératif";
        if (tempsChoisi === "passé") return conj[tempsChoisi][idxGenre];
        return conj[tempsChoisi][pronomIndex];
    }

    // Regular verb
    let typeVerbe;
    if (verbes1ereConj.includes(verbe)) typeVerbe = "1ere";
    else if (verbes2emeConj.includes(verbe)) typeVerbe = "2eme";
    else return verbe;

    let radical;
    if (verbe.endsWith("at'") || verbe.endsWith("it'") || verbe.endsWith("et'")) radical = verbe.slice(0, -3);
    else if (verbe.endsWith("t'")) radical = verbe.slice(0, -2);
    else radical = verbe;

    if (tempsChoisi === "participe passé") return radical + terminaisons[typeVerbe][tempsChoisi][idxGenre];
    if (tempsChoisi === "gérondif") return radical + terminaisons[typeVerbe][tempsChoisi][0];
    if (tempsChoisi === "impératif" && pronomIndex === 0) return "Forme inexistante à l'impératif";
    if (tempsChoisi === "passé") {
        const radPasse = verbe.endsWith("t'") ? verbe.slice(0, -2) : radical;
        return radPasse + terminaisons[typeVerbe][tempsChoisi][idxGenre];
    }
    return radical + terminaisons[typeVerbe][tempsChoisi][pronomIndex];
}

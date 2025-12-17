import random
import tkinter as tk
from tkinter import ttk, messagebox
import os

# Variable pour choisir le dictionnaire
# 1: dictionnaire complet, 2: dictionnaire échantillon
dictionnaire = 1

# Variable pour choisir le type d'entraînement
# 0: conjugaison et traduction, 1: uniquement traduction, 2: uniquement conjugaison
training_type = 0

# Variable pour choisir le type de verbes
# 0: tous les verbes, 1: uniquement verbes irréguliers, 2: uniquement verbes réguliers
verb_mode = 0

# créé une liste qui contient tous les mots en français (avant le "%" dans dictionnaire.txt)
mots_francais = []

# créé une liste qui contient tous les mots en espagnol (après le "%" dans dictionnaire.txt)
mots_espagnols = []

# Chemin de base pour les fichiers (racine du projet)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Choix du fichier dictionnaire en fonction de la variable
if dictionnaire == 1:
    fichier_dictionnaire = './Dictionnaires/dictionnaire_spanish.txt'
elif dictionnaire == 2:
    fichier_dictionnaire = './Dictionnaires/dictionnaire_spanish_sample.txt'
else:
    fichier_dictionnaire = './Dictionnaires/dictionnaire_spanish.txt'

# Lecture du fichier dictionnaire
try:
    with open(fichier_dictionnaire, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if '%' in ligne:
                francais, espagnol = ligne.split(' % ')
                mots_francais.append(francais)
                mots_espagnols.append(espagnol)
except FileNotFoundError:
    messagebox.showerror("Erreur", f"Le fichier dictionnaire est introuvable :\n{fichier_dictionnaire}")

# Vérification que le dictionnaire n'est pas vide
if not mots_francais:
    # Ajout de valeurs par défaut pour éviter le crash si le fichier est vide ou mal lu
    mots_francais = ["Erreur"]
    mots_espagnols = ["Dictionnaire vide ou introuvable"]

# Verbes pour la conjugaison (infinitif en espagnol)
verbes_ar = [
    'amar', 'andar', 'ayudar', 'bailar', 'buscar', 'caminar', 'cantar', 'cenar', 'comprar',
    'conversar', 'cortar', 'dejar', 'desear', 'entrar', 'escuchar', 'esperar', 'estudiar',
    'explicar', 'ganar', 'gastar', 'gustar', 'hablar', 'lavar', 'levantar', 'llamar', 'llegar',
    'llevar', 'mandar', 'mirar', 'nadar', 'necesitar', 'pagar', 'pasar', 'pensar', 'preguntar',
    'preparar', 'quedar', 'regresar', 'terminar', 'tocar', 'tomar', 'trabajar', 'usar', 'viajar', 'visitar'
]

verbes_er = [
    'aprender', 'beber', 'comer', 'comprender', 'correr', 'creer', 'deber', 'leer', 'meter',
    'poseer', 'romper', 'temer', 'vender', 'esconder', 'sorprender', 'responder', 'prometer'
]

verbes_ir = [
    'abrir', 'asistir', 'compartir', 'consistir', 'decidir', 'describir', 'discutir', 'escribir',
    'existir', 'insistir', 'partir', 'permitir', 'recibir', 'subir', 'sufrir', 'unir', 'vivir',
    'admitir', 'añadir', 'cubrir', 'descubrir', 'imprimir', 'ocurrir'
]

# Verbes irréguliers
verbes_irreguliers = ['ser', 'estar', 'tener', 'hacer', 'venir', 'ir', 'poder', 'decir', 'saber', 'ver', 'dar', 'traer', 'querer']
verbes_irreguliers_connus = []
verbes_irreguliers_pas_connus = []

# Temps
temps = ['imparfait']
temps_connus = ['impératif', 'conditionnel présent', 'passé', 'présent', 'futur', 'gérondif', 'participe passé']
temps_pas_connus = ['présent du subjonctif', 'imparfait du subjonctif', 'futur du subjonctif']

# Pronoms
pronoms = ['yo', 'tú', 'él/ella/usted', 'nosotros', 'vosotros', 'ellos/ellas/ustedes']

# Terminaisons par temps et pronom
terminaisons = {
    'ar': {
        'présent': ['o', 'as', 'a', 'amos', 'áis', 'an'],
        'passé': ['é', 'aste', 'ó', 'amos', 'asteis', 'aron'],
        'futur': ['aré', 'arás', 'ará', 'aremos', 'aréis', 'arán'],
        'imparfait': ['aba', 'abas', 'aba', 'ábamos', 'abais', 'aban'],
        'présent du subjonctif': ['e', 'es', 'e', 'emos', 'éis', 'en'],
        'imparfait du subjonctif': ['ara', 'aras', 'ara', 'áramos', 'arais', 'aran'],
        'futur du subjonctif': ['are', 'ares', 'are', 'áremos', 'areis', 'aren'],
        'participe passé': ['ado', 'ado', 'ado', 'ado', 'ado', 'ado'],
        'gérondif': ['ando', 'ando', 'ando', 'ando', 'ando', 'ando'],
        'impératif': ['', 'a', 'e', 'emos', 'ad', 'en'],
        'conditionnel présent': ['aría', 'arías', 'aría', 'aríamos', 'aríais', 'arían']
    },
    'er': {
        'présent': ['o', 'es', 'e', 'emos', 'éis', 'en'],
        'passé': ['í', 'iste', 'ió', 'imos', 'isteis', 'ieron'],
        'futur': ['eré', 'erás', 'erá', 'eremos', 'eréis', 'erán'],
        'imparfait': ['ía', 'ías', 'ía', 'íamos', 'íais', 'ían'],
        'présent du subjonctif': ['a', 'as', 'a', 'amos', 'áis', 'an'],
        'imparfait du subjonctif': ['iera', 'ieras', 'iera', 'iéramos', 'ierais', 'ieran'],
        'futur du subjonctif': ['iere', 'ieres', 'iere', 'iéremos', 'iereis', 'ieren'],
        'participe passé': ['ido', 'ido', 'ido', 'ido', 'ido', 'ido'],
        'gérondif': ['iendo', 'iendo', 'iendo', 'iendo', 'iendo', 'iendo'],
        'impératif': ['', 'e', 'a', 'amos', 'ed', 'an'],
        'conditionnel présent': ['ería', 'erías', 'ería', 'eríamos', 'eríais', 'erían']
    },
    'ir': {
        'présent': ['o', 'es', 'e', 'imos', 'ís', 'en'],
        'passé': ['í', 'iste', 'ió', 'imos', 'isteis', 'ieron'],
        'futur': ['iré', 'irás', 'irá', 'iremos', 'iréis', 'irán'],
        'imparfait': ['ía', 'ías', 'ía', 'íamos', 'íais', 'ían'],
        'présent du subjonctif': ['a', 'as', 'a', 'amos', 'áis', 'an'],
        'imparfait du subjonctif': ['iera', 'ieras', 'iera', 'iéramos', 'ierais', 'ieran'],
        'futur du subjonctif': ['iere', 'ieres', 'iere', 'iéremos', 'iereis', 'iren'],
        'participe passé': ['ido', 'ido', 'ido', 'ido', 'ido', 'ido'],
        'gérondif': ['iendo', 'iendo', 'iendo', 'iendo', 'iendo', 'iendo'],
        'impératif': ['', 'e', 'a', 'amos', 'id', 'an'],
        'conditionnel présent': ['iría', 'irías', 'iría', 'iríamos', 'iríais', 'irían']
    }
}

# Terminaisons spéciales pour les verbes irréguliers
terminaisons_tener = {
    'présent': ['tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen'],
    'passé': ['tuve', 'tuviste', 'tuvo', 'tuvimos', 'tuvisteis', 'tuvieron'],
    'futur': ['tendré', 'tendrás', 'tendrá', 'tendremos', 'tendréis', 'tendrán'],
    'imparfait': ['tenía', 'tenías', 'tenía', 'teníamos', 'teníais', 'tenían'],
    'présent du subjonctif': ['tenga', 'tengas', 'tenga', 'tengamos', 'tengáis', 'tengan'],
    'imparfait du subjonctif': ['tuviera', 'tuvieras', 'tuviera', 'tuviéramos', 'tuvierais', 'tuvieran'],
    'futur du subjonctif': ['tuviere', 'tuvieres', 'tuviere', 'tuviéremos', 'tuviereis', 'tuvieren'],
    'participe passé': ['tenido', 'tenido', 'tenido', 'tenido', 'tenido', 'tenido'],
    'gérondif': ['teniendo', 'teniendo', 'teniendo', 'teniendo', 'teniendo', 'teniendo'],
    'impératif': ['', 'ten', 'tenga', 'tengamos', 'tened', 'tengan'],
    'conditionnel présent': ['tendría', 'tendrías', 'tendría', 'tendríamos', 'tendríais', 'tendrían']
}

terminaisons_hacer = {
    'présent': ['hago', 'haces', 'hace', 'hacemos', 'hacéis', 'hacen'],
    'passé': ['hice', 'hiciste', 'hizo', 'hicimos', 'hicisteis', 'hicieron'],
    'futur': ['haré', 'harás', 'hará', 'haremos', 'haréis', 'harán'],
    'imparfait': ['hacía', 'hacías', 'hacía', 'hacíamos', 'hacíais', 'hacían'],
    'présent du subjonctif': ['haga', 'hagas', 'haga', 'hagamos', 'hagáis', 'hagan'],
    'imparfait du subjonctif': ['hiciera', 'hicieras', 'hiciera', 'hiciéramos', 'hicierais', 'hicieran'],
    'futur du subjonctif': ['hiciere', 'hicieres', 'hiciere', 'hiciéremos', 'hiciereis', 'hicieren'],
    'participe passé': ['hecho', 'hecho', 'hecho', 'hecho', 'hecho', 'hecho'],
    'gérondif': ['haciendo', 'haciendo', 'haciendo', 'haciendo', 'haciendo', 'haciendo'],
    'impératif': ['', 'haz', 'haga', 'hagamos', 'haced', 'hagan'],
    'conditionnel présent': ['haría', 'harías', 'haría', 'haríamos', 'haríais', 'harían']
}

terminaisons_ser = {
    'présent': ['soy', 'eres', 'es', 'somos', 'sois', 'son'],
    'passé': ['fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron'],
    'futur': ['seré', 'serás', 'será', 'seremos', 'seréis', 'serán'],
    'imparfait': ['era', 'eras', 'era', 'éramos', 'erais', 'eran'],
    'présent du subjonctif': ['sea', 'seas', 'sea', 'seamos', 'seáis', 'sean'],
    'imparfait du subjonctif': ['fuera', 'fueras', 'fuera', 'fuéramos', 'fuerais', 'fueran'],
    'futur du subjonctif': ['fuere', 'fueres', 'fuere', 'fuéremos', 'fuereis', 'fueren'],
    'participe passé': ['sido', 'sido', 'sido', 'sido', 'sido', 'sido'],
    'gérondif': ['siendo', 'siendo', 'siendo', 'siendo', 'siendo', 'siendo'],
    'impératif': ['', 'sé', 'sea', 'seamos', 'sed', 'sean'],
    'conditionnel présent': ['sería', 'serías', 'sería', 'seríamos', 'seríais', 'serían']
}

terminaisons_estar = {
    'présent': ['estoy', 'estás', 'está', 'estamos', 'estáis', 'están'],
    'passé': ['estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron'],
    'futur': ['estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán'],
    'imparfait': ['estaba', 'estabas', 'estaba', 'estábamos', 'estabais', 'estaban'],
    'présent du subjonctif': ['esté', 'estés', 'esté', 'estemos', 'estéis', 'estén'],
    'imparfait du subjonctif': ['estuviera', 'estuvieras', 'estuviera', 'estuviéramos', 'estuvierais', 'estuvieran'],
    'futur du subjonctif': ['estuviere', 'estuvieres', 'estuviere', 'estuviéremos', 'estuviereis', 'estuvieren'],
    'participe passé': ['estado', 'estado', 'estado', 'estado', 'estado', 'estado'],
    'gérondif': ['estando', 'estando', 'estando', 'estando', 'estando', 'estando'],
    'impératif': ['', 'está', 'esté', 'estemos', 'estad', 'estén'],
    'conditionnel présent': ['estaría', 'estarías', 'estaría', 'estaríamos', 'estaríais', 'estarían']
}

terminaisons_venir = {
    'présent': ['vengo', 'vienes', 'viene', 'venimos', 'venís', 'vienen'],
    'passé': ['vine', 'viniste', 'vino', 'vinimos', 'vinisteis', 'vinieron'],
    'futur': ['vendré', 'vendrás', 'vendrá', 'vendremos', 'vendréis', 'vendrán'],
    'imparfait': ['venía', 'venías', 'venía', 'veníamos', 'veníais', 'venían'],
    'présent du subjonctif': ['venga', 'vengas', 'venga', 'vengamos', 'vengáis', 'vengan'],
    'imparfait du subjonctif': ['viniera', 'vinieras', 'viniera', 'viniéramos', 'vinierais', 'vinieran'],
    'futur du subjonctif': ['viniere', 'vinieres', 'viniere', 'viniéremos', 'viniereis', 'vinieren'],
    'participe passé': ['venido', 'venido', 'venido', 'venido', 'venido', 'venido'],
    'gérondif': ['viniendo', 'viniendo', 'viniendo', 'viniendo', 'viniendo', 'viniendo'],
    'impératif': ['', 'ven', 'venga', 'vengamos', 'venid', 'vengan'],
    'conditionnel présent': ['vendría', 'vendrías', 'vendría', 'vendríamos', 'vendríais', 'vendrían']
}

terminaisons_ir = {
    'présent': ['voy', 'vas', 'va', 'vamos', 'vais', 'van'],
    'passé': ['fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron'],
    'futur': ['iré', 'irás', 'irá', 'iremos', 'iréis', 'irán'],
    'imparfait': ['iba', 'ibas', 'iba', 'íbamos', 'ibais', 'iban'],
    'présent du subjonctif': ['vaya', 'vayas', 'vaya', 'vayamos', 'vayáis', 'vayan'],
    'imparfait du subjonctif': ['fuera', 'fueras', 'fuera', 'fuéramos', 'fuerais', 'fueran'],
    'futur du subjonctif': ['fuere', 'fueres', 'fuere', 'fuéremos', 'fuereis', 'fueren'],
    'participe passé': ['ido', 'ido', 'ido', 'ido', 'ido', 'ido'],
    'gérondif': ['yendo', 'yendo', 'yendo', 'yendo', 'yendo', 'yendo'],
    'impératif': ['', 've', 'vaya', 'vayamos', 'id', 'vayan'],
    'conditionnel présent': ['iría', 'irías', 'iría', 'iríamos', 'iríais', 'irían']
}

terminaisons_poder = {
    'présent': ['puedo', 'puedes', 'puede', 'podemos', 'podéis', 'pueden'],
    'passé': ['pude', 'pudiste', 'pudo', 'pudimos', 'pudisteis', 'pudieron'],
    'futur': ['podré', 'podrás', 'podrá', 'podremos', 'podréis', 'podrán'],
    'imparfait': ['podía', 'podías', 'podía', 'podíamos', 'podíais', 'podían'],
    'présent du subjonctif': ['pueda', 'puedas', 'pueda', 'podamos', 'podáis', 'puedan'],
    'imparfait du subjonctif': ['pudiera', 'pudieras', 'pudiera', 'pudiéramos', 'pudierais', 'pudieran'],
    'futur du subjonctif': ['pudiere', 'pudieres', 'pudiere', 'pudiéremos', 'pudiereis', 'pudieren'],
    'participe passé': ['podido', 'podido', 'podido', 'podido', 'podido', 'podido'],
    'gérondif': ['pudiendo', 'pudiendo', 'pudiendo', 'pudiendo', 'pudiendo', 'pudiendo'],
    'impératif': ['', 'puede', 'pueda', 'podamos', 'poded', 'puedan'],
    'conditionnel présent': ['podría', 'podrías', 'podría', 'podríamos', 'podríais', 'podrían']
}

# Nouvelles terminaisons irrégulières
terminaisons_decir = {
    'présent': ['digo', 'dices', 'dice', 'decimos', 'decís', 'dicen'],
    'passé': ['dije', 'dijiste', 'dijo', 'dijimos', 'dijisteis', 'dijeron'],
    'futur': ['diré', 'dirás', 'dirá', 'diremos', 'diréis', 'dirán'],
    'imparfait': ['decía', 'decías', 'decía', 'decíamos', 'decíais', 'decían'],
    'présent du subjonctif': ['diga', 'digas', 'diga', 'digamos', 'digáis', 'digan'],
    'imparfait du subjonctif': ['dijera', 'dijeras', 'dijera', 'dijéramos', 'dijerais', 'dijeran'],
    'futur du subjonctif': ['dijere', 'dijeres', 'dijere', 'dijéremos', 'dijereis', 'dijeren'],
    'participe passé': ['dicho', 'dicho', 'dicho', 'dicho', 'dicho', 'dicho'],
    'gérondif': ['diciendo', 'diciendo', 'diciendo', 'diciendo', 'diciendo', 'diciendo'],
    'impératif': ['', 'di', 'diga', 'digamos', 'decid', 'digan'],
    'conditionnel présent': ['diría', 'dirías', 'diría', 'diríamos', 'diríais', 'dirían']
}

terminaisons_saber = {
    'présent': ['sé', 'sabes', 'sabe', 'sabemos', 'sabéis', 'saben'],
    'passé': ['supe', 'supiste', 'supo', 'supimos', 'supisteis', 'supieron'],
    'futur': ['sabré', 'sabrás', 'sabrá', 'sabremos', 'sabréis', 'sabrán'],
    'imparfait': ['sabía', 'sabías', 'sabía', 'sabíamos', 'sabíais', 'sabían'],
    'présent du subjonctif': ['sepa', 'sepas', 'sepa', 'sepamos', 'sepáis', 'sepan'],
    'imparfait du subjonctif': ['supiera', 'supieras', 'supiera', 'supiéramos', 'supierais', 'supieran'],
    'futur du subjonctif': ['supiere', 'supieres', 'supiere', 'supiéremos', 'supiereis', 'supieren'],
    'participe passé': ['sabido', 'sabido', 'sabido', 'sabido', 'sabido', 'sabido'],
    'gérondif': ['sabiendo', 'sabiendo', 'sabiendo', 'sabiendo', 'sabiendo', 'sabiendo'],
    'impératif': ['', 'sabe', 'sepa', 'sepamos', 'sabed', 'sepan'],
    'conditionnel présent': ['sabría', 'sabrías', 'sabría', 'sabríamos', 'sabríais', 'sabrían']
}

terminaisons_ver = {
    'présent': ['veo', 'ves', 've', 'vemos', 'veis', 'ven'],
    'passé': ['vi', 'viste', 'vio', 'vimos', 'visteis', 'vieron'],
    'futur': ['veré', 'verás', 'verá', 'veremos', 'veréis', 'verán'],
    'imparfait': ['veía', 'veías', 'veía', 'veíamos', 'veíais', 'veían'],
    'présent du subjonctif': ['vea', 'veas', 'vea', 'veamos', 'veáis', 'vean'],
    'imparfait du subjonctif': ['viera', 'vieras', 'viera', 'viéramos', 'vierais', 'vieran'],
    'futur du subjonctif': ['viere', 'vieres', 'viere', 'viéremos', 'viereis', 'vieren'],
    'participe passé': ['visto', 'visto', 'visto', 'visto', 'visto', 'visto'],
    'gérondif': ['viendo', 'viendo', 'viendo', 'viendo', 'viendo', 'viendo'],
    'impératif': ['', 've', 'vea', 'veamos', 'ved', 'vean'],
    'conditionnel présent': ['vería', 'verías', 'vería', 'veríamos', 'veríais', 'verían']
}

terminaisons_dar = {
    'présent': ['doy', 'das', 'da', 'damos', 'dais', 'dan'],
    'passé': ['di', 'diste', 'dio', 'dimos', 'disteis', 'dieron'],
    'futur': ['daré', 'darás', 'dará', 'daremos', 'daréis', 'darán'],
    'imparfait': ['daba', 'dabas', 'daba', 'dábamos', 'dabais', 'daban'],
    'présent du subjonctif': ['dé', 'des', 'dé', 'demos', 'deis', 'den'],
    'imparfait du subjonctif': ['diera', 'dieras', 'diera', 'diéramos', 'dierais', 'dieran'],
    'futur du subjonctif': ['diere', 'dieres', 'diere', 'diéremos', 'diereis', 'dieren'],
    'participe passé': ['dado', 'dado', 'dado', 'dado', 'dado', 'dado'],
    'gérondif': ['dando', 'dando', 'dando', 'dando', 'dando', 'dando'],
    'impératif': ['', 'da', 'dé', 'demos', 'dad', 'den'],
    'conditionnel présent': ['daría', 'darías', 'daría', 'daríamos', 'daríais', 'darían']
}

terminaisons_traer = {
    'présent': ['traigo', 'traes', 'trae', 'traemos', 'traéis', 'traen'],
    'passé': ['traje', 'trajiste', 'trajo', 'trajimos', 'trajisteis', 'trajeron'],
    'futur': ['traeré', 'traerás', 'traerá', 'traeremos', 'traeréis', 'traerán'],
    'imparfait': ['traía', 'traías', 'traía', 'traíamos', 'traíais', 'traían'],
    'présent du subjonctif': ['traiga', 'traigas', 'traiga', 'traigamos', 'traigáis', 'traigan'],
    'imparfait du subjonctif': ['trajera', 'trajeras', 'trajera', 'trajéramos', 'trajerais', 'trajeran'],
    'futur du subjonctif': ['trajere', 'trajeres', 'trajere', 'trajéremos', 'trajereis', 'trajeren'],
    'participe passé': ['traído', 'traído', 'traído', 'traído', 'traído', 'traído'],
    'gérondif': ['trayendo', 'trayendo', 'trayendo', 'trayendo', 'trayendo', 'trayendo'],
    'impératif': ['', 'trae', 'traiga', 'traigamos', 'traed', 'traigan'],
    'conditionnel présent': ['traería', 'traerías', 'traería', 'traeríamos', 'traeríais', 'traerían']
}

terminaisons_querer = {
    'présent': ['quiero', 'quieres', 'quiere', 'queremos', 'queréis', 'quieren'],
    'passé': ['quise', 'quisiste', 'quiso', 'quisimos', 'quisisteis', 'quisieron'],
    'futur': ['querré', 'querrás', 'querrá', 'querremos', 'querréis', 'querrán'],
    'imparfait': ['quería', 'querías', 'quería', 'queríamos', 'queríais', 'querían'],
    'présent du subjonctif': ['quiera', 'quieras', 'quiera', 'queramos', 'queráis', 'quieran'],
    'imparfait du subjonctif': ['quisiera', 'quisieras', 'quisiera', 'quisiéramos', 'quisierais', 'quisieran'],
    'futur du subjonctif': ['quisiere', 'quisieres', 'quisiere', 'quisiéremos', 'quisiereis', 'quisieren'],
    'participe passé': ['querido', 'querido', 'querido', 'querido', 'querido', 'querido'],
    'gérondif': ['queriendo', 'queriendo', 'queriendo', 'queriendo', 'queriendo', 'queriendo'],
    'impératif': ['', 'quiere', 'quiera', 'queramos', 'quered', 'quieran'],
    'conditionnel présent': ['querría', 'querrías', 'querría', 'querríamos', 'querríais', 'querrían']
}


def conjuguer_verbe(verbe, pronom_index, temps_choisi):
    """Conjugue un verbe selon le pronom et le temps donnés"""
    # Vérifier si c'est un verbe irrégulier
    if verbe == 'tener':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_tener[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_tener[temps_choisi][pronom_index]
    elif verbe == 'hacer':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_hacer[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_hacer[temps_choisi][pronom_index]
    elif verbe == 'ser':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_ser[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_ser[temps_choisi][pronom_index]
    elif verbe == 'estar':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_estar[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_estar[temps_choisi][pronom_index]
    elif verbe == 'venir':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_venir[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_venir[temps_choisi][pronom_index]
    elif verbe == 'ir':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_ir[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_ir[temps_choisi][pronom_index]
    elif verbe == 'poder':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_poder[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_poder[temps_choisi][pronom_index]
    elif verbe == 'decir':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_decir[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_decir[temps_choisi][pronom_index]
    elif verbe == 'saber':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_saber[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_saber[temps_choisi][pronom_index]
    elif verbe == 'ver':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_ver[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_ver[temps_choisi][pronom_index]
    elif verbe == 'dar':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_dar[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_dar[temps_choisi][pronom_index]
    elif verbe == 'traer':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_traer[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_traer[temps_choisi][pronom_index]
    elif verbe == 'querer':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_querer[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_querer[temps_choisi][pronom_index]

    # Conjugaison régulière pour les autres verbes
    if verbe.endswith('ar'):
        radical = verbe[:-2]
        type_verbe = 'ar'
    elif verbe.endswith('er'):
        radical = verbe[:-2]
        type_verbe = 'er'
    elif verbe.endswith('ir'):
        radical = verbe[:-2]
        type_verbe = 'ir'
    else:
        return verbe  # Cas d'erreur

    # Cas spéciaux pour certains temps
    if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
        # Ces temps ne varient pas selon le pronom
        terminaison = terminaisons[type_verbe][temps_choisi][0]
        return radical + terminaison
    elif temps_choisi == 'impératif' and pronom_index == 0:
        # L'impératif n'a pas de forme pour "yo"
        return "Forme inexistante à l'impératif"
    else:
        terminaison = terminaisons[type_verbe][temps_choisi][pronom_index]
        return radical + terminaison


class QuizApp:
    def __init__(self, root):
        self.root = root

        # Configuration du style pour changer la couleur de fond
        style = ttk.Style()
        style.theme_use('clam')  # Utilise un thème qui permet la personnalisation
        style.configure('TFrame', background='#454545')  # Couleur de fond des frames
        style.configure('TLabel', background='#454545')  # Couleur de fond des labels

        # Couleur de fond de la fenêtre principale
        self.root.configure(bg='#454545')

        self.root.title("Espagnol")

        # Mettre la fenêtre en vrai plein écran
        self.root.attributes('-fullscreen', True)

        # Variables pour stocker la question actuelle
        self.mode_actuel = None
        self.bonne_reponse = None
        self.verbe_choisi = None
        self.pronom_index = None
        self.temps_choisi = None
        self.index_aleatoire = None

        # Variables pour le compteur de pourcentage
        self.total_questions = 0
        self.correct_answers = 0

        self.setup_ui()
        self.nouvelle_question()

    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        # Obtenir les dimensions de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Dimensions de la fenêtre
        window_width = 800
        window_height = 600

        # Calculer la position pour centrer
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Appliquer la position
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def setup_ui(self):
        # Configuration de la grille principale
        self.root.columnconfigure(0, weight=1)  # Une seule colonne maintenant
        self.root.rowconfigure(0, weight=1)

        # Frame principal (centré)
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configuration de la grille pour le frame principal
        main_frame.columnconfigure(0, weight=1)

        # Label pour afficher la bonne réponse en cas d'erreur (en haut)
        self.bonne_reponse_label = ttk.Label(main_frame, text="",
                                             font=("Arial", 30, "bold"),
                                             foreground="#000000",
                                             justify="center")
        self.bonne_reponse_label.grid(row=0, column=0, pady=(10, 10))

        # Frame pour la question avec plusieurs labels pour les couleurs
        self.question_frame = ttk.Frame(main_frame)
        self.question_frame.grid(row=1, column=0, pady=(20, 10))

        # Label principal pour les questions de traduction (beaucoup plus grand)
        self.question_label = ttk.Label(self.question_frame, text="",
                                        font=("Arial", 50, "bold"),  # 24 * 2.5 = 60
                                        wraplength=900,
                                        justify="center")

        # Labels spéciaux pour les questions de conjugaison avec couleurs (beaucoup plus grands)
        self.conjugaison_frame = ttk.Frame(self.question_frame)

        # Nouveau frame pour regrouper intro + irrégulier sur une seule ligne
        self.titre_frame = ttk.Frame(self.conjugaison_frame)

        self.intro_label = ttk.Label(self.titre_frame, text="",
                                     font=("Arial", 55, "bold"),  # 22 * 2.5 = 55
                                     justify="center")

        self.irregulier_label = ttk.Label(self.titre_frame, text="",
                                          font=("Arial", 60, "bold"),
                                          foreground="#9500ff",  # Violet pour "irrégulier"
                                          justify="center")

        self.verbe_label = ttk.Label(self.conjugaison_frame, text="",
                                     font=("Arial", 65, "bold"),  # 26 * 2.5 = 65 (verbe plus visible)
                                     foreground="#e74c3c",  # Rouge pour le verbe
                                     justify="center")

        self.temps_label = ttk.Label(self.conjugaison_frame, text="",
                                     font=("Arial", 65, "bold"),  # 24 * 2.5 = 60
                                     foreground="#3498db",  # Bleu pour le temps
                                     justify="center")

        self.pronom_label = ttk.Label(self.conjugaison_frame, text="",
                                      font=("Arial", 65, "bold"),  # 24 * 2.5 = 60
                                      foreground="#2bc46c",  # Vert pour le pronom
                                      justify="center")

        # Frame pour la saisie
        saisie_frame = ttk.Frame(main_frame)
        saisie_frame.grid(row=2, column=0, pady=(0, 15))
        saisie_frame.columnconfigure(0, weight=1)

        # Champ de saisie uniquement (sans label "Votre réponse :")
        self.reponse_entry = ttk.Entry(saisie_frame, font=("Arial", 45), width=20)
        self.reponse_entry.grid(row=0, column=0, sticky="ew")
        self.reponse_entry.bind('<Return>', lambda e: self.verifier_reponse())

        # Bouton valider (centré et beaucoup plus grand)
        self.valider_btn = ttk.Button(main_frame, text="Valider",
                                      command=self.verifier_reponse)
        self.valider_btn.config(width=10)
        # Configuration du style du bouton pour augmenter la taille du texte
        style = ttk.Style()
        style.configure("Large.TButton", font=("Arial", 40, "bold"))  # 16 * 2.5 = 40
        self.valider_btn.config(style="Large.TButton")
        self.valider_btn.grid(row=3, column=0, pady=(0, 10))

        # Supprimer le resultat_label car on utilise maintenant les couleurs de fond

        # Frame pour les boutons de contrôle
        controles_frame = ttk.Frame(main_frame)
        controles_frame.grid(row=4, column=0, pady=(0, 0))

        # Configuration des colonnes pour centrer les boutons
        controles_frame.columnconfigure(0, weight=1)
        controles_frame.columnconfigure(1, weight=1)
        controles_frame.columnconfigure(2, weight=1)

        # Style pour les boutons de contrôle
        style.configure("Control.TButton", font=("Arial", 20, "bold"))

        # Bouton Dictionnaire
        self.dict_btn = ttk.Button(controles_frame, text="Dictionnaire",
                                   command=self.changer_dictionnaire,
                                   style="Control.TButton")
        self.dict_btn.grid(row=0, column=0, padx=20, pady=10)

        self.dict_status = ttk.Label(controles_frame, text="",
                                     font=("Arial", 16),
                                     justify="center")
        self.dict_status.grid(row=1, column=0, padx=20)

        # Bouton Type d'entraînement
        self.training_btn = ttk.Button(controles_frame, text="Type d'entraînement",
                                       command=self.changer_training_type,
                                       style="Control.TButton")
        self.training_btn.grid(row=0, column=1, padx=20, pady=10)

        self.training_status = ttk.Label(controles_frame, text="",
                                         font=("Arial", 16),
                                         justify="center")
        self.training_status.grid(row=1, column=1, padx=20)

        # Bouton Verbes irréguliers
        self.irregular_btn = ttk.Button(controles_frame, text="Verbes irréguliers",
                                        command=self.changer_irregular_mode,
                                        style="Control.TButton")
        self.irregular_btn.grid(row=0, column=2, padx=20, pady=10)

        self.irregular_status = ttk.Label(controles_frame, text="",
                                          font=("Arial", 16),
                                          justify="center")
        self.irregular_status.grid(row=1, column=2, padx=20)

        # Bouton Quitter
        self.quit_btn = ttk.Button(main_frame, text="Quitter",
                                   command=self.quitter_application,
                                   style="Control.TButton")
        self.quit_btn.grid(row=5, column=0, pady=(20, 10))

        # Label pour afficher le pourcentage de bonnes réponses (en bas)
        self.percentage_label = ttk.Label(main_frame, text="0% (0/0)",
                                          font=("Arial", 24, "bold"),
                                          foreground="#00bcd4",
                                          justify="center")
        self.percentage_label.grid(row=6, column=0, pady=(10, 20))

        # Mettre à jour l'affichage des statuts
        self.mettre_a_jour_statuts()

        # Focus sur le champ de saisie
        self.reponse_entry.focus()

    def nouvelle_question(self):
        # Réinitialiser l'interface et le fond
        self.reponse_entry.delete(0, tk.END)
        self.bonne_reponse_label.config(text="")
        self.valider_btn.config(state="normal")
        self.reponse_entry.config(state="normal")

        # Remettre le fond neutre
        self.root.configure(bg='#454545')

        # Choix du type de question selon training_type
        if training_type == 0:
            # Utiliser la proportion du curseur pour choisir entre conjugaison et traduction
            if random.random() * 100 < 25:
                self.mode_actuel = 'conjugaison'
            else:
                self.mode_actuel = 'traduction'
        elif training_type == 1:
            # Uniquement traduction
            self.mode_actuel = 'traduction'
        elif training_type == 2:
            # Uniquement conjugaison
            self.mode_actuel = 'conjugaison'

        if self.mode_actuel == 'traduction':
            self.generer_question_traduction()
        else:
            self.generer_question_conjugaison()

        self.reponse_entry.focus()

    def generer_question_traduction(self):
        self.index_aleatoire = random.randint(0, len(mots_francais) - 1)

        # Toujours français vers espagnol
        mot_affiche = mots_francais[self.index_aleatoire]
        self.bonne_reponse = mots_espagnols[self.index_aleatoire]

        # Masquer le frame de conjugaison et afficher le label simple
        self.conjugaison_frame.pack_forget()
        self.question_label.pack(pady=20)
        self.question_label.config(text=f"\n\n{mot_affiche}", foreground="#d6c124")  # Rouge par exemple

    def generer_question_conjugaison(self):
        # Choisir les verbes selon la variable conjugaison_irreguliers_seulement
        if verb_mode == 1:
            # Uniquement les verbes irréguliers
            tous_verbes = verbes_irreguliers
        elif verb_mode == 2:
            # Uniquement les verbes réguliers
            tous_verbes = verbes_ar + verbes_er + verbes_ir
        else:
            # Tous les verbes (réguliers + irréguliers)
            tous_verbes = verbes_ar + verbes_er + verbes_ir + verbes_irreguliers

        self.verbe_choisi = random.choice(tous_verbes)
        pronom_choisi = random.choice(pronoms)
        self.pronom_index = pronoms.index(pronom_choisi)
        self.temps_choisi = random.choice(temps)

        # self.temps_choisi = "futur simple"

        self.bonne_reponse = conjuguer_verbe(self.verbe_choisi, self.pronom_index, self.temps_choisi)

        # Masquer le label simple et afficher le frame de conjugaison coloré
        self.question_label.pack_forget()
        self.conjugaison_frame.pack(pady=20)

        # Configurer les textes avec couleurs (mots-clés seulement)
        # self.intro_label.config(text="Conjuguez le verbe")
        if self.verbe_choisi in verbes_irreguliers:
            self.irregulier_label.config(text="irrégulier")
        else:
            self.irregulier_label.config(text="")  # Vider le label si verbe régulier

        self.verbe_label.config(text=f"{self.verbe_choisi}")  # Juste le verbe
        self.temps_label.config(text=f"{self.temps_choisi}")  # Juste le temps
        self.pronom_label.config(text=f"{pronom_choisi}")  # Juste le pronom

        # Réorganisation : nettoyer puis empaqueter
        for widget in (self.titre_frame, self.intro_label, self.irregulier_label,
                       self.verbe_label, self.temps_label, self.pronom_label):
            widget.pack_forget()

        # Ligne titre (intro + irrégulier sur la même ligne)
        self.titre_frame.pack()
        self.intro_label.pack(side="left")
        if self.verbe_choisi in verbes_irreguliers:
            self.irregulier_label.pack(side="left", padx=(10, 0))

        # Saut de ligne après le titre avec verbe_label
        self.verbe_label.pack(pady=(15, 0))
        self.temps_label.pack()
        self.pronom_label.pack()

    def normaliser_texte(self, texte):
        """Supprime les accents d'un texte pour la comparaison"""
        import unicodedata
        # Normalise le texte en décomposant les caractères accentués
        texte_normalise = unicodedata.normalize('NFD', texte)
        # Supprime les marques diacritiques (accents)
        texte_sans_accents = ''.join(c for c in texte_normalise if unicodedata.category(c) != 'Mn')
        return texte_sans_accents.lower()

    def verifier_reponse(self):
        reponse_utilisateur = self.reponse_entry.get().strip()

        if not reponse_utilisateur:
            messagebox.showwarning("Attention", "Veuillez entrer une réponse!")
            return

        if self.mode_actuel == 'traduction':
            # Vérification pour la traduction (toujours français vers espagnol)
            try:
                index_reponse = mots_espagnols.index(reponse_utilisateur)
                if index_reponse == self.index_aleatoire:
                    self.afficher_resultat("succes")
                else:
                    # Vérifier si c'est juste une erreur d'accent
                    reponse_sans_accents = self.normaliser_texte(reponse_utilisateur)
                    bonne_reponse_sans_accents = self.normaliser_texte(self.bonne_reponse)

                    if reponse_sans_accents == bonne_reponse_sans_accents:
                        self.afficher_resultat("presque")
                    else:
                        self.afficher_resultat("echec")
            except ValueError:
                # Vérifier si c'est juste une erreur d'accent
                reponse_sans_accents = self.normaliser_texte(reponse_utilisateur)
                bonne_reponse_sans_accents = self.normaliser_texte(self.bonne_reponse)

                if reponse_sans_accents == bonne_reponse_sans_accents:
                    self.afficher_resultat("presque")
                else:
                    self.afficher_resultat("echec")
        else:
            # Vérification pour la conjugaison
            if reponse_utilisateur.lower() == self.bonne_reponse.lower():
                self.afficher_resultat("succes")
            else:
                # Vérifier si c'est juste une erreur d'accent
                reponse_sans_accents = self.normaliser_texte(reponse_utilisateur)
                bonne_reponse_sans_accents = self.normaliser_texte(self.bonne_reponse)

                if reponse_sans_accents == bonne_reponse_sans_accents:
                    self.afficher_resultat("presque")
                else:
                    self.afficher_resultat("echec")

        # Vider immédiatement le champ de saisie
        self.reponse_entry.delete(0, tk.END)

        # Désactiver temporairement le bouton valider et le champ de saisie
        self.valider_btn.config(state="disabled", text="Valider")
        self.reponse_entry.config(state="disabled")

        # Passer automatiquement à la question suivante après 750ms
        self.root.after(750, self.nouvelle_question)

    def afficher_resultat(self, resultat):
        """Affiche le résultat en changeant la couleur de fond de toute la fenêtre"""
        # Mettre à jour le compteur
        self.total_questions += 1
        if resultat == "succes" or resultat == "presque":
            self.correct_answers += 1
        
        # Mettre à jour l'affichage du pourcentage
        self.update_percentage_display()

        couleur_fond = '#454545'  # Valeur par défaut

        if resultat == "succes":
            # Fond vert pour succès - changer toute la fenêtre
            couleur_fond = '#15853f'
            # Ne pas afficher la bonne réponse pour un succès
            self.bonne_reponse_label.config(text="", foreground="#000000")
        elif resultat == "presque":
            # Fond orange pour presque (erreur d'accent)
            couleur_fond = '#d98b09'
            # Afficher la bonne réponse en noir
            self.bonne_reponse_label.config(text=f"Bonne réponse : {self.bonne_reponse}", foreground="#000000")
        elif resultat == "echec":
            # Fond rouge pour échec
            couleur_fond = '#a32c2c'
            # Afficher la bonne réponse en noir
            self.bonne_reponse_label.config(text=f"Bonne réponse : {self.bonne_reponse}", foreground="#000000")

        # Changer la couleur de fond de TOUTE la fenêtre et tous ses éléments
        self.root.configure(bg=couleur_fond)

        # Obtenir le style et changer la couleur de tous les éléments
        style = ttk.Style()
        style.configure('TFrame', background=couleur_fond)
        style.configure('TLabel', background=couleur_fond)

        # Remettre le fond neutre après 750ms
        self.root.after(750, self.remettre_fond_neutre)

    def update_percentage_display(self):
        """Met à jour l'affichage du pourcentage de bonnes réponses"""
        if self.total_questions > 0:
            percentage = (self.correct_answers / self.total_questions) * 100
            self.percentage_label.config(
                text=f"{percentage:.1f}% ({self.correct_answers}/{self.total_questions})"
            )
        else:
            self.percentage_label.config(text="0% (0/0)")

    def remettre_fond_neutre(self):
        """Remet le fond neutre de toute la fenêtre"""
        self.root.configure(bg='#454545')
        style = ttk.Style()
        style.configure('TFrame', background='#454545')
        style.configure('TLabel', background='#454545')
        # Passer à la nouvelle question
        self.nouvelle_question()

    def changer_dictionnaire(self):
        """Change le type de dictionnaire utilisé"""
        global dictionnaire, mots_francais, mots_espagnols

        # Cycle entre les valeurs 1 et 2
        dictionnaire = 1 if dictionnaire == 2 else 2

        # Recharger le dictionnaire
        mots_francais.clear()
        mots_espagnols.clear()

        # Chemin de base
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Choisir le bon fichier avec la bonne extension
        if dictionnaire == 1:
            fichier_dictionnaire = os.path.join(base_dir, 'Dictionnaires', 'dictionnaire_spanish.txt')
        else:
            fichier_dictionnaire = os.path.join(base_dir, 'Dictionnaires', 'dictionnaire_spanish_sample.txt')

        # Recharger les mots
        try:
            with open(fichier_dictionnaire, 'r', encoding='utf-8') as fichier:
                for ligne in fichier:
                    ligne = ligne.strip()
                    if '%' in ligne:
                        francais, espagnol = ligne.split(' % ')
                        mots_francais.append(francais)
                        mots_espagnols.append(espagnol)
        except FileNotFoundError:
            messagebox.showerror("Erreur", f"Le fichier dictionnaire est introuvable :\n{fichier_dictionnaire}")
            # Restaurer des valeurs par défaut pour éviter le crash
            mots_francais.append("Erreur")
            mots_espagnols.append("Fichier introuvable")

        if not mots_francais:
             mots_francais.append("Vide")
             mots_espagnols.append("Dictionnaire vide")

        # Mettre à jour l'affichage
        self.mettre_a_jour_statuts()
        # Générer une nouvelle question si on est en mode traduction
        if hasattr(self, 'mode_actuel') and self.mode_actuel == 'traduction':
            self.nouvelle_question()

    def changer_training_type(self):
        """Change le type d'entraînement"""
        global training_type

        # Cycle entre 0, 1, 2
        training_type = (training_type + 1) % 3

        # Mettre à jour l'affichage
        self.mettre_a_jour_statuts()
        # Générer une nouvelle question
        self.nouvelle_question()

    def changer_irregular_mode(self):
        """Change le mode verbes irréguliers"""
        global verb_mode

        # Basculer entre les trois modes
        verb_mode = (verb_mode + 1) % 3

        # Mettre à jour l'affichage
        self.mettre_a_jour_statuts()
        # Générer une nouvelle question si on est en mode conjugaison
        if hasattr(self, 'mode_actuel') and self.mode_actuel == 'conjugaison':
            self.nouvelle_question()

    def mettre_a_jour_statuts(self):
        """Met à jour l'affichage des statuts sous chaque bouton"""
        # Statut dictionnaire
        if dictionnaire == 1:
            self.dict_status.config(text="Complet", foreground="#2563eb")
        else:
            self.dict_status.config(text="Échantillon", foreground="#16a34a")

        # Statut type d'entraînement
        if training_type == 0:
            self.training_status.config(text="Mixte\n(25% conj / 75% trad)", foreground="#7c3aed")
        elif training_type == 1:
            self.training_status.config(text="Traduction\nuniquement", foreground="#dc2626")
        else:
            self.training_status.config(text="Conjugaison\nuniquement", foreground="#ea580c")

        # Statut verbes irréguliers
        if verb_mode == 1:
            self.irregular_status.config(text="Irréguliers\nseulement", foreground="#be185d")
        elif verb_mode == 2:
            self.irregular_status.config(text="Réguliers\nseulement", foreground="#4caf50")
        else:
            self.irregular_status.config(text="Tous les\nverbes", foreground="#059669")

    def quitter_application(self):
        """Ferme l'application"""
        self.root.quit()
        self.root.destroy()


# Remplacer la boucle while par l'interface graphique
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

import random
import tkinter as tk
from tkinter import ttk, messagebox

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

# créé une liste qui contient tous les mots en portugais (après le "%" dans dictionnaire.txt)
mots_portugais = []

# Choix du fichier dictionnaire en fonction de la variable
if dictionnaire == 1:
    fichier_dictionnaire = '../Dictionnaires/dictionnaire_portuguese.txt'
elif dictionnaire == 2:
    fichier_dictionnaire = '../Dictionnaires/dictionnaire_portuguese_sample.txt'
else:
    fichier_dictionnaire = '../Dictionnaires/dictionnaire_portuguese.txt'

# Lecture du fichier dictionnaire
with open(fichier_dictionnaire, 'r', encoding='utf-8') as fichier:
    for ligne in fichier:
        ligne = ligne.strip()
        if '%' in ligne:
            francais, portugais = ligne.split(' % ')
            mots_francais.append(francais)
            mots_portugais.append(portugais)

# Verbes pour la conjugaison (infinitif en portugais)
verbes_ar = [
    'amar', 'andar', 'ajudar', 'arrumar', 'atuar', 'brincar', 'cantar', 'chamar', 'chegar',
    'comprar', 'conversar', 'cortar', 'dançar', 'desejar', 'encontrar', 'escutar', 'estudar',
    'falar', 'ganhar', 'gostar', 'guardar', 'jogar', 'lavar', 'levar', 'mandar', 'mudar',
    'nadar', 'pagar', 'pensar', 'preparar', 'procurar', 'trabalhar', 'usar', 'visitar', 'voltar'
]

verbes_er = [
    'aprender', 'beber', 'comer', 'correr', 'crescer', 'dever', 'entender', 'escrever', 'escolher',
    'esquecer', 'morrer', 'mover', 'nascer', 'perder', 'prometer', 'receber', 'resolver',
    'responder', 'vender', 'proteger', 'chover', 'suceder', 'esconder', 'temer', 'valer',
    'meter', 'reconhecer', 'reter', 'tecer', 'oferecer', 'absorver', 'agradecer', 'depender',
    'persuadir', 'conceder'
]

verbes_ir = [
    'admitir', 'assistir', 'compartir', 'construir', 'decidir', 'discutir', 'dormir', 'fugir',
    'impedir', 'insistir', 'investir', 'omitir', 'partir', 'permitir', 'proibir',
    'repetir', 'seguir', 'servir', 'subir', 'sumir', 'vestir', 'consentir',
    'distribuir', 'dividir', 'imprimir', 'instruir', 'garantir', 'cobrir',
    'concluir', 'agir', 'assistir', 'punir', 'polir', 'definir', 'decrescer'
]

# Verbes irréguliers
verbes_irreguliers = ['ser', 'estar', 'ter', 'fazer', 'vir', 'ir', 'poder', 'dizer', 'saber', 'ver', 'dar', 'trazer',
                      'querer']
verbes_irreguliers_connus = []
verbes_irreguliers_pas_connus = []

# Temps
temps = ['imparfait']
temps_connus = ['impératif', 'conditionnel présent', 'passé', 'présent', 'futur', 'gérondif', 'participe passé']
temps_pas_connus = ['présent du subjonctif', 'imparfait du subjonctif', 'futur du subjonctif']

# Pronoms
pronoms = ['eu', 'ele/você/a gente', 'nós', 'eles/vocês']

# Terminaisons par temps et pronom
terminaisons = {
    'ar': {
        'présent': ['o', 'a', 'amos', 'am'],
        'passé': ['ei', 'ou', 'amos', 'aram'],
        'futur': ['arei', 'ará', 'aremos', 'arão'],
        'imparfait': ['ava', 'ava', 'ávamos', 'avam'],
        'présent du subjonctif': ['e', 'e', 'emos', 'em'],
        'imparfait du subjonctif': ['asse', 'asse', 'ássemos', 'assem'],
        'futur du subjonctif': ['ar', 'ar', 'armos', 'arem'],
        'participe passé': ['ado', 'ado', 'ado', 'ado'],
        'gérondif': ['ando', 'ando', 'ando', 'ando'],
        'impératif': ['', 'e', 'emos', 'em'],
        'conditionnel présent': ['aria', 'aria', 'aríamos', 'ariam']
    },
    'er': {
        'présent': ['o', 'e', 'emos', 'em'],
        'passé': ['i', 'eu', 'emos', 'eram'],
        'futur': ['erei', 'erá', 'eremos', 'erão'],
        'imparfait': ['ia', 'ia', 'íamos', 'iam'],
        'présent du subjonctif': ['a', 'a', 'amos', 'am'],
        'imparfait du subjonctif': ['esse', 'esse', 'êssemos', 'essem'],
        'futur du subjonctif': ['er', 'er', 'ermos', 'erem'],
        'participe passé': ['ido', 'ido', 'ido', 'ido'],
        'gérondif': ['endo', 'endo', 'endo', 'endo'],
        'impératif': ['', 'a', 'amos', 'am'],
        'conditionnel présent': ['eria', 'eria', 'eríamos', 'eriam']
    },
    'ir': {
        'présent': ['o', 'e', 'imos', 'em'],
        'passé': ['i', 'iu', 'imos', 'iram'],
        'futur': ['irei', 'irá', 'iremos', 'irão'],
        'imparfait': ['ia', 'ia', 'íamos', 'iam'],
        'présent du subjonctif': ['a', 'a', 'amos', 'am'],
        'imparfait du subjonctif': ['isse', 'isse', 'íssemos', 'issem'],
        'futur du subjonctif': ['ir', 'ir', 'irmos', 'irem'],
        'participe passé': ['ido', 'ido', 'ido', 'ido'],
        'gérondif': ['indo', 'indo', 'indo', 'indo'],
        'impératif': ['', 'a', 'amos', 'am'],
        'conditionnel présent': ['iria', 'iria', 'iríamos', 'iriam']
    }
}

# Terminaisons spéciales pour les verbes irréguliers
terminaisons_ter = {
    'présent': ['tenho', 'tem', 'temos', 'têm'],
    'passé': ['tive', 'teve', 'tivemos', 'tiveram'],
    'futur': ['terei', 'terá', 'teremos', 'terão'],
    'imparfait': ['tinha', 'tinha', 'tínhamos', 'tinham'],
    'présent du subjonctif': ['tenha', 'tenha', 'tenhamos', 'tenham'],
    'imparfait du subjonctif': ['tivesse', 'tivesse', 'tivéssemos', 'tivessem'],
    'futur du subjonctif': ['tiver', 'tiver', 'tivermos', 'tiverem'],
    'participe passé': ['tido', 'tido', 'tido', 'tido'],
    'gérondif': ['tendo', 'tendo', 'tendo', 'tendo'],
    'impératif': ['', 'tenha', 'tenhamos', 'tenham'],
    'conditionnel présent': ['teria', 'teria', 'teríamos', 'teriam']
}

terminaisons_fazer = {
    'présent': ['faço', 'faz', 'fazemos', 'fazem'],
    'passé': ['fiz', 'fez', 'fizemos', 'fizeram'],
    'futur': ['farei', 'fará', 'faremos', 'farão'],
    'imparfait': ['fazia', 'fazia', 'fazíamos', 'faziam'],
    'présent du subjonctif': ['faça', 'faça', 'façamos', 'façam'],
    'imparfait du subjonctif': ['fizesse', 'fizesse', 'fizéssemos', 'fizessem'],
    'futur du subjonctif': ['fizer', 'fizer', 'fizermos', 'fizerem'],
    'participe passé': ['feito', 'feito', 'feito', 'feito'],
    'gérondif': ['fazendo', 'fazendo', 'fazendo', 'fazendo'],
    'impératif': ['', 'faça', 'façamos', 'façam'],
    'conditionnel présent': ['faria', 'faria', 'faríamos', 'fariam']
}

terminaisons_ser = {
    'présent': ['sou', 'é', 'somos', 'são'],
    'passé': ['fui', 'foi', 'fomos', 'foram'],
    'futur': ['serei', 'será', 'seremos', 'serão'],
    'imparfait': ['era', 'era', 'éramos', 'eram'],
    'présent du subjonctif': ['seja', 'seja', 'sejamos', 'sejam'],
    'imparfait du subjonctif': ['fosse', 'fosse', 'fôssemos', 'fossem'],
    'futur du subjonctif': ['for', 'for', 'formos', 'forem'],
    'participe passé': ['sido', 'sido', 'sido', 'sido'],
    'gérondif': ['sendo', 'sendo', 'sendo', 'sendo'],
    'impératif': ['', 'seja', 'sejamos', 'sejam'],
    'conditionnel présent': ['seria', 'seria', 'seríamos', 'seriam']
}

terminaisons_estar = {
    'présent': ['estou', 'está', 'estamos', 'estão'],
    'passé': ['estive', 'esteve', 'estivemos', 'estiveram'],
    'futur': ['estarei', 'estará', 'estaremos', 'estarão'],
    'imparfait': ['estava', 'estava', 'estávamos', 'estavam'],
    'présent du subjonctif': ['esteja', 'esteja', 'estejamos', 'estejam'],
    'imparfait du subjonctif': ['estivesse', 'estivesse', 'estivéssemos', 'estivessem'],
    'futur du subjonctif': ['estiver', 'estiver', 'estivermos', 'estiverem'],
    'participe passé': ['estado', 'estado', 'estado', 'estado'],
    'gérondif': ['estando', 'estando', 'estando', 'estando'],
    'impératif': ['', 'esteja', 'estejamos', 'estejam'],
    'conditionnel présent': ['estaria', 'estaria', 'estaríamos', 'estariam']
}

terminaisons_vir = {
    'présent': ['venho', 'vem', 'vimos', 'vêm'],
    'passé': ['vim', 'veio', 'viemos', 'vieram'],
    'futur': ['virei', 'virá', 'viremos', 'virão'],
    'imparfait': ['vinha', 'vinha', 'vínhamos', 'vinham'],
    'présent du subjonctif': ['venha', 'venha', 'venhamos', 'venham'],
    'imparfait du subjonctif': ['viesse', 'viesse', 'viéssemos', 'viessem'],
    'futur du subjonctif': ['vier', 'vier', 'viermos', 'vierem'],
    'participe passé': ['vindo', 'vindo', 'vindo', 'vindo'],
    'gérondif': ['vindo', 'vindo', 'vindo', 'vindo'],
    'impératif': ['', 'venha', 'venhamos', 'venham'],
    'conditionnel présent': ['viria', 'viria', 'viríamos', 'viriam']
}

terminaisons_ir = {
    'présent': ['vou', 'vai', 'vamos', 'vão'],
    'passé': ['fui', 'foi', 'fomos', 'foram'],
    'futur': ['irei', 'irá', 'iremos', 'irão'],
    'imparfait': ['ia', 'ia', 'íamos', 'iam'],
    'présent du subjonctif': ['vá', 'vá', 'vamos', 'vão'],
    'imparfait du subjonctif': ['fosse', 'fosse', 'fôssemos', 'fossem'],
    'futur du subjonctif': ['for', 'for', 'formos', 'forem'],
    'participe passé': ['ido', 'ido', 'ido', 'ido'],
    'gérondif': ['indo', 'indo', 'indo', 'indo'],
    'impératif': ['', 'vá', 'vamos', 'vão'],
    'conditionnel présent': ['iria', 'iria', 'iríamos', 'iriam']
}

terminaisons_poder = {
    'présent': ['posso', 'pode', 'podemos', 'podem'],
    'passé': ['pude', 'pôde', 'pudemos', 'puderam'],
    'futur': ['poderei', 'poderá', 'poderemos', 'poderão'],
    'imparfait': ['podia', 'podia', 'podíamos', 'podiam'],
    'présent du subjonctif': ['possa', 'possa', 'possamos', 'possam'],
    'imparfait du subjonctif': ['pudesse', 'pudesse', 'pudéssemos', 'pudessem'],
    'futur du subjonctif': ['puder', 'puder', 'pudermos', 'puderem'],
    'participe passé': ['podido', 'podido', 'podido', 'podido'],
    'gérondif': ['podendo', 'podendo', 'podendo', 'podendo'],
    'impératif': ['', 'possa', 'possamos', 'possam'],
    'conditionnel présent': ['poderia', 'poderia', 'poderíamos', 'poderiam']
}

# Nouvelles terminaisons irrégulières
terminaisons_dizer = {
    'présent': ['digo', 'diz', 'dizemos', 'dizem'],
    'passé': ['disse', 'disse', 'dissemos', 'disseram'],
    'futur': ['direi', 'dirá', 'diremos', 'dirão'],
    'imparfait': ['dizia', 'dizia', 'dizíamos', 'diziam'],
    'présent du subjonctif': ['diga', 'diga', 'digamos', 'digam'],
    'imparfait du subjonctif': ['dissesse', 'dissesse', 'disséssemos', 'dissessem'],
    'futur du subjonctif': ['disser', 'disser', 'dissermos', 'disserem'],
    'participe passé': ['dito', 'dito', 'dito', 'dito'],
    'gérondif': ['dizendo', 'dizendo', 'dizendo', 'dizendo'],
    'impératif': ['', 'diga', 'digamos', 'digam'],
    'conditionnel présent': ['diria', 'diria', 'diríamos', 'diriam']
}

terminaisons_saber = {
    'présent': ['sei', 'sabe', 'sabemos', 'sabem'],
    'passé': ['soube', 'soube', 'soubemos', 'souberam'],
    'futur': ['saberei', 'saberá', 'saberemos', 'saberão'],
    'imparfait': ['sabia', 'sabia', 'sabíamos', 'sabiam'],
    'présent du subjonctif': ['saiba', 'saiba', 'saibamos', 'saibam'],
    'imparfait du subjonctif': ['soubesse', 'soubesse', 'soubéssemos', 'soubessem'],
    'futur du subjonctif': ['souber', 'souber', 'soubermos', 'souberem'],
    'participe passé': ['sabido', 'sabido', 'sabido', 'sabido'],
    'gérondif': ['sabendo', 'sabendo', 'sabendo', 'sabendo'],
    'impératif': ['', 'saiba', 'saibamos', 'saibam'],
    'conditionnel présent': ['saberia', 'saberia', 'saberíamos', 'saberiam']
}

terminaisons_ver = {
    'présent': ['vejo', 'vê', 'vemos', 'veem'],
    'passé': ['vi', 'viu', 'vimos', 'viram'],
    'futur': ['verei', 'verá', 'veremos', 'verão'],
    'imparfait': ['via', 'via', 'víamos', 'viam'],
    'présent du subjonctif': ['veja', 'veja', 'vejamos', 'vejam'],
    'imparfait du subjonctif': ['visse', 'visse', 'víssemos', 'vissem'],
    'futur du subjonctif': ['vir', 'vir', 'virmos', 'virem'],
    'participe passé': ['visto', 'visto', 'visto', 'visto'],
    'gérondif': ['vendo', 'vendo', 'vendo', 'vendo'],
    'impératif': ['', 'veja', 'vejamos', 'vejam'],
    'conditionnel présent': ['veria', 'veria', 'veríamos', 'veriam']
}

terminaisons_dar = {
    'présent': ['dou', 'dá', 'damos', 'dão'],
    'passé': ['dei', 'deu', 'demos', 'deram'],
    'futur': ['darei', 'dará', 'daremos', 'darão'],
    'imparfait': ['dava', 'dava', 'dávamos', 'davam'],
    'présent du subjonctif': ['dê', 'dê', 'demos', 'deem'],
    'imparfait du subjonctif': ['desse', 'desse', 'déssemos', 'dessem'],
    'futur du subjonctif': ['der', 'der', 'dermos', 'derem'],
    'participe passé': ['dado', 'dado', 'dado', 'dado'],
    'gérondif': ['dando', 'dando', 'dando', 'dando'],
    'impératif': ['', 'dê', 'demos', 'deem'],
    'conditionnel présent': ['daria', 'daria', 'daríamos', 'dariam']
}

terminaisons_trazer = {
    'présent': ['trago', 'traz', 'trazemos', 'trazem'],
    'passé': ['trouxe', 'trouxe', 'trouxemos', 'trouxeram'],
    'futur': ['trarei', 'trará', 'traremos', 'trarão'],
    'imparfait': ['trazia', 'trazia', 'trazíamos', 'traziam'],
    'présent du subjonctif': ['tragam', 'tragam', 'tragamos', 'tragam'],
    'imparfait du subjonctif': ['trouxesse', 'trouxesse', 'trouxéssemos', 'trouxessem'],
    'futur du subjonctif': ['trouxer', 'trouxer', 'trouxermos', 'trouxerem'],
    'participe passé': ['trado', 'trado', 'trado', 'trado'],
    'gérondif': ['trazendo', 'trazendo', 'trazendo', 'trazendo'],
    'impératif': ['', 'tragam', 'tragamos', 'tragam'],
    'conditionnel présent': ['traria', 'traria', 'traríamos', 'trariam']
}

terminaisons_querer = {
    'présent': ['quero', 'quer', 'queremos', 'querem'],
    'passé': ['quis', 'quis', 'quisemos', 'quiseram'],
    'futur': ['quererei', 'quererá', 'quereremos', 'quererão'],
    'imparfait': ['queria', 'queria', 'queríamos', 'queriam'],
    'présent du subjonctif': ['queira', 'queira', 'queiramos', 'queiram'],
    'imparfait du subjonctif': ['quisesse', 'quisesse', 'quiséssemos', 'quisessem'],
    'futur du subjonctif': ['quiser', 'quiser', 'quisermos', 'quiserem'],
    'participe passé': ['querido', 'querido', 'querido', 'querido'],
    'gérondif': ['querendo', 'querendo', 'querendo', 'querendo'],
    'impératif': ['', 'queira', 'queiramos', 'queiram'],
    'conditionnel présent': ['quereria', 'quereria', 'quereríamos', 'quereriam']
}


def conjuguer_verbe(verbe, pronom_index, temps_choisi):
    """Conjugue un verbe selon le pronom et le temps donnés"""
    # Vérifier si c'est un verbe irrégulier
    if verbe == 'ter':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_ter[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_ter[temps_choisi][pronom_index]
    elif verbe == 'fazer':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_fazer[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_fazer[temps_choisi][pronom_index]
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
    elif verbe == 'vir':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_vir[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_vir[temps_choisi][pronom_index]
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
    elif verbe == 'dizer':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_dizer[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_dizer[temps_choisi][pronom_index]
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
    elif verbe == 'trazer':
        if temps_choisi == 'participe passé' or temps_choisi == 'gérondif':
            return terminaisons_trazer[temps_choisi][0]
        elif temps_choisi == 'impératif' and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_trazer[temps_choisi][pronom_index]
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
        # L'impératif n'a pas de forme pour "eu"
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

        self.root.title("Portugais")

        # Mettre la fenêtre en vrai plein écran
        self.root.attributes('-fullscreen', True)

        # Variables pour stocker la question actuelle
        self.mode_actuel = None
        self.bonne_reponse = None
        self.verbe_choisi = None
        self.pronom_index = None
        self.temps_choisi = None
        self.index_aleatoire = None

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
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

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
        self.reponse_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
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

        # Toujours français vers portugais
        mot_affiche = mots_francais[self.index_aleatoire]
        self.bonne_reponse = mots_portugais[self.index_aleatoire]

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
            # Vérification pour la traduction (toujours français vers portugais)
            try:
                index_reponse = mots_portugais.index(reponse_utilisateur)
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
        global dictionnaire, mots_francais, mots_portugais

        # Cycle entre les valeurs 1 et 2
        dictionnaire = 1 if dictionnaire == 2 else 2

        # Recharger le dictionnaire
        mots_francais.clear()
        mots_portugais.clear()

        # Choisir le bon fichier avec la bonne extension
        if dictionnaire == 1:
            fichier_dictionnaire = 'dictionnaire.txt'
        else:
            fichier_dictionnaire = 'dictionnaire_sample.txt'

        # Recharger les mots
        with open(fichier_dictionnaire, 'r', encoding='utf-8') as fichier:
            for ligne in fichier:
                ligne = ligne.strip()
                if '%' in ligne:
                    francais, portugais = ligne.split(' % ')
                    mots_francais.append(francais)
                    mots_portugais.append(portugais)

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

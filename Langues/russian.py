import random
import tkinter as tk
from tkinter import ttk, messagebox
import os
import csv
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ============== CONFIGURATION ==============
AUTO_SAVE_THRESHOLD = 100  # Nombre d'essais avant auto-sauvegarde

# Objectifs par catégorie (%)
GOALS = {
    'reguliers': 85,      # Conjugaison verbes réguliers
    'irreguliers': 80,    # Conjugaison verbes irréguliers  
    'vocabulaire': 70,    # Vocabulaire dictionnaire complet
    'tout': 70            # Tous les verbes + tout le vocabulaire
}

# Noms des fichiers par catégorie
CATEGORY_FILES = {
    'reguliers': 'conjugaison_reguliers',
    'irreguliers': 'conjugaison_irreguliers',
    'vocabulaire': 'vocabulaire',
    'tout': 'tout'
}

# Chemins des fichiers
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'Data', 'Russian')
GRAPHS_DIR = os.path.join(BASE_DIR, 'Graphs', 'Russian')

# Créer les dossiers s'ils n'existent pas
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(GRAPHS_DIR, exist_ok=True)

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

# créé une liste qui contient tous les mots en russe (après le "%" dans dictionnaire.txt)
mots_russes = []

# Choix du fichier dictionnaire en fonction de la variable
if dictionnaire == 1:
    fichier_dictionnaire = os.path.join(BASE_DIR, 'Dictionnaires', 'dictionnaire_russian.txt')
elif dictionnaire == 2:
    fichier_dictionnaire = os.path.join(BASE_DIR, 'Dictionnaires', 'dictionnaire_russian_sample.txt')
else:
    fichier_dictionnaire = os.path.join(BASE_DIR, 'Dictionnaires', 'dictionnaire_russian.txt')

# Lecture du fichier dictionnaire
try:
    with open(fichier_dictionnaire, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if '%' in ligne:
                francais, russe = ligne.split(' % ')
                mots_francais.append(francais)
                mots_russes.append(russe)
except FileNotFoundError:
    print(f"Erreur: Le fichier dictionnaire est introuvable: {fichier_dictionnaire}")

# Vérification que le dictionnaire n'est pas vide
if not mots_francais:
    mots_francais = ["Erreur"]
    mots_russes = ["Dictionnaire vide ou introuvable"]

# ============== VERBES RUSSES (translittération latine) ==============
# Le signe mou (ь) est représenté par une apostrophe droite dans les noms de verbes
# mais on utilise des guillemets doubles pour éviter les conflits Python

# Verbes réguliers 1ère conjugaison (en -at')
verbes_1ere_conj = [
    "tchitat'", "dyelat'", "znat'", "igrat'", "goulyat'", "doumat'", "rabotat'",
    "slouchat'", "polagat'", "pytsat'", "pisat'", "iskat'",
    "otvyetchat'", "koupat'", "pomogat'", "vybirat'", "posylat'",
    "nachinat'", "kontchat'", "otkryvat'", "zakryvat'",
    "priglachat'", "obyedat'", "oujinat'", "zavtrakat'"
]

# Verbes réguliers 2ème conjugaison (en -it')
verbes_2eme_conj = [
    "govorit'", "khodit'", "lyoubit'", "outchit'", "videt'",
    "smotret'", "stoyat'", "sidet'", "lyejat'", "spat'", "derjat'",
    "nosit'", "prosit'", "platit'", "gotovit'", "stroit'", "zvonit'",
    "kourit'", "khotyet'", "loujit'sya", "stanovit'sya",
    "pokoupat'", "pomnit'", "kontchit'",
    "poloutchit'", "otpravit'"
]

# Verbes irréguliers (les plus courants)
verbes_irreguliers = [
    "byt'", "yest'", "pit'", "dat'", "jit'", "idti", "yekhat'",
    "motch'", "khotyet'", "brat'", "stat'", "vzyat'"
]
verbes_irreguliers_connus = []
verbes_irreguliers_pas_connus = []

# Temps
temps = ["présent", "passé", "futur", "impératif", "participe passé", "gérondif"]
temps_connus = []
temps_pas_connus = []

# Pronoms russes (translittérés)
pronoms = ["ya", "ty", "on/ona", "my", "vy", "oni"]

# ============== TERMINAISONS RÉGULIÈRES ==============

# Terminaisons pour les verbes réguliers
terminaisons = {
    "1ere": {
        "présent": ["you", "yech'", "yet", "yem", "yete", "yout"],
        "passé": ["l", "l", "l/la", "li", "li", "li"],
        "futur": ["boudou", "boudech'", "boudyet", "boudyem", "boudyete", "boudout"],
        "impératif": ["", "i", "", "", "ite", ""],
        "participe passé": ["l", "l", "l", "l", "l", "l"],
        "gérondif": ["ya", "ya", "ya", "ya", "ya", "ya"]
    },
    "2eme": {
        "présent": ["you", "ich'", "it", "im", "ite", "yat"],
        "passé": ["l", "l", "l/la", "li", "li", "li"],
        "futur": ["boudou", "boudech'", "boudyet", "boudyem", "boudyete", "boudout"],
        "impératif": ["", "i", "", "", "ite", ""],
        "participe passé": ["l", "l", "l", "l", "l", "l"],
        "gérondif": ["ya", "ya", "ya", "ya", "ya", "ya"]
    }
}

# ============== CONJUGAISONS IRRÉGULIÈRES ==============

# byt' (быть - être)
terminaisons_byt = {
    "présent": ["-", "-", "-", "-", "-", "-"],
    "passé": ["byl", "byl", "byl/byla", "byli", "byli", "byli"],
    "futur": ["boudou", "boudech'", "boudyet", "boudyem", "boudyete", "boudout"],
    "impératif": ["", "boud'", "", "", "boud'te", ""],
    "participe passé": ["byvchii", "byvchii", "byvchii", "byvchii", "byvchii", "byvchii"],
    "gérondif": ["boudoutchi", "boudoutchi", "boudoutchi", "boudoutchi", "boudoutchi", "boudoutchi"]
}

# yest' (есть - manger)
terminaisons_yest = {
    "présent": ["yem", "yech'", "yest", "yedim", "yedite", "yedyat"],
    "passé": ["yel", "yel", "yel/yela", "yeli", "yeli", "yeli"],
    "futur": ["boudou yest'", "boudech' yest'", "boudyet yest'", "boudyem yest'", "boudyete yest'", "boudout yest'"],
    "impératif": ["", "yech'", "", "", "yech'te", ""],
    "participe passé": ["yevchii", "yevchii", "yevchii", "yevchii", "yevchii", "yevchii"],
    "gérondif": ["yedya", "yedya", "yedya", "yedya", "yedya", "yedya"]
}

# pit' (пить - boire)
terminaisons_pit = {
    "présent": ["p'you", "p'yoch'", "p'yot", "p'yom", "p'yote", "p'yout"],
    "passé": ["pil", "pil", "pil/pila", "pili", "pili", "pili"],
    "futur": ["boudou pit'", "boudech' pit'", "boudyet pit'", "boudyem pit'", "boudyete pit'", "boudout pit'"],
    "impératif": ["", "pyei", "", "", "pyeite", ""],
    "participe passé": ["pivchii", "pivchii", "pivchii", "pivchii", "pivchii", "pivchii"],
    "gérondif": ["piya", "piya", "piya", "piya", "piya", "piya"]
}

# dat' (дать - donner)
terminaisons_dat = {
    "présent": ["dayou", "dayoch'", "dayot", "dadim", "dadite", "dadout"],
    "passé": ["dal", "dal", "dal/dala", "dali", "dali", "dali"],
    "futur": ["dam", "dach'", "dast", "dadim", "dadite", "dadout"],
    "impératif": ["", "dai", "", "", "daite", ""],
    "participe passé": ["davchii", "davchii", "davchii", "davchii", "davchii", "davchii"],
    "gérondif": ["dav", "dav", "dav", "dav", "dav", "dav"]
}

# jit' (жить - vivre)
terminaisons_jit = {
    "présent": ["jivou", "jivyoch'", "jivyot", "jivyom", "jivyote", "jivout"],
    "passé": ["jil", "jil", "jil/jila", "jili", "jili", "jili"],
    "futur": ["boudou jit'", "boudech' jit'", "boudyet jit'", "boudyem jit'", "boudyete jit'", "boudout jit'"],
    "impératif": ["", "jivi", "", "", "jivite", ""],
    "participe passé": ["jivchii", "jivchii", "jivchii", "jivchii", "jivchii", "jivchii"],
    "gérondif": ["jivya", "jivya", "jivya", "jivya", "jivya", "jivya"]
}

# idti (идти - aller à pied)
terminaisons_idti = {
    "présent": ["idou", "idyoch'", "idyot", "idyom", "idyote", "idout"],
    "passé": ["chyol", "chyol", "chyol/chla", "chli", "chli", "chli"],
    "futur": ["boudou idti", "boudech' idti", "boudyet idti", "boudyem idti", "boudyete idti", "boudout idti"],
    "impératif": ["", "idi", "", "", "idite", ""],
    "participe passé": ["chedchii", "chedchii", "chedchii", "chedchii", "chedchii", "chedchii"],
    "gérondif": ["idya", "idya", "idya", "idya", "idya", "idya"]
}

# yekhat' (ехать - aller en véhicule)
terminaisons_yekhat = {
    "présent": ["yedou", "yedech'", "yedyet", "yedyem", "yedyete", "yedout"],
    "passé": ["yekhal", "yekhal", "yekhal/yekhala", "yekhali", "yekhali", "yekhali"],
    "futur": ["boudou yekhat'", "boudech' yekhat'", "boudyet yekhat'", "boudyem yekhat'", "boudyete yekhat'", "boudout yekhat'"],
    "impératif": ["", "yezjai", "", "", "yezjaite", ""],
    "participe passé": ["yekhavchii", "yekhavchii", "yekhavchii", "yekhavchii", "yekhavchii", "yekhavchii"],
    "gérondif": ["yekhav", "yekhav", "yekhav", "yekhav", "yekhav", "yekhav"]
}

# motch' (мочь - pouvoir)
terminaisons_motch = {
    "présent": ["mogou", "mojech'", "mojyet", "mojyem", "mojyete", "mogout"],
    "passé": ["mog", "mog", "mog/mogla", "mogli", "mogli", "mogli"],
    "futur": ["smogou", "smojech'", "smojyet", "smojyem", "smojyete", "smogout"],
    "impératif": ["", "", "", "", "", ""],
    "participe passé": ["mogchii", "mogchii", "mogchii", "mogchii", "mogchii", "mogchii"],
    "gérondif": ["mogya", "mogya", "mogya", "mogya", "mogya", "mogya"]
}

# khotyet' (хотеть - vouloir)
terminaisons_khotyet = {
    "présent": ["khotchou", "khotchech'", "khotchet", "khotim", "khotite", "khotyat"],
    "passé": ["khotyel", "khotyel", "khotyel/khotyela", "khotyeli", "khotyeli", "khotyeli"],
    "futur": ["boudou khotyet'", "boudech' khotyet'", "boudyet khotyet'", "boudyem khotyet'", "boudyete khotyet'", "boudout khotyet'"],
    "impératif": ["", "khotchi", "", "", "khotchite", ""],
    "participe passé": ["khotyevchii", "khotyevchii", "khotyevchii", "khotyevchii", "khotyevchii", "khotyevchii"],
    "gérondif": ["khotya", "khotya", "khotya", "khotya", "khotya", "khotya"]
}

# brat' (брать - prendre)
terminaisons_brat = {
    "présent": ["byerou", "byeryoch'", "byeryot", "byeryom", "byeryote", "byerout"],
    "passé": ["bral", "bral", "bral/brala", "brali", "brali", "brali"],
    "futur": ["boudou brat'", "boudech' brat'", "boudyet brat'", "boudyem brat'", "boudyete brat'", "boudout brat'"],
    "impératif": ["", "byeri", "", "", "byerite", ""],
    "participe passé": ["bravchii", "bravchii", "bravchii", "bravchii", "bravchii", "bravchii"],
    "gérondif": ["byerya", "byerya", "byerya", "byerya", "byerya", "byerya"]
}

# stat' (стать - devenir)
terminaisons_stat = {
    "présent": ["stanou", "stanech'", "stanyet", "stanyem", "stanyete", "stanout"],
    "passé": ["stal", "stal", "stal/stala", "stali", "stali", "stali"],
    "futur": ["stanou", "stanech'", "stanyet", "stanyem", "stanyete", "stanout"],
    "impératif": ["", "stan'", "", "", "stan'te", ""],
    "participe passé": ["stavchii", "stavchii", "stavchii", "stavchii", "stavchii", "stavchii"],
    "gérondif": ["stav", "stav", "stav", "stav", "stav", "stav"]
}

# vzyat' (взять - prendre/saisir, perfectif)
terminaisons_vzyat = {
    "présent": ["-", "-", "-", "-", "-", "-"],
    "passé": ["vzyal", "vzyal", "vzyal/vzyala", "vzyali", "vzyali", "vzyali"],
    "futur": ["voz'mou", "voz'myoch'", "voz'myot", "voz'myom", "voz'myote", "voz'mout"],
    "impératif": ["", "voz'mi", "", "", "voz'mite", ""],
    "participe passé": ["vzyavchii", "vzyavchii", "vzyavchii", "vzyavchii", "vzyavchii", "vzyavchii"],
    "gérondif": ["vzyav", "vzyav", "vzyav", "vzyav", "vzyav", "vzyav"]
}


def conjuguer_verbe(verbe, pronom_index, temps_choisi):
    """Conjugue un verbe selon le pronom et le temps donnés"""
    # Vérifier si c'est un verbe irrégulier
    if verbe == "byt'":
        if temps_choisi == "participe passé" or temps_choisi == "gérondif":
            return terminaisons_byt[temps_choisi][0]
        elif temps_choisi == "impératif" and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_byt[temps_choisi][pronom_index]
    elif verbe == "yest'":
        if temps_choisi == "participe passé" or temps_choisi == "gérondif":
            return terminaisons_yest[temps_choisi][0]
        elif temps_choisi == "impératif" and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_yest[temps_choisi][pronom_index]
    elif verbe == "pit'":
        if temps_choisi == "participe passé" or temps_choisi == "gérondif":
            return terminaisons_pit[temps_choisi][0]
        elif temps_choisi == "impératif" and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_pit[temps_choisi][pronom_index]
    elif verbe == "dat'":
        if temps_choisi == "participe passé" or temps_choisi == "gérondif":
            return terminaisons_dat[temps_choisi][0]
        elif temps_choisi == "impératif" and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_dat[temps_choisi][pronom_index]
    elif verbe == "jit'":
        if temps_choisi == "participe passé" or temps_choisi == "gérondif":
            return terminaisons_jit[temps_choisi][0]
        elif temps_choisi == "impératif" and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_jit[temps_choisi][pronom_index]
    elif verbe == "idti":
        if temps_choisi == "participe passé" or temps_choisi == "gérondif":
            return terminaisons_idti[temps_choisi][0]
        elif temps_choisi == "impératif" and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_idti[temps_choisi][pronom_index]
    elif verbe == "yekhat'":
        if temps_choisi == "participe passé" or temps_choisi == "gérondif":
            return terminaisons_yekhat[temps_choisi][0]
        elif temps_choisi == "impératif" and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_yekhat[temps_choisi][pronom_index]
    elif verbe == "motch'":
        if temps_choisi == "participe passé" or temps_choisi == "gérondif":
            return terminaisons_motch[temps_choisi][0]
        elif temps_choisi == "impératif" and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_motch[temps_choisi][pronom_index]
    elif verbe == "khotyet'":
        if temps_choisi == "participe passé" or temps_choisi == "gérondif":
            return terminaisons_khotyet[temps_choisi][0]
        elif temps_choisi == "impératif" and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_khotyet[temps_choisi][pronom_index]
    elif verbe == "brat'":
        if temps_choisi == "participe passé" or temps_choisi == "gérondif":
            return terminaisons_brat[temps_choisi][0]
        elif temps_choisi == "impératif" and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_brat[temps_choisi][pronom_index]
    elif verbe == "stat'":
        if temps_choisi == "participe passé" or temps_choisi == "gérondif":
            return terminaisons_stat[temps_choisi][0]
        elif temps_choisi == "impératif" and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_stat[temps_choisi][pronom_index]
    elif verbe == "vzyat'":
        if temps_choisi == "participe passé" or temps_choisi == "gérondif":
            return terminaisons_vzyat[temps_choisi][0]
        elif temps_choisi == "impératif" and pronom_index == 0:
            return "Forme inexistante à l'impératif"
        else:
            return terminaisons_vzyat[temps_choisi][pronom_index]

    # Conjugaison régulière pour les autres verbes
    if verbe in verbes_1ere_conj:
        type_verbe = "1ere"
    elif verbe in verbes_2eme_conj:
        type_verbe = "2eme"
    else:
        return verbe  # Cas d'erreur

    # Extraire le radical (enlever at', it', et', etc.)
    if verbe.endswith("at'") or verbe.endswith("it'") or verbe.endswith("et'"):
        radical = verbe[:-3]
    elif verbe.endswith("t'"):
        radical = verbe[:-2]
    else:
        radical = verbe

    # Cas spéciaux pour certains temps
    if temps_choisi == "participe passé" or temps_choisi == "gérondif":
        terminaison = terminaisons[type_verbe][temps_choisi][0]
        return radical + terminaison
    elif temps_choisi == "impératif" and pronom_index == 0:
        return "Forme inexistante à l'impératif"
    else:
        terminaison = terminaisons[type_verbe][temps_choisi][pronom_index]
        return radical + terminaison


def get_current_category():
    """Détermine la catégorie actuelle basée sur training_type et verb_mode"""
    if training_type == 2:  # Conjugaison uniquement
        if verb_mode == 2:  # Réguliers uniquement
            return 'reguliers'
        elif verb_mode == 1:  # Irréguliers uniquement
            return 'irreguliers'
        else:  # Tous les verbes
            return 'tout'
    elif training_type == 1:  # Traduction uniquement
        return 'vocabulaire'
    else:  # Mixte
        return 'tout'


def generate_2d_graph(category):
    """Génère un graphique 2D de la progression pour une catégorie"""
    csv_file = os.path.join(DATA_DIR, f'{CATEGORY_FILES[category]}.csv')
    graph_file = os.path.join(GRAPHS_DIR, f'{CATEGORY_FILES[category]}_progress.png')
    goal = GOALS[category]
    
    if not os.path.exists(csv_file):
        return
    
    dates = []
    percentages = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    date_val = datetime.strptime(row['date'], '%Y-%m-%d')
                    pct_val = float(row['percentage'])
                    dates.append(date_val)
                    percentages.append(pct_val)
                except (ValueError, KeyError, TypeError):
                    continue
        
        if not dates or len(dates) != len(percentages):
            return
    except Exception:
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Progress points and line
    ax.plot(dates, percentages, 'b-o', markersize=8, linewidth=2, label='Scores')
    
    # Goal line (horizontal line at goal percentage)
    ax.axhline(y=goal, color='red', linestyle='--', linewidth=2, label=f'Goal: {goal}%')
    
    # Fix Y-axis limits (0 to 100%)
    ax.set_ylim(0, 100)
    
    # Category names in English
    category_names = {
        'reguliers': 'Regular Conjugation',
        'irreguliers': 'Irregular Conjugation',
        'vocabulaire': 'Vocabulary',
        'tout': 'All (Verbs + Vocabulary)'
    }
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Success rate (%)', fontsize=12)
    ax.set_title(f'Russian Progress - {category_names[category]} (Goal: {goal}%)', fontsize=14)
    
    # Format X-axis to display dates nicely
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    
    # Add grid for better readability
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(graph_file, dpi=150, bbox_inches='tight')
    plt.close()


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

        self.root.title("Russe")

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
        
        # Variables pour le suivi de catégorie et sauvegarde
        self.current_category = get_current_category()
        self.has_saved = False

        self.setup_ui()
        self.nouvelle_question()

    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def setup_ui(self):
        # Configuration de la grille principale
        self.root.columnconfigure(0, weight=1)
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

        # Label principal pour les questions de traduction
        self.question_label = ttk.Label(self.question_frame, text="",
                                        font=("Arial", 50, "bold"),
                                        wraplength=900,
                                        justify="center")

        # Labels spéciaux pour les questions de conjugaison avec couleurs
        self.conjugaison_frame = ttk.Frame(self.question_frame)

        # Nouveau frame pour regrouper intro + irrégulier sur une seule ligne
        self.titre_frame = ttk.Frame(self.conjugaison_frame)

        self.intro_label = ttk.Label(self.titre_frame, text="",
                                     font=("Arial", 55, "bold"),
                                     justify="center")

        self.irregulier_label = ttk.Label(self.titre_frame, text="",
                                          font=("Arial", 60, "bold"),
                                          foreground="#9500ff",
                                          justify="center")

        self.verbe_label = ttk.Label(self.conjugaison_frame, text="",
                                     font=("Arial", 65, "bold"),
                                     foreground="#e74c3c",
                                     justify="center")

        self.temps_label = ttk.Label(self.conjugaison_frame, text="",
                                     font=("Arial", 65, "bold"),
                                     foreground="#3498db",
                                     justify="center")

        self.pronom_label = ttk.Label(self.conjugaison_frame, text="",
                                      font=("Arial", 65, "bold"),
                                      foreground="#2bc46c",
                                      justify="center")

        # Frame pour la saisie
        saisie_frame = ttk.Frame(main_frame)
        saisie_frame.grid(row=2, column=0, pady=(0, 15))
        saisie_frame.columnconfigure(0, weight=1)

        # Champ de saisie
        self.reponse_entry = ttk.Entry(saisie_frame, font=("Arial", 45), width=20)
        self.reponse_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.reponse_entry.bind('<Return>', lambda e: self.verifier_reponse())

        # Bouton valider
        self.valider_btn = ttk.Button(main_frame, text="Valider",
                                      command=self.verifier_reponse)
        self.valider_btn.config(width=10)
        style = ttk.Style()
        style.configure("Large.TButton", font=("Arial", 40, "bold"))
        self.valider_btn.config(style="Large.TButton")
        self.valider_btn.grid(row=3, column=0, pady=(0, 10))

        # Frame pour les boutons de contrôle
        controles_frame = ttk.Frame(main_frame)
        controles_frame.grid(row=4, column=0, pady=(0, 0))

        controles_frame.columnconfigure(0, weight=1)
        controles_frame.columnconfigure(1, weight=1)
        controles_frame.columnconfigure(2, weight=1)

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

        # Frame pour boutons Enregistrer et Quitter
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=5, column=0, pady=(20, 10))
        
        style.configure("Save.TButton", font=("Arial", 20, "bold"))
        self.save_btn = ttk.Button(bottom_frame, text="Enregistrer",
                                   command=self.save_progress,
                                   style="Save.TButton")
        self.save_btn.grid(row=0, column=0, padx=20)
        
        self.quit_btn = ttk.Button(bottom_frame, text="Quitter",
                                   command=self.quitter_application,
                                   style="Control.TButton")
        self.quit_btn.grid(row=0, column=1, padx=20)

        # Label pour afficher le pourcentage de bonnes réponses (en bas)
        self.percentage_label = ttk.Label(main_frame, text="0% (0/0)",
                                          font=("Arial", 24, "bold"),
                                          foreground="#00bcd4",
                                          justify="center")
        self.percentage_label.grid(row=6, column=0, pady=(10, 5))

        # Label pour afficher l'objectif de la catégorie
        self.goal_label = ttk.Label(main_frame, text="",
                                    font=("Arial", 18),
                                    foreground="#ff6b6b",
                                    justify="center")
        self.goal_label.grid(row=7, column=0, pady=(0, 20))

        # Mettre à jour l'affichage des statuts
        self.mettre_a_jour_statuts()
        self.update_goal_display()

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
            if random.random() * 100 < 25:
                self.mode_actuel = 'conjugaison'
            else:
                self.mode_actuel = 'traduction'
        elif training_type == 1:
            self.mode_actuel = 'traduction'
        elif training_type == 2:
            self.mode_actuel = 'conjugaison'

        if self.mode_actuel == 'traduction':
            self.generer_question_traduction()
        else:
            self.generer_question_conjugaison()

        self.reponse_entry.focus()

    def generer_question_traduction(self):
        self.index_aleatoire = random.randint(0, len(mots_francais) - 1)

        # Toujours français vers russe
        mot_affiche = mots_francais[self.index_aleatoire]
        self.bonne_reponse = mots_russes[self.index_aleatoire]

        # Masquer le frame de conjugaison et afficher le label simple
        self.conjugaison_frame.pack_forget()
        self.question_label.pack(pady=20)
        self.question_label.config(text=f"\n\n{mot_affiche}", foreground="#d6c124")

    def generer_question_conjugaison(self):
        # Choisir les verbes selon la variable verb_mode
        if verb_mode == 1:
            tous_verbes = verbes_irreguliers
        elif verb_mode == 2:
            tous_verbes = verbes_1ere_conj + verbes_2eme_conj
        else:
            tous_verbes = verbes_1ere_conj + verbes_2eme_conj + verbes_irreguliers

        self.verbe_choisi = random.choice(tous_verbes)
        pronom_choisi = random.choice(pronoms)
        self.pronom_index = pronoms.index(pronom_choisi)
        self.temps_choisi = random.choice(temps)

        self.bonne_reponse = conjuguer_verbe(self.verbe_choisi, self.pronom_index, self.temps_choisi)

        # Masquer le label simple et afficher le frame de conjugaison coloré
        self.question_label.pack_forget()
        self.conjugaison_frame.pack(pady=20)

        # Configurer les textes avec couleurs
        if self.verbe_choisi in verbes_irreguliers:
            self.irregulier_label.config(text="irrégulier")
        else:
            self.irregulier_label.config(text="")

        self.verbe_label.config(text=f"{self.verbe_choisi}")
        self.temps_label.config(text=f"{self.temps_choisi}")
        self.pronom_label.config(text=f"{pronom_choisi}")

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
        texte_normalise = unicodedata.normalize('NFD', texte)
        texte_sans_accents = ''.join(c for c in texte_normalise if unicodedata.category(c) != 'Mn')
        return texte_sans_accents.lower()

    def verifier_reponse(self):
        reponse_utilisateur = self.reponse_entry.get().strip()

        if not reponse_utilisateur:
            messagebox.showwarning("Attention", "Veuillez entrer une réponse!")
            return

        if self.mode_actuel == 'traduction':
            try:
                index_reponse = mots_russes.index(reponse_utilisateur)
                if index_reponse == self.index_aleatoire:
                    self.afficher_resultat("succes")
                else:
                    reponse_sans_accents = self.normaliser_texte(reponse_utilisateur)
                    bonne_reponse_sans_accents = self.normaliser_texte(self.bonne_reponse)

                    if reponse_sans_accents == bonne_reponse_sans_accents:
                        self.afficher_resultat("presque")
                    else:
                        self.afficher_resultat("echec")
            except ValueError:
                reponse_sans_accents = self.normaliser_texte(reponse_utilisateur)
                bonne_reponse_sans_accents = self.normaliser_texte(self.bonne_reponse)

                if reponse_sans_accents == bonne_reponse_sans_accents:
                    self.afficher_resultat("presque")
                else:
                    self.afficher_resultat("echec")
        else:
            if reponse_utilisateur.lower() == self.bonne_reponse.lower():
                self.afficher_resultat("succes")
            else:
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

        # Vérifier auto-save
        self.check_auto_save()

        # Passer automatiquement à la question suivante après 750ms
        self.root.after(750, self.nouvelle_question)

    def afficher_resultat(self, resultat):
        """Affiche le résultat en changeant la couleur de fond de toute la fenêtre"""
        self.total_questions += 1
        if resultat == "succes" or resultat == "presque":
            self.correct_answers += 1
        
        self.update_percentage_display()

        if resultat == "succes":
            couleur_fond = '#15853f'
            self.bonne_reponse_label.config(text="", foreground="#000000")
        elif resultat == "presque":
            couleur_fond = '#d98b09'
            self.bonne_reponse_label.config(text=f"Bonne réponse : {self.bonne_reponse}", foreground="#000000")
        elif resultat == "echec":
            couleur_fond = '#a32c2c'
            self.bonne_reponse_label.config(text=f"Bonne réponse : {self.bonne_reponse}", foreground="#000000")

        self.root.configure(bg=couleur_fond)

        style = ttk.Style()
        style.configure('TFrame', background=couleur_fond)
        style.configure('TLabel', background=couleur_fond)

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

    def update_goal_display(self):
        """Met à jour l'affichage de l'objectif de la catégorie"""
        if dictionnaire == 2:
            self.goal_label.config(text="")
            return
        
        category = get_current_category()
        goal = GOALS[category]
        
        self.goal_label.config(text=f"Objectif : {goal}%")

    def remettre_fond_neutre(self):
        """Remet le fond neutre de toute la fenêtre"""
        self.root.configure(bg='#454545')
        style = ttk.Style()
        style.configure('TFrame', background='#454545')
        style.configure('TLabel', background='#454545')
        self.nouvelle_question()

    def changer_dictionnaire(self):
        """Change le type de dictionnaire utilisé"""
        global dictionnaire, mots_francais, mots_russes

        dictionnaire = 1 if dictionnaire == 2 else 2

        mots_francais.clear()
        mots_russes.clear()

        if dictionnaire == 1:
            fichier_dict = os.path.join(BASE_DIR, 'Dictionnaires', 'dictionnaire_russian.txt')
        else:
            fichier_dict = os.path.join(BASE_DIR, 'Dictionnaires', 'dictionnaire_russian_sample.txt')

        try:
            with open(fichier_dict, 'r', encoding='utf-8') as fichier:
                for ligne in fichier:
                    ligne = ligne.strip()
                    if '%' in ligne:
                        francais, russe = ligne.split(' % ')
                        mots_francais.append(francais)
                        mots_russes.append(russe)
        except FileNotFoundError:
            messagebox.showerror("Erreur", f"Le fichier dictionnaire est introuvable :\n{fichier_dict}")
            mots_francais.append("Erreur")
            mots_russes.append("Fichier introuvable")

        if not mots_francais:
            mots_francais.append("Vide")
            mots_russes.append("Dictionnaire vide")

        self.mettre_a_jour_statuts()
        self.update_goal_display()
        if hasattr(self, 'mode_actuel') and self.mode_actuel == 'traduction':
            self.nouvelle_question()

    def changer_training_type(self):
        """Change le type d'entraînement"""
        global training_type

        training_type = (training_type + 1) % 3
        
        new_category = get_current_category()
        if new_category != self.current_category:
            self.reset_progress()
            self.current_category = new_category

        self.mettre_a_jour_statuts()
        self.update_goal_display()
        self.nouvelle_question()

    def changer_irregular_mode(self):
        """Change le mode verbes irréguliers"""
        global verb_mode

        verb_mode = (verb_mode + 1) % 3
        
        new_category = get_current_category()
        if new_category != self.current_category:
            self.reset_progress()
            self.current_category = new_category

        self.mettre_a_jour_statuts()
        self.update_goal_display()
        if hasattr(self, 'mode_actuel') and self.mode_actuel == 'conjugaison':
            self.nouvelle_question()

    def mettre_a_jour_statuts(self):
        """Met à jour l'affichage des statuts sous chaque bouton"""
        if dictionnaire == 1:
            self.dict_status.config(text="Complet", foreground="#2563eb")
        else:
            self.dict_status.config(text="Échantillon", foreground="#16a34a")

        if training_type == 0:
            self.training_status.config(text="Mixte\n(25% conj / 75% trad)", foreground="#7c3aed")
        elif training_type == 1:
            self.training_status.config(text="Traduction\nuniquement", foreground="#dc2626")
        else:
            self.training_status.config(text="Conjugaison\nuniquement", foreground="#ea580c")

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
        sys.exit(0)
    
    def reset_progress(self):
        """Réinitialise la progression (quand on change de catégorie)"""
        self.total_questions = 0
        self.correct_answers = 0
        self.has_saved = False
        self.update_percentage_display()
    
    def check_auto_save(self):
        """Vérifie si l'auto-sauvegarde doit être déclenchée - quitte automatiquement"""
        if self.total_questions >= AUTO_SAVE_THRESHOLD and not self.has_saved:
            self.save_progress()
            self.root.quit()
            self.root.destroy()
            sys.exit(0)
    
    def save_progress(self):
        """Sauvegarde la progression dans un fichier CSV et génère le graphique"""
        if self.has_saved or self.total_questions == 0:
            return
        
        self.has_saved = True
        
        try:
            category = get_current_category()
            csv_file = os.path.join(DATA_DIR, f'{CATEGORY_FILES[category]}.csv')
            
            percentage = (self.correct_answers / self.total_questions) * 100
            today = datetime.now().strftime('%Y-%m-%d')
            
            file_exists = os.path.exists(csv_file)
            
            with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['date', 'attempts', 'percentage'])
                writer.writerow([today, self.total_questions, f'{percentage:.1f}'])
            
            try:
                generate_2d_graph(category)
            except Exception:
                pass
        except Exception:
            pass
        
        self.root.quit()
        self.root.destroy()
        sys.exit(0)


# Remplacer la boucle while par l'interface graphique
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

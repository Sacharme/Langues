import random
import tkinter as tk
from tkinter import ttk
import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.dates as mdates
import numpy as np

# ============== CONFIGURATION ==============
AUTO_SAVE_THRESHOLD = 200  # Nombre d'essais avant auto-sauvegarde
GOAL_PERCENTAGE = 95       # Objectif de réussite (%)

# Chemins des fichiers
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'Data', 'Greek Alphabet')
GRAPHS_DIR = os.path.join(BASE_DIR, 'Graphs', 'Greek Alphabet')
CSV_FILE = os.path.join(DATA_DIR, 'alphabet.csv')
GRAPH_FILE = os.path.join(GRAPHS_DIR, 'alphabet_progress.png')

# Créer les dossiers s'ils n'existent pas
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(GRAPHS_DIR, exist_ok=True)

# Dictionnaire de l'alphabet grec
# Clé : Lettre (Majuscule + Minuscule)
# Valeur : Liste des translittérations acceptées
alphabet = {
    'Α α': ['a', 'alpha'],
    'Β β': ['b', 'v', 'beta'],
    'Γ γ': ['g', 'gamma'],
    'Δ δ': ['d', 'delta'],
    'Ε ε': ['e', 'epsilon'],
    'Ζ ζ': ['z', 'zeta'],
    'Η η': ['i', 'e', 'eta'],
    'Θ θ': ['th', 'theta'],
    'Ι ι': ['i', 'iota'],
    'Κ κ': ['k', 'kappa'],
    'Λ λ': ['l', 'lambda'],
    'Μ μ': ['m', 'mu'],
    'Ν ν': ['n', 'nu'],
    'Ξ ξ': ['x', 'ks', 'xi'],
    'Ο ο': ['o', 'omicron'],
    'Π π': ['p', 'pi'],
    'Ρ ρ': ['r', 'rho'],
    'Σ σ': ['s', 'sigma'],
    'Τ τ': ['t', 'tau'],
    'Υ υ': ['y', 'u', 'upsilon'],
    'Φ φ': ['f', 'ph', 'phi'],
    'Χ χ': ['ch', 'kh', 'x', 'chi'],
    'Ψ ψ': ['ps', 'psi'],
    'Ω ω': ['o', 'omega'],
}


def generate_3d_graph():
    """Génère un graphique 3D de la progression"""
    if not os.path.exists(CSV_FILE):
        return
    
    dates = []
    attempts = []
    percentages = []
    
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                dates.append(datetime.strptime(row['date'], '%Y-%m-%d'))
                attempts.append(int(row['attempts']))
                percentages.append(float(row['percentage']))
            except (ValueError, KeyError):
                continue
    
    if not dates:
        return
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Convertir les dates en nombres pour le graphique
    date_nums = mdates.date2num(dates)
    
    # Points de progression
    ax.scatter(attempts, date_nums, percentages, c='blue', s=100, marker='o', label='Scores')
    
    # Ligne reliant les points
    if len(dates) > 1:
        ax.plot(attempts, date_nums, percentages, c='blue', alpha=0.5)
    
    # Fixer les limites de l'axe Z (0 à 100%)
    ax.set_zlim(0, 100)
    
    # Ligne de but (plan horizontal à GOAL_PERCENTAGE)
    if attempts and dates:
        x_min, x_max = min(attempts), max(attempts)
        x_margin = max(1, (x_max - x_min) * 0.1)
        y_min, y_max = min(date_nums), max(date_nums)
        y_margin = max(0.5, (y_max - y_min) * 0.1)
        
        x_range = [x_min - x_margin, x_max + x_margin]
        y_range = [y_min - y_margin, y_max + y_margin]
        X, Y = np.meshgrid(x_range, y_range)
        Z = np.full_like(X, GOAL_PERCENTAGE, dtype=float)
        ax.plot_surface(X, Y, Z, alpha=0.4, color='red', edgecolor='darkred', linewidth=2)
    
    ax.set_xlabel('Number of attempts')
    ax.set_ylabel('Date')
    ax.set_zlabel('Success rate (%)')
    ax.set_title(f'Greek Alphabet Progress (Goal: {GOAL_PERCENTAGE}%)')
    
    # Formater l'axe Y pour afficher les dates
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: mdates.num2date(x).strftime('%d/%m')))
    
    plt.tight_layout()
    plt.savefig(GRAPH_FILE, dpi=150, bbox_inches='tight')
    plt.close()


class AlphabetApp:
    def __init__(self, root):
        self.root = root
        self.has_saved = False

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#454545')
        style.configure('TLabel', background='#454545', foreground='white')
        style.configure('TButton', font=('Arial', 20))

        self.root.configure(bg='#454545')
        self.root.title("Alphabet Grec")
        self.root.attributes('-fullscreen', True)

        self.lettre_actuelle = None
        self.reponses_possibles = None

        self.total_questions = 0
        self.correct_answers = 0

        self.setup_ui()
        self.nouvelle_question()

    def setup_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)

        self.feedback_label = ttk.Label(main_frame, text="", font=("Arial", 30, "bold"), justify="center")
        self.feedback_label.grid(row=0, column=0, pady=(50, 20))

        self.question_label = ttk.Label(main_frame, text="", font=("Arial", 150, "bold"), justify="center")
        self.question_label.grid(row=1, column=0, pady=50)

        self.reponse_entry = ttk.Entry(main_frame, font=("Arial", 40), justify="center", width=10)
        self.reponse_entry.grid(row=3, column=0, pady=20)
        self.reponse_entry.bind('<Return>', lambda e: self.verifier_reponse())
        self.reponse_entry.focus()

        self.valider_btn = ttk.Button(main_frame, text="Valider", command=self.verifier_reponse)
        self.valider_btn.grid(row=4, column=0, pady=30, ipadx=20, ipady=10)

        controles_frame = ttk.Frame(main_frame)
        controles_frame.grid(row=5, column=0, pady=20)
        
        style = ttk.Style()
        style.configure("Save.TButton", font=("Arial", 20, "bold"))
        self.save_btn = ttk.Button(controles_frame, text="Enregistrer", 
                                   command=self.save_progress, style="Save.TButton")
        self.save_btn.grid(row=0, column=0, padx=20)
        
        quit_btn = ttk.Button(controles_frame, text="Quitter", command=self.quitter)
        quit_btn.grid(row=0, column=1, padx=20)

        self.percentage_label = ttk.Label(main_frame, text="0% (0/0)",
                                          font=("Arial", 24, "bold"),
                                          foreground="#00bcd4",
                                          justify="center")
        self.percentage_label.grid(row=6, column=0, pady=(10, 5))

        self.goal_label = ttk.Label(main_frame, text=f"Objectif : {GOAL_PERCENTAGE}%",
                                    font=("Arial", 18),
                                    foreground="#ff6b6b",
                                    justify="center")
        self.goal_label.grid(row=7, column=0, pady=(0, 20))

    def nouvelle_question(self):
        self.lettre_actuelle, self.reponses_possibles = random.choice(list(alphabet.items()))

        self.question_label.config(text=self.lettre_actuelle)
        self.reponse_entry.config(state="normal")
        self.reponse_entry.delete(0, tk.END)
        self.valider_btn.config(state="normal")
        self.feedback_label.config(text="")

        self.root.configure(bg='#454545')
        style = ttk.Style()
        style.configure('TFrame', background='#454545')
        style.configure('TLabel', background='#454545')
        self.reponse_entry.focus()

    def verifier_reponse(self):
        reponse = self.reponse_entry.get().strip().lower()

        if not reponse and '' not in self.reponses_possibles:
             return

        correct = reponse in self.reponses_possibles

        if correct:
            self.afficher_resultat(True)
        else:
            self.afficher_resultat(False)

        self.reponse_entry.config(state="disabled")
        self.valider_btn.config(state="disabled")

        self.check_auto_save()
        self.root.after(1000, self.nouvelle_question)

    def afficher_resultat(self, succes):
        self.total_questions += 1
        if succes:
            self.correct_answers += 1
        
        self.update_percentage_display()

        reponse_str = " / ".join([r for r in self.reponses_possibles if r])
        if not reponse_str: reponse_str = "(aucune)"

        if succes:
            couleur = '#15853f'
            self.feedback_label.config(text=f"{reponse_str}", foreground="white")
        else:
            couleur = '#a32c2c'
            self.feedback_label.config(text=f"{reponse_str}", foreground="white")

        self.root.configure(bg=couleur)
        style = ttk.Style()
        style.configure('TFrame', background=couleur)
        style.configure('TLabel', background=couleur)

    def update_percentage_display(self):
        if self.total_questions > 0:
            percentage = (self.correct_answers / self.total_questions) * 100
            self.percentage_label.config(
                text=f"{percentage:.1f}% ({self.correct_answers}/{self.total_questions})"
            )
        else:
            self.percentage_label.config(text="0% (0/0)")

    def check_auto_save(self):
        if self.total_questions >= AUTO_SAVE_THRESHOLD and not self.has_saved:
            self.save_progress()

    def save_progress(self):
        if self.has_saved or self.total_questions == 0:
            return
        
        self.has_saved = True
        
        percentage = (self.correct_answers / self.total_questions) * 100
        today = datetime.now().strftime('%Y-%m-%d')
        
        file_exists = os.path.exists(CSV_FILE)
        
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['date', 'attempts', 'percentage'])
            writer.writerow([today, self.total_questions, f'{percentage:.1f}'])
        
        generate_3d_graph()
        
        self.root.quit()
        self.root.destroy()

    def quitter(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlphabetApp(root)
    root.mainloop()

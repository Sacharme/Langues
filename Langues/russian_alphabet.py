import random
import tkinter as tk
from tkinter import ttk

# Dictionnaire de l'alphabet russe
# Clé : Lettre (Majuscule + Minuscule)
# Valeur : Liste des translittérations acceptées
alphabet = {
    'А а': ['a'],
    'Б б': ['b'],
    'В в': ['v'],
    'Г г': ['g', 'gue'],
    'Д д': ['d'],
    'Е е': ['ye', 'ie', 'je', 'e'],
    'Ё ё': ['yo', 'io', 'jo'],
    'Ж ж': ['zh', 'j'],
    'З з': ['z'],
    'И и': ['i'],
    'Й й': ['y', 'i', 'j', 'ï'],
    'К к': ['k'],
    'Л л': ['l'],
    'М м': ['m'],
    'Н н': ['n'],
    'О о': ['o'],
    'П п': ['p'],
    'Р р': ['r'],
    'С с': ['s'],
    'Т т': ['t'],
    'У у': ['u', 'ou'],
    'Ф ф': ['f'],
    'Х х': ['kh', 'h'],
    'Ц ц': ['ts'],
    'Ч ч': ['ch', 'tch'],
    'Ш ш': ['sh', 'ch'],
    'Щ щ': ['shch', 'sch', 'chtch'],
    'Ъ ъ': ['signe dur', 'hard sign', '"', ''],
    'Ы ы': ['y'],
    'Ь ь': ['signe mou', 'soft sign', "'", ''],
    'Э э': ['e', 'eh'],
    'Ю ю': ['yu', 'iu', 'ju', 'you'],
    'Я я': ['ya', 'ia', 'ja']
}

class AlphabetApp:
    def __init__(self, root):
        self.root = root

        # Configuration du style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#454545')
        style.configure('TLabel', background='#454545', foreground='white')
        style.configure('TButton', font=('Arial', 20))

        self.root.configure(bg='#454545')
        self.root.title("Alphabet Russe")
        self.root.attributes('-fullscreen', True)

        self.lettre_actuelle = None
        self.reponses_possibles = None

        self.setup_ui()
        self.nouvelle_question()

    def setup_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)

        # Label de résultat / bonne réponse
        self.feedback_label = ttk.Label(main_frame, text="", font=("Arial", 30, "bold"), justify="center")
        self.feedback_label.grid(row=0, column=0, pady=(50, 20))

        # Label de la lettre à deviner
        self.question_label = ttk.Label(main_frame, text="", font=("Arial", 150, "bold"), justify="center")
        self.question_label.grid(row=1, column=0, pady=50)

        # Instruction
        instruction_label = ttk.Label(main_frame, text="Entrez la prononciation (translittération)", font=("Arial", 20))
        instruction_label.grid(row=2, column=0, pady=(0, 20))

        # Champ de saisie
        self.reponse_entry = ttk.Entry(main_frame, font=("Arial", 40), justify="center", width=10)
        self.reponse_entry.grid(row=3, column=0, pady=20)
        self.reponse_entry.bind('<Return>', lambda e: self.verifier_reponse())
        self.reponse_entry.focus()

        # Bouton Valider
        self.valider_btn = ttk.Button(main_frame, text="Valider", command=self.verifier_reponse)
        self.valider_btn.grid(row=4, column=0, pady=30, ipadx=20, ipady=10)

        # Bouton Quitter
        quit_btn = ttk.Button(main_frame, text="Quitter", command=self.quitter)
        quit_btn.grid(row=5, column=0, pady=20)

    def nouvelle_question(self):
        self.lettre_actuelle, self.reponses_possibles = random.choice(list(alphabet.items()))

        self.question_label.config(text=self.lettre_actuelle)
        self.reponse_entry.config(state="normal")
        self.reponse_entry.delete(0, tk.END)
        self.valider_btn.config(state="normal")
        self.feedback_label.config(text="")

        # Reset background
        self.root.configure(bg='#454545')
        style = ttk.Style()
        style.configure('TFrame', background='#454545')
        style.configure('TLabel', background='#454545')
        self.reponse_entry.focus()

    def verifier_reponse(self):
        reponse = self.reponse_entry.get().strip().lower()

        # Si l'utilisateur n'entre rien et que la réponse vide n'est pas autorisée
        if not reponse and '' not in self.reponses_possibles:
             return

        correct = reponse in self.reponses_possibles

        if correct:
            self.afficher_resultat(True)
        else:
            self.afficher_resultat(False)

        self.reponse_entry.config(state="disabled")
        self.valider_btn.config(state="disabled")

        self.root.after(2000, self.nouvelle_question)

    def afficher_resultat(self, succes):
        if succes:
            couleur = '#15853f' # Vert
            self.feedback_label.config(text="Correct !", foreground="white")
        else:
            couleur = '#a32c2c' # Rouge
            reponse_str = " ou ".join([r for r in self.reponses_possibles if r])
            if not reponse_str: reponse_str = "(aucune)"
            self.feedback_label.config(text=f"{reponse_str}", foreground="white")

        self.root.configure(bg=couleur)
        style = ttk.Style()
        style.configure('TFrame', background=couleur)
        style.configure('TLabel', background=couleur)

    def quitter(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlphabetApp(root)
    root.mainloop()

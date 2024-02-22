import random
import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from datetime import date

class Keybox(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("générateur de code Boîte à clé")
        # Création d'une nouvelle base de données
        self.db_path = "keybox_database.db"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS keybox (id INTEGER PRIMARY KEY, code TEXT, date TEXT)")
        self.conn.commit()

        self.geometry("600x480")
        self.generated_code = None  # Ajoutez une variable membre pour stocker le code généré

        # Ajout d'un conteneur pour les widgets avec un arrière-plan
        self.container = tk.Frame(self, bg="#52C181")
        self.container.pack(fill="both", expand=True)

        self.create_widgets()

        # Ajoutez une Treeview pour afficher les données
        self.tree = ttk.Treeview(self.container, columns=('Code', 'Date'), show='headings')
        self.tree.heading('Code', text='Code')
        self.tree.heading('Date', text='Date')

        self.tree.pack(pady=10)

        # Afficher les données existantes dans la base de données
        self.afficher_codes_existant()

    def generer_code(self):
        chiffres_disponibles = list(range(10))
        random.shuffle(chiffres_disponibles)

        # Vérifier si les chiffres se suivent et régénérer si nécessaire
        while any(abs(a - b) == 1 for a, b in zip(chiffres_disponibles, chiffres_disponibles[1:])):
            random.shuffle(chiffres_disponibles)

        code = chiffres_disponibles[:4]

        return code

    def create_widgets(self):
        # Champ de date du jour
        today_date = date.today().strftime("%d/%m/%Y")
        tk.Label(self.container, text=f"Date du jour: {today_date}", bg="#52C181", font=('Times New Roman', 14)).pack(pady=5)

        # Entry pour afficher le code généré
        self.generated_code_entry = tk.Entry(self.container)
        self.generated_code_entry.pack(pady=10)

        # Bouton Générer Code
        tk.Button(self.container, text="Générer Code", command=self.generer_et_afficher_code).pack(pady=10)

        # Bouton Enregistrer
        tk.Button(self.container, text="Enregistrer", command=self.enregistrer_code, bg="red", fg="white").pack(pady=10)

    def generer_et_afficher_code(self):
        self.generated_code = self.generer_code()  # Stocke le code généré dans la variable membre
        self.generated_code_entry.delete(0, tk.END)  # Efface le contenu précédent de l'entry
        self.generated_code_entry.insert(0, ''.join(map(str, self.generated_code)))  # Affiche le code dans l'entry

    def enregistrer_code(self):
        # Utilisez self.generated_code pour récupérer le code généré
        code = ''.join(map(str, self.generated_code)) if self.generated_code else ''.join(map(str, self.generer_code()))
        date_today = date.today().strftime("%Y-%m-%d")

        # Enregistrement dans la base de données
        self.cursor.execute("INSERT INTO keybox (code, date) VALUES (?, ?)", (code, date_today))
        self.conn.commit()

        # Mise à jour du Treeview
        self.afficher_codes_existant()

        messagebox.showinfo("Enregistrement réussi", "Code enregistré avec succès!")

    def afficher_codes_existant(self):
        # Effacer les données actuelles dans le Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Récupérer les données depuis la base de données
        self.cursor.execute("SELECT * FROM keybox")
        rows = self.cursor.fetchall()

        # Afficher les données dans le Treeview
        for row in rows:
            self.tree.insert("", "end", values=(row[1], row[2]))

if __name__ == "__main__":
    app = Keybox()
    app.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

class HorlogeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Horloge avec Alarme")

        self.heure_actuelle = (0, 0, 0)
        self.alarme = (12, 0, 0, "AM")
        self.alarme_declenchee = False

        self.label_heure = ttk.Label(root, text="")
        self.label_heure.pack(padx=10, pady=10)

        self.format_24h_var = tk.BooleanVar()
        self.format_24h_var.set(True)
        self.bouton_format = ttk.Checkbutton(root, text="Format 24h", variable=self.format_24h_var, command=self.actualiser_format)
        self.bouton_format.pack()

        self.bouton_alarme = ttk.Button(root, text="Régler l'alarme", command=self.regler_alarme)
        self.bouton_alarme.pack(pady=10)

        self.mise_a_jour_heure()

    def mise_a_jour_heure(self):
        if self.format_24h_var.get():
            heure_transformee = time.strftime("%H:%M:%S", time.localtime())
        else:
            heure_transformee = time.strftime("%I:%M:%S %p", time.localtime())
        self.label_heure.config(text=f"Heure actuelle : {heure_transformee}")
        self.verifier_alarme()
        if not self.alarme_declenchee:
            self.root.after(1000, self.mise_a_jour_heure)

    def actualiser_format(self):
        self.mise_a_jour_heure()

    def regler_alarme(self):
        reglage_alarme = tk.Toplevel(self.root)
        reglage_alarme.title("Régler l'alarme")

        heures_var = tk.StringVar()
        minutes_var = tk.StringVar()
        secondes_var = tk.StringVar()
        am_pm_var = tk.StringVar()

        heures_var.set(str(self.alarme[0]))
        minutes_var.set(str(self.alarme[1]))
        secondes_var.set(str(self.alarme[2]))
        am_pm_var.set(self.alarme[3])

        ttk.Label(reglage_alarme, text="Heures:").grid(row=0, column=0)
        ttk.Label(reglage_alarme, text="Minutes:").grid(row=1, column=0)
        ttk.Label(reglage_alarme, text="Secondes:").grid(row=2, column=0)
        ttk.Label(reglage_alarme, text="AM/PM:").grid(row=3, column=0)

        entree_heures = ttk.Entry(reglage_alarme, textvariable=heures_var)
        entree_minutes = ttk.Entry(reglage_alarme, textvariable=minutes_var)
        entree_secondes = ttk.Entry(reglage_alarme, textvariable=secondes_var)

        choix_am_pm = ttk.Combobox(reglage_alarme, textvariable=am_pm_var, values=["AM", "PM"])
        choix_am_pm.grid(row=3, column=1, pady=5)

        entree_heures.grid(row=0, column=1)
        entree_minutes.grid(row=1, column=1)
        entree_secondes.grid(row=2, column=1)

        bouton_valider = ttk.Button(reglage_alarme, text="Valider", command=lambda: self.valider_alarme(heures_var.get(), minutes_var.get(), secondes_var.get(), am_pm_var.get(), reglage_alarme))
        bouton_valider.grid(row=4, column=0, columnspan=2, pady=10)

        if self.format_24h_var.get():
            choix_am_pm.config(state="disabled")

    def valider_alarme(self, heures, minutes, secondes, am_pm, fenetre_parente):
        try:
            heures = int(heures)
            minutes = int(minutes)
            secondes = int(secondes)

            if self.format_24h_var.get() and not (0 <= heures < 24 and 0 <= minutes < 60 and 0 <= secondes < 60):
                raise ValueError("Format 24h invalide")
            elif not self.format_24h_var.get() and not (0 <= heures < 12 and 0 <= minutes < 60 and 0 <= secondes < 60 and am_pm in ["AM", "PM"]):
                raise ValueError("Format 12h invalide")

            self.alarme = (heures, minutes, secondes, am_pm)
            self.alarme_declenchee = False
            fenetre_parente.destroy()
        except ValueError as e:
            messagebox.showerror("Erreur", f"Veuillez entrer des valeurs valides. ({str(e)})")

    def verifier_alarme(self):
        heures, minutes, secondes = time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec
        am_pm = time.strftime("%p", time.localtime())
        if (heures, minutes, secondes, am_pm) == self.alarme and not self.alarme_declenchee:
            messagebox.showinfo("Alarme", "Alarme déclenchée !")
            self.alarme_declenchee = True

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x150")
    app = HorlogeApp(root)
    root.mainloop()

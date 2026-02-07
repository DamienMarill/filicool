"""
🍭 Fililico - Quick Mode UI
Interface minimaliste Tkinter pour le filigranage rapide via clic droit
"""

import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import WatermarkEngine


class QuickModeApp:
    """
    Interface minimaliste pour le filigranage rapide.
    Utilisée via le menu contextuel (clic droit).
    """

    # Dimensions de la fenêtre
    WIDTH = 420
    HEIGHT = 180

    # Couleurs kawaii
    COLORS = {
        "bg": "#fdf2f8",  # Cotton Cloud
        "primary": "#f472b6",  # Bubblegum Pink
        "secondary": "#a78bfa",  # Magic Berry
        "text": "#4c1d95",  # Deep Grape
        "success": "#34d399",  # Minty Fresh
        "error": "#f472b6",  # Bubblegum Pink
    }

    def __init__(self, file_path: Optional[str] = None):
        """
        Initialise l'interface Quick Mode.

        Args:
            file_path: Chemin du fichier à traiter (passé par le menu contextuel)
        """
        self.file_path = Path(file_path) if file_path else None
        self.engine = WatermarkEngine()
        self.result = None

        # Création de la fenêtre
        self.root = tk.Tk()
        self._setup_window()
        self._create_widgets()
        self._bind_events()

    def _setup_window(self):
        """Configure la fenêtre principale."""
        self.root.title("🍭 Fililico - Quick Mode")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLORS["bg"])

        # Centrer la fenêtre
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.WIDTH) // 2
        y = (self.root.winfo_screenheight() - self.HEIGHT) // 2
        self.root.geometry(f"+{x}+{y}")

        # Garder la fenêtre au premier plan
        self.root.attributes("-topmost", True)

        # Icône (si disponible)
        try:
            icon_path = Path(__file__).parent.parent.parent / "assets" / "images" / "logo.png"
            if icon_path.exists():
                icon = tk.PhotoImage(file=str(icon_path))
                self.root.iconphoto(True, icon)
        except Exception:
            pass

    def _create_widgets(self):
        """Crée les widgets de l'interface."""
        # Frame principal avec padding
        main_frame = tk.Frame(self.root, bg=self.COLORS["bg"], padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Titre
        title_label = tk.Label(
            main_frame,
            text="🍭 Filigraner Illico!",
            font=("Segoe UI", 14, "bold"),
            fg=self.COLORS["primary"],
            bg=self.COLORS["bg"],
        )
        title_label.pack(pady=(0, 10))

        # Nom du fichier
        if self.file_path:
            file_label = tk.Label(
                main_frame,
                text=f"📄 {self.file_path.name}",
                font=("Segoe UI", 9),
                fg=self.COLORS["text"],
                bg=self.COLORS["bg"],
            )
            file_label.pack(pady=(0, 10))

        # Frame pour le champ texte
        input_frame = tk.Frame(main_frame, bg=self.COLORS["bg"])
        input_frame.pack(fill=tk.X, pady=5)

        # Label
        text_label = tk.Label(
            input_frame,
            text="Texte du filigrane :",
            font=("Segoe UI", 10),
            fg=self.COLORS["text"],
            bg=self.COLORS["bg"],
        )
        text_label.pack(anchor=tk.W)

        # Champ de saisie
        self.text_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 11),
            fg=self.COLORS["text"],
            bg="white",
            relief=tk.FLAT,
            highlightthickness=2,
            highlightbackground=self.COLORS["secondary"],
            highlightcolor=self.COLORS["primary"],
        )
        self.text_entry.insert(0, "CONFIDENTIEL")
        self.text_entry.pack(fill=tk.X, pady=5, ipady=5)
        self.text_entry.focus_set()
        self.text_entry.select_range(0, tk.END)

        # Frame pour les boutons
        button_frame = tk.Frame(main_frame, bg=self.COLORS["bg"])
        button_frame.pack(fill=tk.X, pady=(15, 0))

        # Bouton Annuler
        self.cancel_btn = tk.Button(
            button_frame,
            text="❌ Annuler",
            font=("Segoe UI", 10),
            fg=self.COLORS["text"],
            bg="white",
            activebackground=self.COLORS["bg"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            command=self._cancel,
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Bouton Valider
        self.submit_btn = tk.Button(
            button_frame,
            text="✨ Filigraner!",
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg=self.COLORS["primary"],
            activebackground=self.COLORS["secondary"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            command=self._process,
        )
        self.submit_btn.pack(side=tk.RIGHT)

    def _bind_events(self):
        """Lie les événements clavier."""
        self.root.bind("<Return>", lambda e: self._process())
        self.root.bind("<Escape>", lambda e: self._cancel())

    def _process(self):
        """Traite le fichier avec le filigrane."""
        text = self.text_entry.get().strip()

        if not text:
            messagebox.showwarning(
                "🍭 Oops!",
                "Le texte du filigrane ne peut pas être vide !",
            )
            return

        if not self.file_path:
            messagebox.showerror(
                "🍭 Erreur",
                "Aucun fichier spécifié !",
            )
            return

        if not self.file_path.exists():
            messagebox.showerror(
                "🍭 Erreur",
                f"Fichier introuvable :\n{self.file_path}",
            )
            return

        # Désactiver les boutons pendant le traitement
        self.submit_btn.config(state=tk.DISABLED, text="⏳ Traitement...")
        self.cancel_btn.config(state=tk.DISABLED)
        self.root.update()

        try:
            # Mettre à jour le moteur et traiter
            self.engine.text = text
            result = self.engine.process(self.file_path)

            if result.success:
                self.result = result
                messagebox.showinfo(
                    "🍭 Succès!",
                    f"Filigrane ajouté avec succès !\n\n"
                    f"📄 {result.output_path.name}\n"
                    f"📁 {result.output_path.parent}",
                )
                self.root.quit()
            else:
                messagebox.showerror(
                    "🍭 Erreur",
                    f"Impossible de traiter le fichier :\n{result.error}",
                )
                self.submit_btn.config(state=tk.NORMAL, text="✨ Filigraner!")
                self.cancel_btn.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror(
                "🍭 Erreur",
                f"Une erreur est survenue :\n{str(e)}",
            )
            self.submit_btn.config(state=tk.NORMAL, text="✨ Filigraner!")
            self.cancel_btn.config(state=tk.NORMAL)

    def _cancel(self):
        """Annule et ferme la fenêtre."""
        self.root.quit()

    def run(self):
        """Lance l'application."""
        self.root.mainloop()
        self.root.destroy()
        return self.result


def main():
    """Point d'entrée pour le mode Quick."""
    # Récupérer le fichier passé en argument
    file_path = sys.argv[1] if len(sys.argv) > 1 else None

    if not file_path:
        # Mode démo sans fichier
        print("🍭 Fililico Quick Mode")
        print("Usage: python quick_mode.py <fichier>")
        print("\nLancement en mode démo...")

    app = QuickModeApp(file_path)
    result = app.run()

    if result and result.success:
        print(f"✅ Fichier créé: {result.output_path}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

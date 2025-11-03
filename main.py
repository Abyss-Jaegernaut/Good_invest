import sys
from view.console_view import (
    afficher_menu_principal, 
    choisir_dataset, 
    afficher_resultat,
    afficher_message
)
from controller.brute_force_controller import run_brute_force
from controller.optimized_controller import run_optimized

def main():
    """Point d'entrée principal de l'application."""
    while True:
        choix = afficher_menu_principal()
        if choix == "1":
            dataset_path = choisir_dataset()
            if dataset_path:
                try:
                    resultat = run_brute_force(dataset_path)
                    afficher_resultat(resultat)
                except Exception as e:
                    afficher_message(f"Une erreur critique est survenue (Force Brute): {e}", "erreur")
        
        elif choix == "2":
            # --- Optimisée ---
            dataset_path = choisir_dataset()
            if dataset_path:
                try:
                    resultat = run_optimized(dataset_path)
                    afficher_resultat(resultat)
                except Exception as e:
                    afficher_message(f"Une erreur critique est survenue (Optimisée): {e}", "erreur")

        elif choix == "3":
            # --- Quitter ---
            print("\nAu revoir ! \n")
            sys.exit()

        else:
            afficher_message("Choix invalide, veuillez réessayer.", "erreur")

if __name__ == "__main__":
    main()
import os
try:
    from colorama import Fore, Style, init
    # Initialiser colorama (pour Windows)
    init(autoreset=True)
except ImportError:
    print("Bibliothèque 'colorama' non trouvée. L'affichage sera sans couleur.")
    # Créer des objets factices pour que le code ne plante pas
    class DummyStyle:
        def __getattr__(self, name):
            return ""
    Fore = DummyStyle()
    Style = DummyStyle()


def afficher_menu_principal():
    """Affiche le menu principal et retourne le choix de l'utilisateur."""
    print(Fore.CYAN + "\n" + "="*50)
    print(Fore.YELLOW + "  ANALYSE DÉCISIONNELLE D’INVESTISSEMENT")
    print(Fore.CYAN + "="*50)
    print(f"  Budget maximal : {Fore.GREEN}500 000 F CFA" + Style.RESET_ALL)
    print(Fore.CYAN + "-"*50)
    print("  [1] Exécuter la solution Force Brute")
    print("  [2] Exécuter la solution Optimisée (Dynamique)")
    print("  [3] Quitter")
    print(Fore.CYAN + "-"*50)
    return input(f"{Fore.WHITE}  Votre choix (1, 2 ou 3) : ")

def choisir_dataset(data_dir="data"):
    """Affiche les fichiers CSV disponibles et retourne le chemin du fichier choisi."""
    try:
        fichiers = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
        if not fichiers:
            afficher_message(f"Aucun fichier .csv trouvé dans le dossier '{data_dir}'.", "erreur")
            return None
    except FileNotFoundError:
        afficher_message(f"Le dossier '{data_dir}' n'existe pas.", "erreur")
        return None

    print(f"\n{Fore.YELLOW}📊 Jeux de données disponibles :{Style.RESET_ALL}")
    for i, f in enumerate(fichiers, 1):
        print(f"  [{i}] {f}")
    
    choix = input(f"\n{Fore.WHITE}Choisissez le dataset à utiliser (ex: 1) : ")

    try:
        index = int(choix) - 1
        if 0 <= index < len(fichiers):
            return os.path.join(data_dir, fichiers[index])
        else:
            afficher_message("Choix invalide. Utilisation du premier fichier par défaut.", "info")
            return os.path.join(data_dir, fichiers[0])
    except ValueError:
        afficher_message("Entrée invalide. Utilisation du premier fichier par défaut.", "info")
        return os.path.join(data_dir, fichiers[0])

def afficher_resultat(resultat):
    """Affiche un résumé formaté des résultats de l'exécution."""
    
    if not resultat:
        afficher_message("L'exécution a échoué ou a été interrompue. Aucun résultat.", "erreur")
        return

    methode = resultat.get('method', 'N/A')
    
    print(Fore.CYAN + "\n" + "-"*50)
    print(Fore.YELLOW + f"  Résultats : {methode}")
    print(Fore.CYAN + "-"*50 + Style.RESET_ALL)
    
    print(f"  Dataset          : {Fore.WHITE}{resultat.get('dataset', 'N/A')}")
    print(f"  Coût total        : {Fore.GREEN}{resultat.get('cout_total', 0)} F CFA")
    print(f"  Profit total      : {Fore.GREEN}{resultat.get('profit_total', 0):.2f} F CFA")
    print(f"  Durée d'exécution : {Fore.MAGENTA}{resultat.get('temps_execution', 0):.4f} s")
    print(f"  Mémoire (pic)     : {Fore.CYAN}{resultat.get('pic_memoire_Mo', 0):.2f} Mo")
    
    print(Fore.CYAN + "-"*50 + Style.RESET_ALL)
    
    actions = resultat.get("actions_selectionnees", [])
    if actions:
        print(f"{Fore.WHITE}  Actions sélectionnées ({len(actions)}) :")
        # Limiter l'affichage si la liste est trop longue (pour la console)
        if len(actions) > 15:
            for a in actions[:15]:
                print(Fore.GREEN + f"   - {a}")
            print(Fore.GREEN + f"   ... et {len(actions) - 15} autres (voir JSON).")
        else:
            for a in actions:
                print(Fore.GREEN + f"   - {a}")
    else:
        print(f"{Fore.WHITE}  Aucune action sélectionnée (budget insuffisant ou dataset vide).")
    
    print(Fore.CYAN + "-"*50)
    
    # Afficher le message de sauvegarde
    if resultat.get("saved_to"):
        print(f"{Fore.CYAN}💾 Résultats sauvegardés dans {resultat['saved_to']}{Style.RESET_ALL}")
    print() # Ligne vide pour aérer

def afficher_message(message, type="info"):
    """Affiche un message de statut (info, erreur, succès)."""
    if type == "erreur":
        print(f"{Fore.RED}ERREUR: {message}{Style.RESET_ALL}")
    elif type == "info":
        print(f"{Fore.CYAN}INFO: {message}{Style.RESET_ALL}")
    elif type == "succes":
        print(f"{Fore.GREEN}SUCCÈS: {message}{Style.RESET_ALL}")
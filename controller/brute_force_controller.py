import time
import tracemalloc
import itertools  # Outil pour générer les combinaisons
from model.dataset_loader import charger_dataset, BUDGET_MAX
from model.result_saver import sauvegarder_resultat

def run_brute_force(dataset_path):
    """
    Exécute l'algorithme de force brute.
    Teste toutes les combinaisons d'actions possibles.
    """
    print(f"\n> Lancement de la solution Force Brute sur {dataset_path}...")
    
    actions = charger_dataset(dataset_path)
    if actions is None:
        return None # Erreur de chargement gérée par le loader

    # Limite de sécurité : La force brute est en O(2^N).
    # Au-delà de ~20-22 actions, le temps devient déraisonnable.
    if len(actions) > 20:
        print(f"ERREUR: Le dataset est trop grand ({len(actions)} actions) pour la Force Brute.")
        print("Veuillez utiliser un dataset de 20 actions maximum ou utiliser la solution optimisée.")
        return None
        
    # --- Démarrage des métriques ---
    tracemalloc.start()
    start_time = time.perf_counter()
    # --------------------------------

    meilleur_profit = 0
    meilleur_cout = 0
    meilleure_combinaison = []

    n = len(actions)
    # Itérer sur toutes les tailles de combinaisons possibles (de 1 à N) 
    for k in range(1, n + 1):
        # Générer toutes les combinaisons de k actions
        for combo in itertools.combinations(actions, k):
            cout_total = sum(action.cost for action in combo)
            
            # Vérifier la contrainte de budget [cite: 20]
            if cout_total <= BUDGET_MAX:
                profit_total = sum(action.profit_amount for action in combo)
                
                # Maximiser le profit [cite: 8]
                if profit_total > meilleur_profit:
                    meilleur_profit = profit_total
                    meilleur_cout = cout_total
                    meilleure_combinaison = list(combo)

    # --- Arrêt des métriques ---
    end_time = time.perf_counter()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    # --------------------------

    # Formater les résultats
    resultat_final = {
        "dataset": dataset_path,
        "method": "Force Brute",
        "cout_total": meilleur_cout,
        "profit_total": meilleur_profit,
        "temps_execution": end_time - start_time,
        "memoire_utilisee_Mo": current_mem / 10**6, # Mémoire actuelle à la fin
        "pic_memoire_Mo": peak_mem / 10**6,       # Pic mémoire pendant l'exécution
        "actions_selectionnees": [action.id for action in meilleure_combinaison]
    }

    # Sauvegarder et retourner
    sauvegarder_resultat(resultat_final, methode="Force Brute")
    return resultat_final
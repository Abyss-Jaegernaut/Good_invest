import time
import tracemalloc
import sys
from model.dataset_loader import charger_dataset, BUDGET_MAX
from model.result_saver import sauvegarder_resultat

def run_optimized(dataset_path):
    """
    Algorithme optimisé utilisant la programmation dynamique.
    Optimisé pour la vitesse et l'utilisation mémoire.
    """
    print(f"\n> Lancement de la solution Optimisée (DP) sur {dataset_path}...")
    
    actions = charger_dataset(dataset_path)
    if not actions:
        return None

    tracemalloc.start()
    start_time = time.perf_counter()
    
    # Trier les actions par ratio profit/coût décroissant
    actions.sort(key=lambda x: x.profit_amount / x.cost, reverse=True)
    
    # Utilisation d'un ensemble pour un accès plus rapide aux indices
    dp = {0: (0.0, set())}  # budget: (profit, set_des_indices)
    
    for i, action in enumerate(actions):
        cost = action.cost
        profit = action.profit_amount
        
        # Créer une copie des entrées actuelles pour itération
        current_entries = list(dp.items())
        
        for budget, (current_profit, indices) in current_entries:
            new_budget = budget + cost
            
            if new_budget > BUDGET_MAX:
                continue
                
            new_profit = current_profit + profit
            
            # Vérifier si cette combinaison est meilleure
            if new_budget not in dp or new_profit > dp[new_budget][0]:
                if i not in indices:  # Vérifier que l'action n'est pas déjà incluse
                    new_indices = set(indices)  # Créer un nouveau set
                    new_indices.add(i)
                    dp[new_budget] = (new_profit, new_indices)
                    
                    # Nettoyer périodiquement les entrées non optimales
                    if len(dp) > 10000:  # Ajuster selon les besoins
                        # Garder uniquement les entrées avec les meilleurs profits
                        best_entries = {}
                        for b, (p, idx) in dp.items():
                            if p >= best_entries.get(b, (0,))[0]:
                                best_entries[b] = (p, idx)
                        dp = best_entries
    
    # Trouver la meilleure solution
    if not dp:
        meilleur_cout = 0
        meilleur_profit = 0
        meilleure_combinaison = []
    else:
        # Utiliser une boucle explicite pour plus de clarté et de contrôle
        best_budget = 0
        best_profit = 0
        best_indices = set()
        
        for budget, (profit, indices) in dp.items():
            if profit > best_profit or (profit == best_profit and budget < best_budget):
                best_budget = budget
                best_profit = profit
                best_indices = indices
        
        meilleur_cout = best_budget
        meilleur_profit = best_profit
        meilleure_combinaison = [actions[i] for i in best_indices]
    
    # Calcul des métriques de performance
    end_time = time.perf_counter()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Préparation des résultats
    resultat_final = {
        "dataset": dataset_path,
        "method": "Optimisée (DP)",
        "cout_total": meilleur_cout,
        "profit_total": meilleur_profit,
        "temps_execution": end_time - start_time,
        "memoire_utilisee_Mo": current_mem / 10**6,
        "pic_memoire_Mo": peak_mem / 10**6,
        "actions_selectionnees": [action.id for action in meilleure_combinaison]
    }

    sauvegarder_resultat(resultat_final, methode="Optimisée (DP)")
    return resultat_final
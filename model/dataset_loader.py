import csv
from .action import Action

# Budget maximal défini dans le cahier des charges [cite: 16, 20]
BUDGET_MAX = 500000 

def charger_dataset(filepath):
    """
    Charge les actions depuis un fichier CSV.
    Ignore les actions dont le coût est supérieur au budget total
    ou dont le coût/profit est nul ou négatif.
    """
    actions = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Utilise DictReader pour lire le CSV par nom de colonne [cite: 17]
            # Le délimiteur est ';' dans les fichiers CSV fournis
            reader = csv.DictReader(f, delimiter=';')
            
            for row in reader:
                try:
                    # Adapter aux noms de colonnes réels: 'price' au lieu de 'cost', 'name' au lieu de 'id'
                    cost = int(float(row["price"]))
                    profit_pct = float(row["profit_pct"])
                    
                    # Optimisation : Ignorer les actions inutiles ou invalides
                    if cost <= 0 or profit_pct <= 0:
                        continue
                    
                    # Optimisation : Ignorer les actions qui dépassent à elles seules le budget [cite: 20]
                    if cost <= BUDGET_MAX:
                        actions.append(Action(
                            id_action=row["name"],
                            cost=cost,
                            profit_pct=profit_pct
                        ))
                        
                except (ValueError, KeyError) as e:
                    print(f"Attention: Ligne ignorée (données invalides) : {row} - Erreur: {e}")
                    
    except FileNotFoundError:
        print(f"Erreur: Fichier non trouvé : {filepath}")
        return None
    except Exception as e:
        print(f"Erreur inattendue lors de la lecture de {filepath}: {e}")
        return None
        
    if not actions:
        print(f"Attention: Aucun dataset valide n'a été chargé depuis {filepath}.")
        return None

    print(f"INFO: {len(actions)} actions chargées et valides depuis {filepath}.")
    return actions
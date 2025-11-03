import json
import os

def sauvegarder_resultat(resultat, methode):
    """
    Sauvegarde le dictionnaire de résultats dans un fichier JSON.
    Le nom du fichier est généré dynamiquement.
    """
    output_dir = "results"
    
    # Assurer que le dossier 'results' existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Créer un nom de fichier dynamique
    try:
        # Extrait le nom du fichier (ex: "dataset1_test")
        dataset_name = os.path.basename(resultat["dataset"]).replace(".csv", "")
        # Nettoie le nom de la méthode (ex: "Force_Brute")
        methode_name = methode.lower().replace(" ", "_").replace("(", "").replace(")", "")
        
        filename = f"{output_dir}/{methode_name}_{dataset_name}.json"
    except KeyError:
        print("Erreur: Dictionnaire de résultat invalide (manque 'dataset').")
        filename = f"{output_dir}/error.json"

    # Sauvegarder en JSON
    try:
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(resultat, f, indent=4, ensure_ascii=False)
        
        # Confirmer à l'utilisateur (sera affiché après le résumé)
        resultat["saved_to"] = filename # Ajoute le chemin de sauvegarde au résultat
        
    except Exception as e:
        print(f"Erreur critique lors de la sauvegarde du fichier JSON : {e}")
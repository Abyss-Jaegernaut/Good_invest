class Action:
    """
    Représente une seule action avec son coût et son profit.
    Le profit réel (en F CFA) est calculé à l'initialisation.
    """
    def __init__(self, id_action, cost, profit_pct):
        self.id = str(id_action)
        
        # S'assurer que le coût est un entier (contrainte du problème) [cite: 22]
        self.cost = int(cost) 
        self.profit_pct = float(profit_pct)
        
        # Calculer le bénéfice réel [cite: 24]
        # profit_pct est en pourcentage (ex: 27.19 = 27.19%), donc diviser par 100
        self.profit_amount = self.cost * (self.profit_pct / 100)

    def __repr__(self):
        """Représentation textuelle pour le débogage."""
        return (
            f"Action(id={self.id}, cost={self.cost}, "
            f"profit={self.profit_amount:.2f})"
        )
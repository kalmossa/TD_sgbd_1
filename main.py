import sys
import gestion_produits as manager

def lire_entier_securise(message):
    """Boucle tant que l'utilisateur n'entre pas un entier valide."""
    while True:
        valeur = input(message)
        try:
            return int(valeur)
        except ValueError:
            print("Erreur: Veuillez entrer un nombre entier valide.")

def demarrer_application():
    print("=== GESTION DE STOCK v1.0 ===")
    
    while True:  # La "Game Loop"
        print("\n1. Lister les produits")
        print("2. Ajouter un produit")
        print("3. Vendre un produit (Transaction)")
        print("Q. Quitter")
        
        choix = input("Votre choix : > ").upper()
        
        if choix == "1":
            manager.afficher_catalogue()
        
        elif choix == "2":
            print("\n--- NOUVEAU PRODUIT ---")
            nom = input("Nom: ")
            prix = input("Prix (€): ")
            stock = lire_entier_securise("Stock initial: ")
            manager.ajouter_produit_securise(nom, prix, stock)
        
        elif choix == "3":
            print("\n--- CAISSE ENREGISTREUSE ---")
            manager.afficher_catalogue()  # Afficher d'abord le catalogue
            id_prod = lire_entier_securise("ID du produit: ")
            qte = lire_entier_securise("Quantité: ")
            
            if qte <= 0:
                print("[ERREUR] La quantité doit être positive.")
            else:
                manager.effectuer_vente_securisee(id_prod, qte)
        
        elif choix == "Q":
            print("Fermeture de l'application...")
            sys.exit()
        
        else:
            print("Option inconnue.")

if __name__ == "__main__":
    demarrer_application()
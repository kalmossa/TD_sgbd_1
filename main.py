import sys
from data_access import BoutiqueDAL

db = BoutiqueDAL()

def lire_entier_securise(message):
    """ Boucle tant que l'utilisateur n'entre pas un entier valide. """
    while True:
        valeur = input(message)
        try:
            return int(valeur)
        except ValueError:
            print("Erreur: Veuillez entrer un nombre entier valide.")

def valider_inputs_produit(nom, prix):
    """ Validation minimale (BLL simplifiée). """
    if not nom or len(str(nom).strip()) < 2:
        print("Erreur: Le nom doit contenir au moins 2 caractères.")
        return False
    if prix < 0:
        print("Erreur: Le prix ne peut pas être négatif.")
        return False
    return True

def demarrer_application():
    print("=== GESTION DE STOCK DAL v2.0 ===")

    while True:
        print("\n1. Lister les produits")
        print("2. Ajouter un produit")
        print("3. Vendre un produit (Transaction)")
        print("Q. Quitter")

        choix = input("Votre choix > ").upper()

        if choix == "1":
            produits = db.get_all_products()
            if not produits:
                print("Aucun produit.")
            else:
                print(f"--- CATALOGUE ({len(produits)}) ---")
                for p in produits:
                    print(f"[{p['id']}] {p['nom']} - {p['prix']}€ (Stock: {p['stock']})")

        elif choix == "2":
            print("\n--- NOUVEAU PRODUIT ---")
            nom = input("Nom: ")
            try:
                prix = float(input("Prix (€): "))
                stock = lire_entier_securise("Stock initial: ")

                if valider_inputs_produit(nom, prix):
                    new_id = db.create_product(nom, prix, stock)
                    if new_id:
                        print(f"Succès! ID: {new_id}")
                    else:
                        print("Erreur création.")
            except ValueError:
                print("Prix invalide.")

        elif choix == "3":
            print("\n--- CAISSE ENREGISTREUSE ---")
            id_prod = lire_entier_securise("ID du produit: ")
            qte = lire_entier_securise("Quantité: ")

            if qte <= 0:
                print("La quantité doit être positive.")
            else:
                succes = db.process_sale_transaction(id_prod, qte)
                if succes:
                    print("Vente enregistrée avec succès.")
                else:
                    print("Échec de la vente.(Stock insuffisant ou erreur technique).")

        elif choix == "Q":
            print("Fermeture...")
            sys.exit()

        else:
            print("Option inconnue.")

if __name__ == "__main__":
    demarrer_application()

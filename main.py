import sys
# ancienne ligne à supprimer : from data_access import BoutiqueDAL
# nouvelle ligne :
from business_logic import BoutiqueService

# instanciation de la couche métier (au lieu de db = BoutiqueDAL())
service = BoutiqueService()


def lire_entier_securise(message):
    """ Boucle tant que l'utilisateur n'entre pas un entier valide. """
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Erreur: Veuillez entrer un nombre entier valide.")


def demarrer_application():
    print("=== GESTION DE STOCK [ARCHITECTURE 3-TIERS] ===")

    while True:
        print("\n1. Lister les produits")
        print("2. Ajouter un produit")
        print("3. Vendre un produit (Transaction)")
        print("Q. Quitter")

        choix = input("Votre choix > ").upper()

        # 1. Lister les produits
        if choix == "1":
            # appel au service au lieu de la dal
            produits = service.obtenir_catalogue()

            if not produits:
                print("Aucun produit disponible.")
            else:
                print(f"--- CATALOGUE ({len(produits)}) ---")
                for p in produits:
                    print(f"[{p['id']}] {p['nom']} - {p['prix']}€ (Stock: {p['stock']})")

        # 2. Ajouter un produit
        elif choix == "2":
            print("\n--- NOUVEAU PRODUIT ---")
            nom = input("Nom: ")

            try:
                prix = float(input("Prix (€): "))
                stock = lire_entier_securise("Stock initial: ")

                # appel au service métier
                # remarquez qu'on ne fait plus de 'if prix < 0' ici.
                # c'est le travail du service ! le main est devenu "bête".
                new_id = service.ajouter_nouveau_produit(nom, prix, stock)

                if new_id:
                    print(f"✅ Succès! Produit créé avec l'ID: {new_id}")
                else:
                    print("❌ Erreur technique lors de la création.")

            except ValueError as e:
                # ici, on attrape les erreurs levées volontairement par la bll
                # ex: "le prix doit être positif"
                print(f"⛔ Erreur de validation : {e}")

        # 3. Vendre un produit
        elif choix == "3":
            print("\n--- CAISSE ENREGISTREUSE ---")
            id_prod = lire_entier_securise("ID du produit: ")
            qte = lire_entier_securise("Quantité: ")

            try:
                # on demande au service de traiter la vente
                service.traiter_vente(id_prod, qte)

                print("✅ Vente validée et stock mis à jour.")

            except ValueError as ve:
                # erreur de saisie logique (ex: qte négative)
                print(f"⛔ {ve}")

            except RuntimeError as re:
                # erreur remontée par la bll (ex: stock insuffisant)
                print(f"⚠️ {re}")
        # Quitter
        elif choix == "Q":
            print("Fermeture...")
            sys.exit()

        else:
            print("Option inconnue.")


if __name__ == "__main__":
    demarrer_application()

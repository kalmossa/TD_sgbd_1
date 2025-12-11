from data_access import BoutiqueDAL


class BoutiqueService:
    """
    Couche métier (BLL).
    Orchestre les interactions entre l'utilisateur et les données.
    Agit comme un filtre de sécurité logique.
    """

    def __init__(self):
        # la BLL possède une instance de la DAL pour pouvoir sauvegarder les résultats
        self.dal = BoutiqueDAL()

    def obtenir_catalogue(self):
        """
        Récupère les produits.
        Ici, pas de règle spéciale : c'est un 'passe-plat', mais nécessaire
        pour que le main ne parle pas directement à la DAL.
        """
        return self.dal.get_all_products()

    def ajouter_nouveau_produit(self, nom, prix, stock):
        """
        Valide les règles métier avant la création d'un produit.
        """
        # nettoyage des données (business rule : formatage)
        if not nom or len(nom.strip()) == 0:
            raise ValueError("Le nom du produit ne peut pas être vide.")

        nom_propre = nom.strip().upper()

        # validation métier (business rule : intégrité domaine)
        if prix <= 0:
            raise ValueError("Le prix de vente doit être strictement positif.")

        if stock < 0:
            raise ValueError("Le stock initial ne peut pas être négatif.")

        # si toutes les règles passent, on autorise l'accès à la DAL
        return self.dal.create_product(nom_propre, prix, stock)

    def traiter_vente(self, id_produit, quantite):
        """
        Gère la logique d'une vente.
        """
        # règle métier 1 : quantité cohérente
        if quantite <= 0:
            raise ValueError("La quantité vendue doit être supérieure à 0.")

        # la vérification du stock exact est réalisée dans la transaction SQL
        succes = self.dal.process_sale_transaction(id_produit, quantite)

        if not succes:
            # si la DAL renvoie False, c'est généralement un problème de stock
            # ou une erreur technique masquée
            raise RuntimeError("Échec de la vente : stock insuffisant ou erreur technique.")

        return True

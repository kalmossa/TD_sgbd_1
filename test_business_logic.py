import unittest
from unittest.mock import MagicMock
from business_logic import BoutiqueService


class TestBoutiqueService(unittest.TestCase):

    def setUp(self):
        """
        cette méthode s'exécute automatiquement AVANT chaque test.
        elle sert à remettre les compteurs à zéro.
        """
        # 1. on instancie le service à tester
        self.service = BoutiqueService()

        # 2. LE MOCKING (étape critique)
        self.service.dal = MagicMock()

    def test_regle_prix_negatif(self):
        """
        scénario : on essaie de créer un produit avec un prix négatif.
        résultat attendu : le service doit lever une ValueError.
        """
        with self.assertRaises(ValueError):
            self.service.ajouter_nouveau_produit("test", -10, 5)

        self.service.dal.create_product.assert_not_called()

    def test_regle_stock_negatif(self):
        """
        scénario : prix ok, mais stock négatif.
        résultat attendu : ValueError.
        """
        with self.assertRaises(ValueError):
            self.service.ajouter_nouveau_produit("test", 100, -5)

    def test_creation_produit_valide(self):
        """
        scénario : tout est correct (cas nominal).
        résultat attendu : la dal est appelée avec les bonnes données transformées.
        """
        nom_sale = " coca cola "
        prix = 1.5
        stock = 100

        self.service.ajouter_nouveau_produit(nom_sale, prix, stock)

        self.service.dal.create_product.assert_called_once_with("COCA COLA", 1.5, 100)

    # --------------------------------------------------------------
    # ÉTAPE D : tests de la vente (simulation de retour mock)
    # --------------------------------------------------------------

    def test_vente_reussie(self):
        """
        vérifie qu'une vente valide appelle bien la transaction sql.
        """
        # on "dresse" le mock : "si on t'appelle, réponds True"
        self.service.dal.process_sale_transaction.return_value = True

        # action
        resultat = self.service.traiter_vente(id_produit=1, quantite=5)

        # vérification
        self.assertTrue(resultat)
        self.service.dal.process_sale_transaction.assert_called_once_with(1, 5)

    def test_vente_quantite_invalide(self):
        """
        vérifie qu'on ne peut pas vendre 0 ou -1 produit.
        """
        with self.assertRaises(ValueError):
            self.service.traiter_vente(1, 0)

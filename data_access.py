from database_config import get_connection, log_critical_error

class BoutiqueDAL:
    """ Data Access Layer. Toutes les interactions SQL passent par ici. """

    def get_all_products(self):
        conn = get_connection()
        if not conn:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nom, prix, stock FROM produits ORDER BY id")
                lignes = cursor.fetchall()
                return [{"id": r[0], "nom": r[1], "prix": r[2], "stock": r[3]} for r in lignes]
        except Exception as e:
            log_critical_error("DAL get_all_products", e)
            return []
        finally:
            conn.close()

    def create_product(self, nom, prix, stock):
        conn = get_connection()
        if not conn:
            return None

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO produits (nom, prix, stock) VALUES (%s, %s, %s) RETURNING id",
                    (nom, prix, stock)
                )
                conn.commit()
                return cursor.fetchone()[0]

        except Exception as e:
            conn.rollback()
            log_critical_error("DAL create_product", e)
            return None

        finally:
            conn.close()

    def process_sale_transaction(self, id_produit, quantite):
        """
        Migration directe de effectuer_vente_securisee (Partie 6).
        Logique de vente blindée (locking, update, insertion vente…)
        """
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

           # ÉTAPE 1 : Verrouillage (Locking) + Récupération infos
# La clause 'FOR UPDATE' pose un verrou exclusif sur la ligne ciblée.
            cursor.execute(
                "SELECT stock, nom, prix FROM produits WHERE id = %s FOR UPDATE",
                (id_produit,)
            )
            resultat = cursor.fetchone()

            if not resultat:
                raise ValueError("Produit introuvable")

            stock_actuel = resultat[0]
            nom_produit = resultat[1]
            prix_unitaire = resultat[2]

            # ÉTAPE 2 : Vérification métier
            if stock_actuel < quantite:
                raise ValueError(f"Stock insuffisant ({stock_actuel})")

            # ÉTAPE 3 : Double écriture (Stock + Historique)
            nouv_stock = stock_actuel - quantite
            total_vente = prix_unitaire * quantite

            cursor.execute(
                "UPDATE produits SET stock = %s WHERE id = %s",
                (nouv_stock, id_produit)
            )

            cursor.execute(
                "INSERT INTO ventes (produit_id, quantite, total, date_vente) VALUES (%s, %s, %s, NOW())",
                (id_produit, quantite, total_vente)
            )

            # ÉTAPE 4 : Commit (Libération du verrou + Sauvegarde disque)
            conn.commit()
            print(f"[SUCCÈS] Vente validée pour {total_vente}€.")
            return True

        except Exception as e:
            # ÉTAPE 5 : ROLLBACK (Annulation totale, retour à l'état initial)
            conn.rollback()
            log_critical_error("DAL process_sale_transaction", e)
            print(f"[ÉCHEC] {e}")
            return False

        finally:
            conn.close()

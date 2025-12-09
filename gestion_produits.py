from database_config import get_connection, log_critical_error

def ajouter_produit(nom, prix, stock):
    conn = get_connection()
    if conn is None: 
        return
    
    query = "INSERT INTO produits (nom, prix, stock) VALUES (%s, %s, %s);"
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, (nom, prix, stock))
        conn.commit()
        print(f"[SUCCÈS] Produit '{nom}' inséré.")
    except Exception as e:
        conn.rollback()
        log_critical_error("Insertion produit", e)
        print(f"[ERREUR SQL] Impossible d'insérer: {e}")
    finally:
        cursor.close()
        conn.close()


def afficher_catalogue():
    conn = get_connection()
    if conn is None: 
        return
    
    query = "SELECT id, nom, prix, stock FROM produits ORDER BY nom;"
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        lignes = cursor.fetchall()
        
        print(f"\n--- CATALOGUE ({len(lignes)} articles) ---")
        for produit in lignes:
            print(f"[{produit[0]}] {produit[1]} \t: {produit[2]} € (Stock: {produit[3]})")
    except Exception as e:
        log_critical_error("Lecture catalogue", e)
        print(f"[ERREUR LECTURE]: {e}")
    finally:
        conn.close()


def valider_produit(nom, prix, stock):
    """Vérifie les règles métier avant toute connexion SGBD."""
    
    # Règle 1: Nettoyage et existence du nom
    if not nom or len(str(nom).strip()) < 2:
        return False, "Le nom doit contenir au moins 2 caractères visibles."
    
    # Règle 2: Type et valeur positive du prix
    try:
        prix_float = float(prix)
        if prix_float < 0:
            return False, "Le prix ne peut pas être négatif."
    except ValueError:
        return False, "Le prix doit être une valeur numérique."
    
    # Règle 3: Validation du stock (CORRECTION MAJEURE)
    try:
        stock_int = int(stock)
        if stock_int < 0:
            return False, "Le stock ne peut pas être négatif."
    except ValueError:
        return False, "Le stock doit être un nombre entier."
    
    return True, None


def ajouter_produit_securise(nom, prix, stock):
    # 1. Validation Applicative (Business Layer)
    est_valide, message_erreur = valider_produit(nom, prix, stock)
    if not est_valide:
        print(f"[ANNULATION] {message_erreur}")
        return
    
    # 2. Si valide, appel de la couche de données
    ajouter_produit(nom, prix, stock)


def effectuer_vente_securisee(id_produit, quantite):
    """Transaction de vente avec verrouillage pessimiste (Partie 6)."""
    conn = get_connection()
    if not conn: 
        return False
    
    try:
        cursor = conn.cursor()
        
        # ÉTAPE 1: Verrouillage + Récupération infos
        cursor.execute(
            "SELECT stock, nom, prix FROM produits WHERE id = %s FOR UPDATE",
            (id_produit,)
        )
        resultat = cursor.fetchone()
        
        if not resultat:
            raise ValueError("Produit introuvable")
        
        stock_actuel, nom_produit, prix_unitaire = resultat
        
        # ÉTAPE 2: Vérification Métier
        if stock_actuel < quantite:
            raise ValueError(f"Stock insuffisant ({stock_actuel} disponible)")
        
        # ÉTAPE 3: Double écriture (Stock + Historique)
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
        
        # ÉTAPE 4: COMMIT (Libération du verrou + Sauvegarde disque)
        conn.commit()
        print(f"[SUCCÈS] Vente validée : {quantite}x {nom_produit} = {total_vente}€")
        print(f"[INFO] Nouveau stock : {nouv_stock}")
        return True
        
    except Exception as e:
        # ÉTAPE 5: ROLLBACK (Annulation totale)
        conn.rollback()
        log_critical_error("Transaction Vente", e)
        print(f"[ÉCHEC] {e}")
        return False
    finally:
        cursor.close()
        conn.close()
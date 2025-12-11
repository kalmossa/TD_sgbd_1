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
        for p in lignes:
            print(f"[{p[0]}] {p[1]} : {p[2]}€ (Stock: {p[3]})")
    except Exception as e:
        log_critical_error("Lecture catalogue", e)
        print(f"[ERREUR LECTURE]: {e}")
    finally:
        conn.close()

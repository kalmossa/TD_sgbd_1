from database_config import get_connection
def ajouter_produit(nom, prix, stock):
conn = get_connection()
if conn is None: return
# REQUÊTE PARAMÉTRÉE (%s) : Protection contre l'injection SQL
query = "INSERT INTO produits (nom, prix, stock) VALUES (%s, %s, %s);"
try:
cursor = conn.cursor()
# Exécution : Les données sont en mémoire tampon (Brouillon)
cursor.execute(query, (nom, prix, stock))
# COMMIT : Validation explicite. Le serveur écrit sur le disque dur.
conn.commit()
print(f"[SUCCÈS] Produit '{nom}' inséré.")
except Exception as e:
# ROLLBACK : En cas d'erreur, on annule tout (Filet de sécurité)
conn.rollback()
print(f"[ERREUR SQL] Impossible d'insérer: {e}")
finally:
# Nettoyage obligatoire pour éviter l'erreur "Too many connections"
cursor.close()
conn.close()

def afficher_catalogue():
conn = get_connection()
if conn is None: return
query = "SELECT id, nom, prix, stock FROM produits ORDER BY nom;"
try:
cursor = conn.cursor()
cursor.execute(query)
# fetchall() récupère toutes les lignes restantes dans le curseur
lignes = cursor.fetchall()
print(f"\n--- CATALOGUE ({len(lignes)} articles) ---")
for produit in lignes:
# produit est un tuple : (id, nom, prix, stock)
print(f"[{produit[0]}] {produit[1]} \t: {produit[2]} € (Stock: {produit[3]})")
except Exception as e:
print(f"[ERREUR LECTURE]: {e}")
finally:
conn.close()
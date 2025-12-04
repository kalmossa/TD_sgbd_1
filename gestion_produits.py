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

def valider_produit(nom, prix, stock):
""" Vérifie les règles métier avant toute connexion SGBD. """
# Règle 1: Nettoyage et existence
if not nom or len(str(nom).strip()) < 2:
return False, "Le nom doit contenir au moins 2 caractères visibles."
# Règle 2: Type et valeur positive
try:
prix_float = float(prix)
if prix_float < 0:
return False, "Le prix ne peut pas être négatif."
except ValueError:
return False, "Le prix doit être une valeur numérique."
return True, None
def ajouter_produit_securise(nom, prix, stock):
# 1. Validation Applicative (Business Layer)
est_valide, message_erreur = valider_produit(nom, prix, stock)
if not est_valide:
print(f"[ANNULATION] {message_erreur}")
return # On arrête tout ici, le SGBD n'est pas contacté.
# 2. Si valide, appel de la couche de données
ajouter_produit(nom, prix, stock) 
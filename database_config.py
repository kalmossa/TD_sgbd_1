import psycopg2
from psycopg2 import OperationalError
def get_connection():
"""
Établit une session avec le serveur PostgreSQL.
Retourne: Objet de connexion psycopg2 ou None en cas d'échec.
"""
# DSN (Data Source Name): L'adresse complète de destination
# MISE À JOUR : Utilisation de 'boutique_user' créé en Partie 0
dsn = "host=localhost dbname=boutique_db user=boutique_user
password=secure_pass_123"
try:
# TENTATIVE DE CONNEXION :
# 1. Envoi d'un paquet SYN au serveur.
# 2. Handshake et Authentification.
# 3. Allocation de mémoire (fork d'un processus dédié sur le serveur).
conn = psycopg2.connect(dsn)
print("[INFO] Connexion au SGBD réussie.")
return conn
except OperationalError as e:
# Capture les erreurs réseaux (câble débranché, serveur éteint) ou d'auth.
print(f"[ERREUR CRITIQUE] Échec de connexion au SGBD: {e}")
return None
# Test unitaire rapide
if __name__ == "__main__":
test_conn = get_connection()
if test_conn:
test_conn.close() # Règle d'or: Toujours fermer ce qu'on a ouvert (libération RAM serveur)
print("[INFO] Connexion fermée proprement."
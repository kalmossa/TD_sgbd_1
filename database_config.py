import psycopg2
from psycopg2 import OperationalError
import logging
import os

# Création du dossier de logs
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configuration du logging (Partie 5)
logging.basicConfig(
    filename='logs/db_errors.log',
    level=logging.ERROR,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

def log_critical_error(context, exception):
    """Enregistre l'erreur technique pour le développeur."""
    logging.error(f"Contexte: {context} | Exception: {exception}")

def get_connection():
    """
    Établit une session avec le serveur PostgreSQL.
    Retourne: Objet de connexion psycopg2 ou None en cas d'échec.
    """
    # DSN corrigé : tout sur UNE SEULE ligne
    dsn = "host=localhost dbname=boutique_db user=boutique_user password=secure_pass_123"
    
    try:
        conn = psycopg2.connect(dsn)
        print("[INFO] Connexion au SGBD réussie.")
        return conn
    except OperationalError as e:
        log_critical_error("Connexion SGBD", e)
        print(f"[ERREUR CRITIQUE] Échec de connexion au SGBD: {e}")
        return None

# Test unitaire rapide
if __name__ == "__main__":
    test_conn = get_connection()
    if test_conn:
        test_conn.close()
        print("[INFO] Connexion fermée proprement.")
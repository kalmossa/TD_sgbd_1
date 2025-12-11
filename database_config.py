import psycopg2
from psycopg2 import OperationalError
import logging
import os
from dotenv import load_dotenv # nouvel import

# charge le fichier .env en mémoire
load_dotenv()

# Création du dossier de logs
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/db_errors.log',
    level=logging.ERROR,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

def log_critical_error(context, exception):
    """ Enregistre l'erreur technique pour le développeur. """
    logging.error(f"Contexte: {context} | Exception: {exception}")

def get_connection():
    """
    établit une session avec le serveur postgresql via variable d'environnement.
    """
    # on récupère l'url sécurisée au lieu du dsn hardcodé
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        log_critical_error("config", "variable DATABASE_URL manquante dans le .env")
    return None

    try:
        conn = psycopg2.connect(dsn)
        print("[INFO] Connexion au SGBD réussie.")
        return conn
    except OperationalError as e:
        log_critical_error("Connexion SGBD", e)
        print("[ERREUR] Service indisponible.")
        return None

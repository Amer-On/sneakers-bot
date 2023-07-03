import dotenv
import os


dotenv.load_dotenv()

PG_HOST = os.getenv("PG_HOST")
PG_DBNAME = os.getenv("PG_DBNAME")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_PORT = os.getenv("PG_PORT", default="5432")

FIRM_DBNAME = "Firms"
MODELS_DBNAME = "Models"

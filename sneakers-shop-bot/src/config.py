from os import getenv
import dotenv


dotenv.load_dotenv()

TOKEN = getenv("TOKEN")
SKIP_UPDATES = getenv("SKIP_UPDATES") == "True"
DEBUG = getenv("DEBUG") == "True"

LOGGING_FILE = "logs.log"

REDIS_ADDRESS = getenv('REDIS_ADDRESS')
REDIS_PORT = int(getenv("REDIS_PORT"))

assert type(TOKEN) is str
assert type(SKIP_UPDATES) is bool
assert type(DEBUG) is bool
assert type(REDIS_ADDRESS) is str
assert type(REDIS_PORT) is int

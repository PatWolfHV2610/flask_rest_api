import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URI = os.getenv("REDIS_URI")
QUEUES = ["emails", "default"]
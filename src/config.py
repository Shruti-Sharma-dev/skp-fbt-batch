import os
from dotenv import load_dotenv
import yaml

# Load .env
load_dotenv()

WC_API_URL = os.getenv("WC_API_URL")
WC_CONSUMER_KEY = os.getenv("WC_CONSUMER_KEY")
WC_CONSUMER_SECRET = os.getenv("WC_CONSUMER_SECRET")
TOP_N = int(os.getenv("TOP_N_RECOMMENDATIONS", 3))
INCLUDE_OUT_OF_STOCK = os.getenv("INCLUDE_OUT_OF_STOCK", "false").lower() == "true"

# Load config.yaml
with open("configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)

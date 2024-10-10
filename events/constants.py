import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access environment variables
INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID')
BAYC_CONTRACT_ADDRESS = os.getenv('BAYC_CONTRACT_ADDRESS')
TRANSFER_EVENT_SIGNATURE = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
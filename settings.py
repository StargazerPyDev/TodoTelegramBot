from dotenv import load_dotenv

## using existing module to specify location of the .env file
from pathlib import Path
import os

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

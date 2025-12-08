import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add the 'ai-escape-app' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# You can add common fixtures here later if needed


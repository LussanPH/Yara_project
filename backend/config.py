from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv("PORT"))
NGROK_DOMAIN = os.getenv("NGROK_DOMAIN")
NGROK_TOKEN = os.getenv("NGROK_TOKEN")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRATE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRATE_MINUTES"))

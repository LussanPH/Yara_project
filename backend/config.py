from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv("PORT"))
NGROK_DOMAIN = os.getenv("NGROK_DOMAIN")
NGROK_TOKEN = os.getenv("NGROK_TOKEN")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRATE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRATE_MINUTES"))
GROK_API_KEY = os.getenv('GROK_API_KEY')
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///banco.db")

for prefixo in ("postgres://", "postgresql://"):
    if DATABASE_URL.startswith(prefixo):
        DATABASE_URL = DATABASE_URL.replace(prefixo, "postgresql+psycopg://", 1)
        break


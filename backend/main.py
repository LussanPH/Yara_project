from fastapi import FastAPI
from dotenv import load_dotenv
from pyngrok import ngrok
from contextlib import asynccontextmanager
import uvicorn
import os

load_dotenv()

PORT = int(os.getenv("PORT"))
NGROK_DOMAIN = os.getenv("NGROK_DOMAIN")
NGROK_TOKEN = os.getenv("NGROK_TOKEN")

#FAZ COM QUE O TÚNEL SEJA ABERTO APENAS UMA VEZ DURANTE A EXECUÇÃO DO UVICORN
@asynccontextmanager
async def lifespan(app : FastAPI):
    ngrok.set_auth_token(NGROK_TOKEN)

    tunnel = ngrok.connect(
        PORT,
        domain=NGROK_DOMAIN
    )

    print(f"Tunnel opened with success! {tunnel.public_url}")

    yield

    ngrok.disconnect(public_url=tunnel.public_url)


app = FastAPI(lifespan=lifespan)

from acs_ace_routes import acs_ace_router
from ubs_routes import ubs_router

app.include_router(acs_ace_router)
app.include_router(ubs_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=PORT, reload=True)#uvicorn main:app --host="127.0.0.1" --port 8000 --reload



from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from pyngrok import ngrok
from contextlib import asynccontextmanager
from config import NGROK_DOMAIN, NGROK_TOKEN, PORT
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

from acs_ace_routes import acs_ace_router
from ubs_routes import ubs_router
from auth_routes import auth_router
from coordenador_routes import cm_router

app.include_router(acs_ace_router)
app.include_router(ubs_router)
app.include_router(cm_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=PORT, reload=True)#uvicorn main:app --host="127.0.0.1" --port 8000 --reload



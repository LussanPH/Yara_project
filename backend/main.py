from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from pyngrok import ngrok
from contextlib import asynccontextmanager
from config import NGROK_DOMAIN, NGROK_TOKEN, PORT
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

from routes.acs_ace_routes import acs_ace_router
from routes.ubs_routes import ubs_router
from routes.auth_routes import auth_router
from routes.coordenador_routes import cm_router
from routes.vigilantes_regional_routes import vr_router
from routes.vigilantes_estadual_routes import ve_router

app.include_router(acs_ace_router)
app.include_router(ubs_router)
app.include_router(cm_router)
app.include_router(auth_router)
app.include_router(vr_router)
app.include_router(ve_router)

#if __name__ == "__main__":
    #uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)#uvicorn main:app --host="127.0.0.1" --port 8000 --reload



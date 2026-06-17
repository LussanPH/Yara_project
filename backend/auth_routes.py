from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import create_session, token_verification
from sqlalchemy.orm import Session
from models import Agente, UBS
from security import verify_password
from datetime import timedelta, datetime, timezone
from config import ACCESS_TOKEN_EXPIRATE_MINUTES, ALGORITHM, SECRET_KEY
from jose import jwt, JWTError


def create_jwt(id_usuario, tipo, duracao_token = timedelta(minutes=ACCESS_TOKEN_EXPIRATE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token

    dicionario_informacoes = {"sub":str(id_usuario), "exp":data_expiracao, "tipo":tipo}

    if SECRET_KEY and ALGORITHM:
        jwt_codificado = jwt.encode(dicionario_informacoes, SECRET_KEY, ALGORITHM)

    return jwt_codificado

#VERIFICA SE O USUÁRIO ESTÁ PRESENTE NO BANCO DE DADOS E SE A SENHA É CORRESPONDENTE
def login_auth(email, senha, tipo, session:Session):
    if tipo == "ACS/ACE":
        usuario = session.query(Agente).filter(Agente.email == email).first()
    elif tipo == "UBS":
        usuario = session.query(UBS).filter(UBS.email == email).first()
    else:#PARA TESTE
        usuario = session.query(Agente).filter(Agente.email == email).first()

    if not usuario:
        return False
    elif not verify_password(senha, usuario.senha):
        return False
    
    return usuario



auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])


@auth_router.post("/login")
#Form = (None) Para testes
async def login(dados_login:OAuth2PasswordRequestForm = Depends(), tipo_login:str = Form(None), session : Session = Depends(create_session)):
    usuario = login_auth(dados_login.username, dados_login.password, tipo_login, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou senha inválida.")
    
    access_token = create_jwt(usuario.id, tipo_login)
    refresh_token = create_jwt(usuario.id, tipo_login, timedelta(days=7))

    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "type_token" : "Bearer"
    }


@auth_router.post("/refresh")
async def create_access_token(usuario : Agente | UBS = Depends(token_verification)):
    
    if str(type(usuario)) == "Agente":
        access_token = create_jwt(usuario.id, "ACS/ACE")

    elif str(type(usuario)) == "UBS":
        access_token = create_jwt(usuario.id, "UBS")

    return {
        "access_token" : access_token,
        "type_token": "Bearer"
    }
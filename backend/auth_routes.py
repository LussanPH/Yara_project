from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import create_session, token_verification
from sqlalchemy.orm import Session
from typing import Optional
from models import Agente, UBS
from security import verify_password
from datetime import timedelta, datetime, timezone
from config import ACCESS_TOKEN_EXPIRATE_MINUTES, ALGORITHM, SECRET_KEY
from jose import jwt, JWTError

#Cria o jwt_token para com os dados de id, tipo e data de expiração do token
def create_jwt(id_usuario, tipo, duracao_token = timedelta(minutes=ACCESS_TOKEN_EXPIRATE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token

    if tipo in ['ACS', 'ACE']:
        tipo = 'ACS/ACE'

    dicionario_informacoes = {"sub":str(id_usuario), "exp":data_expiracao, "tipo":tipo}

    if SECRET_KEY and ALGORITHM:
        jwt_codificado = jwt.encode(dicionario_informacoes, SECRET_KEY, ALGORITHM)

    return jwt_codificado

#Verifica se o login efetuado corresponde a um usuário do banco de dados correspondente ao seu respectivo tipo
def login_auth(email, senha, tipo, session:Session):
    if tipo == "ACS/ACE":
        usuario = session.query(Agente).filter(Agente.email == email).first()
    elif tipo == "UBS":
        usuario = session.query(UBS).filter(UBS.email == email).first()
    else:
        return False

    if not usuario:
        return False
    elif not verify_password(senha, usuario.senha):
        return False
    
    return usuario



auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])


#Endpoint de login do usuário
@auth_router.post("/login")
#Form = (None) Para testes
async def login(dados_login:OAuth2PasswordRequestForm = Depends(), tipo_login:Optional[str] = Form(None), session : Session = Depends(create_session)):
    #Caso seja feito pelo authorize do docs do Fastapi, verifica o campo client_id para rastrear o tipo de usuário

    print(dados_login.username)
    print(dados_login.password)
    print(tipo_login)

    usuario = login_auth(dados_login.username, dados_login.password, tipo_login, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou senha inválida.")
    
    access_token = create_jwt(usuario.id, tipo_login)
    refresh_token = create_jwt(usuario.id, tipo_login, timedelta(days=1))

    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "type_token" : "Bearer"
    }


#Endpoint para a criação de um no access_token a partir do refresh_token
@auth_router.post("/refresh")
async def create_access_token(dict_info : Agente | UBS = Depends(token_verification)):
    
    if dict_info.get("tipo") == "ACS/ACE":
        access_token = create_jwt(dict_info.get("sub"), "ACS/ACE")

    elif dict_info.get("tipo") == "UBS":
        access_token = create_jwt(dict_info.get("sub"), "UBS")

    return {
        "access_token" : access_token,
        "type_token": "Bearer"
    }
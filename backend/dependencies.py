from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models import db, Agente, UBS
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session

    finally:
        session.close()

def token_verification(token:str = Depends(oauth2_schema), session:Session = Depends(create_session)):
    if SECRET_KEY and ALGORITHM:
        try:
            dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
            usuario_id = int(dic_info.get("sub"))
            tipo_usuario = dic_info.get("tipo")

        except JWTError:
            raise HTTPException(status_code=401, detail="Acesso Negado.")
        
        if tipo_usuario == "ACS/ACE":
            usuario = session.query(Agente).filter(Agente.id == usuario_id).first()
        elif tipo_usuario == "UBS":
            usuario = session.query(UBS).filter(UBS.id == usuario_id).first()

        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário Inválido.")
        
        return usuario
        



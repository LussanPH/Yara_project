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
        else:
            usuario = session.query(Agente).filter(Agente.id == usuario_id).first() #Para testes

        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário Inválido.")
        
        return dic_info
    

class RoleChecker:
    def __init__(self, allowed_roles : list):
        self.allowed_roles = allowed_roles

    def __call__(self, usuario : dict = Depends(token_verification)):
        if usuario.get("tipo") not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Acesso Negado.")
        
        return usuario
    
somente_Agente = RoleChecker(["ACS/ACE"])
somente_UBS = RoleChecker(["UBS"])



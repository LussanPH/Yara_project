from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models import db, Agente, UBS, Coordenador_Municipal
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM
from datetime import datetime, timezone

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

#Cria uma sessão para comandos SQL em funções de criação/modificação de dados nas tabelas
def create_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session

    finally:
        session.close()

#Verificação da validade do jwt
def token_verification(token:str = Depends(oauth2_schema), session:Session = Depends(create_session)):
    print("TOKEN RECEBIDO:", token)
    if SECRET_KEY and ALGORITHM:
        try:
            dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
            usuario_id = int(dict_info.get("sub"))
            tipo_usuario = dict_info.get("tipo")

        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Erro ao validar token: {e}")

        
        if tipo_usuario == "ACS/ACE":
            usuario = session.query(Agente).filter(Agente.id == usuario_id).first()
        elif tipo_usuario == "UBS":
            usuario = session.query(UBS).filter(UBS.id == usuario_id).first()
        elif tipo_usuario == "CM":
            usuario = session.query(Coordenador_Municipal).filter(Coordenador_Municipal.id == usuario_id).first()

        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário não encontrado.")
        
        return dict_info



#Com base no token, retorna o usuário que está logado atualmente
def get_usuario(token:str = Depends(oauth2_schema), session:Session = Depends(create_session)):
    if SECRET_KEY and ALGORITHM:
        try:
            dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)

        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Erro ao validar token: {e}")
        
        usuario_id = int(dict_info.get('sub'))
        tipo_usuario = dict_info.get('tipo')

        if tipo_usuario == 'ACS/ACE':
            usuario = session.query(Agente).filter(Agente.id == usuario_id).first()
        elif tipo_usuario == 'UBS':
            usuario = session.query(UBS).filter(UBS.id == usuario_id).first()
        elif tipo_usuario == 'CM':
            usuario = session.query(Coordenador_Municipal).filter(Coordenador_Municipal.id == usuario_id).first()

        if not usuario:
            raise HTTPException(status_code=401, detail=f'Usuário {tipo_usuario} não encontrado no banco de dados.')
        
        return usuario


#Classe para a restrição de caminhos com base no tipo do usuário
class RoleChecker:
    def __init__(self, allowed_roles : list):
        self.allowed_roles = allowed_roles

    def __call__(self, dict_info : dict = Depends(token_verification)):
        if dict_info.get("tipo") not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Acesso Negado.")
        
        return dict_info
    
somente_Agente = RoleChecker(["ACS/ACE"])
somente_UBS = RoleChecker(["UBS"])
somente_CM = RoleChecker(["CM"])



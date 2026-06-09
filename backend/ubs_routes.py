from fastapi import APIRouter, Depends, HTTPException
from dependencies import create_session
from schemas import NotificacaoSchema, AgenteSchema, UBSSchema
from models import Agente, UBS, Notificacao
from sqlalchemy.orm import Session
from security import get_hashed_password
from sqlalchemy.exc import SQLAlchemyError
import datetime

ubs_router = APIRouter(prefix="/ubs", tags=["ubs"])



@ubs_router.post("/criar_ubs")
async def criar_ubs(ubs_schema : UBSSchema, session : Session = Depends(create_session)):
    ubs = session.query(UBS).filter(UBS.email == ubs_schema.email).first()

    if ubs:
        raise HTTPException(status_code=400, detail="UBS já cadastrada no sistema!")
    
    senha_hashed = get_hashed_password(ubs_schema.senha)
    ubs_nova = UBS(senha_hashed, ubs_schema.nome, ubs_schema.ubs, ubs_schema.municipio, ubs_schema.email)
    session.add(ubs_nova)
    session.commit()
    
    return {"message": "UBS criada com sucesso!"}
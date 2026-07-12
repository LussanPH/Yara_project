from fastapi import APIRouter, Depends, HTTPException
from dependencies import create_session, token_verification, somente_UBS
from schemas import NotificacaoSchema, AgenteSchema, UBSSchema, DadosUBSSchema
from models import Agente, UBS, Notificacao, Dados_UBS
from sqlalchemy.orm import Session
from security import get_hashed_password
from sqlalchemy.exc import SQLAlchemyError
import datetime

ubs_router = APIRouter(prefix="/ubs", tags=["ubs"], dependencies=[Depends(somente_UBS)])


#Criação de um agente
@ubs_router.post("/criar_agente")
async def criar_agente(agente_schema : AgenteSchema, session : Session = Depends(create_session)):
    agente = session.query(Agente).filter(Agente.email == agente_schema.email).first()

    if agente:
        raise HTTPException(status_code=400, detail="Agente já cadastrado no sistema!")
    
    senha_hash = get_hashed_password(agente_schema.senha)
    agente = Agente(senha_hash, agente_schema.cargo, agente_schema.nome, agente_schema.ubs_atuante, agente_schema.email)
    session.add(agente)
    session.commit()

    return {
        "response" : f"Email {agente_schema.email} cadastrado com sucesso"
    }


#Criação de uma conta UBS
@ubs_router.post("/criar_conta_ubs")
async def criar_conta_ubs(ubs_schema : UBSSchema, session : Session = Depends(create_session)):
    ubs = session.query(UBS).filter(UBS.email == ubs_schema.email).first()

    if ubs:
        raise HTTPException(status_code=400, detail="Conta UBS já cadastrada no sistema!")
    
    senha_hashed = get_hashed_password(ubs_schema.senha)
    ubs_nova = UBS(senha_hashed, ubs_schema.nome, ubs_schema.ubs, ubs_schema.municipio, ubs_schema.email)
    session.add(ubs_nova)
    session.commit()
    
    return {"message": "Conta UBS criada com sucesso!"}


#Criação de uma UBS
@ubs_router.post("/criar_ubs")
async def criar_ubs(dados_ubs_schema : DadosUBSSchema, session: Session = Depends(create_session)):
    dados_ubs = session.query(Dados_UBS).filter(Dados_UBS.nome == dados_ubs_schema.nome).first()

    if dados_ubs:
        raise HTTPException(status_code=400, detail=f"Dados da UBS {dados_ubs.nome} já cadastrada no sistema.")
    
    dados_ubs_nova = Dados_UBS(dados_ubs_schema.nome, dados_ubs_schema.municipio, dados_ubs_schema.estado)
    session.add(dados_ubs_nova)
    session.commit()

    return {'message':f'Dados da UBS {dados_ubs_nova.nome} cadastrados com sucesso!'}
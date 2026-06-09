from fastapi import APIRouter, Depends, HTTPException
from dependencies import create_session
from schemas import NotificacaoSchema, AgenteSchema
from models import Agente, UBS, Notificacao
from sqlalchemy.orm import Session
from security import get_hashed_password
import datetime


acs_ace_router = APIRouter(prefix="/agentes", tags=["Agentes"])


@acs_ace_router.post("/criar_agente")
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



@acs_ace_router.get("/listar_notificacoes")
async def listar_notificacoes(id_agente : int, session : Session = Depends(create_session)):
    agente = session.query(Agente).filter(Agente.id == id_agente).first()

    if not agente:
        raise HTTPException(status_code=400, detail="Usuário não encontrado no sistema!")

    notificacoes = session.query(Notificacao).filter(Notificacao.id == Agente).all()

    return {
        "Notificações" : notificacoes
    }



@acs_ace_router.post("/criar_notificacao")
async def criar_notificacao(id_agente : int, notificacao : NotificacaoSchema, session : Session = Depends(create_session)):
    agente = session.query(Agente).filter(Agente.id == id_agente).first()

    if not agente:
        raise HTTPException(status_code=400, detail="Usuário não encontrado no sistema!")
    
    data_hora = datetime.datetime.now()
    data_hora = data_hora.strftime("%d/%m/%Y %H:%M")

    print(data_hora)
    
    notificacao_nova = Notificacao("Surto de Varíola",
                              "DOENÇA", "Doença Contagiante",  
                              data_hora, 10, 
                              "Sapiranga", 
                              "Escola", 
                              "Sim", 
                              "Muitas crianças com sintomas correspondentes ao da varíola na mesma turma", 
                              agente.id, 
                              "EM ANDAMENTO", 
                              False)
    
    session.add(notificacao_nova)
    session.commit()

    return {
        "response" : f"Notificação {notificacao_nova.nome} com id {notificacao_nova.id} Criada com sucesso!"
    }



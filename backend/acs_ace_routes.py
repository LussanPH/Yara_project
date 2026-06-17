from fastapi import APIRouter, Depends, HTTPException
from dependencies import create_session, token_verification
from schemas import NotificacaoSchema, AgenteSchema
from models import Agente, UBS, Notificacao
from sqlalchemy.orm import Session
from security import get_hashed_password
import datetime


acs_ace_router = APIRouter(prefix="/agentes", tags=["Agentes"], dependencies=[Depends(token_verification)])



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
    
    notificacao_nova = Notificacao(notificacao.nome,
                              notificacao.tipo_evento,
                              notificacao.categoria,  
                              notificacao.data_envio, 
                              notificacao.pessoas_animais_infectados_afetados, 
                              notificacao.local_ocorrencia, 
                              notificacao.meio_identificacao, 
                              notificacao.continuidade_situacao, 
                              notificacao.descricao, 
                              agente.id, 
                              notificacao.status, 
                              notificacao.rascunho)
    
    session.add(notificacao_nova)
    session.commit()

    return {
        "response" : f"Notificação {notificacao_nova.nome} com id {notificacao_nova.id} Criada com sucesso!"
    }



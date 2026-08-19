from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import create_session, somente_UBS, get_usuario
from security import get_hashed_password
from models import Notificacao, UBS, Agente, Dados_UBS
from schemas import NotificacaoSchema, UBSSchema, AgenteSchema
import datetime

ubs_router = APIRouter(prefix="/ubs", tags=["ubs"], dependencies=[Depends(somente_UBS)])


#Criação de conta ubs
@ubs_router.post("/criar_conta")
async def criar_ubs(ubs_schema : UBSSchema, session : Session = Depends(create_session)): 
    ubs = session.query(UBS).filter(UBS.email == ubs_schema.email).first()

    if ubs:
        raise HTTPException(status_code=400, detail="UBS já cadastrada no sistema!")
    
    senha_hashed = get_hashed_password(ubs_schema.senha)
    ubs_nova = UBS(senha_hashed, ubs_schema.nome, ubs_schema.ubs, ubs_schema.municipio, ubs_schema.email)
    session.add(ubs_nova)
    session.commit()
    
    return {"message": "UBS criada com sucesso!"}


#Criação de conta acs/ace
async def criar_ubs(agente_schema : AgenteSchema, session : Session = Depends(create_session)): 
    acs_ace = session.query(Agente).filter(Agente.email == agente_schema.email).first()

    if acs_ace:
        raise HTTPException(status_code=400, detail="UBS já cadastrada no sistema!")
    
    senha_hashed = get_hashed_password(acs_ace.senha)
    acs_ace_novo = Agente(senha_hashed, acs_ace.cargo, acs_ace.nome, acs_ace.ubs_atuante)
    session.add(acs_ace_novo)
    session.commit()
    
    return {"message": f"Agente {acs_ace_novo.cargo} criada com sucesso!"}


# Listar notificações associadas aos agentes da UBS logada
@ubs_router.get("/notificacoes")
async def listar_notificacoes_ubs(usuario = Depends(get_usuario), session : Session = Depends(create_session)):
    try:
        notificacoes = session.query(Notificacao).join(Agente, Notificacao.acs_ace_id == Agente.id).filter(Agente.ubs_atuante == usuario.ubs, Notificacao.rascunho == False).all()      #RETORNA AS NOTIFICAÇÕES DOS AGENTES RELACIONADOS COM OP USUÁRIO UBS QUE NÃO SÃO RASCUNHO

        return {"notificacoes": notificacoes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notificações: {str(e)}")


#Valida Notificação
@ubs_router.patch("/notificacoes/{notificacao_id}/validar")
async def validar_notificacao(notificacao_id: int, usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).join(Agente, Notificacao.acs_ace_id == Agente.id).filter(Agente.ubs_atuante == usuario.ubs, Notificacao.id == notificacao_id, Notificacao.rascunho == False).first()

    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")

    notificacao.validado = True
    session.commit()

    return {"message":f"Notificação {notificacao_id} validada com sucesso!"}


# Complementar Notificação
@ubs_router.patch("/notificacoes/{notificacao_id}/complementar")
async def complementar_notificacao(notificacao_id: int, informacao_extra: str, usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).join(Agente, Notificacao.acs_ace_id == Agente.id).filter(Agente.ubs_atuante == usuario.ubs, Notificacao.id == notificacao_id, Notificacao.rascunho == False).first()  #RETORNA APENAS SE A NOTIFICAÇÃO PERTENCER A UBS LOGADA
    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")
    
    notificacao.descricao += f"\n[Complemento UBS]: {informacao_extra}"
    session.commit()
    return {"message": "Notificação complementada com sucesso!"}


#Rota para retornar o nome da ubs no qual o usuário logado pertence
@ubs_router.get("/dados_ubs")
async def dados_da_ubs(usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    dados_ubs = session.query(Dados_UBS).filter(Dados_UBS.id == usuario.ubs).first()  
    if not dados_ubs:
        raise HTTPException(status_code=404, detail="Dados da UBS não cadastrados no sistema.")
    
    return {"Dados da UBS": dados_ubs}

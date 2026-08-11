from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import create_session, somente_UBS
from models import Notificacao, UBS
from schemas import NotificacaoSchema
import datetime

ubs_router = APIRouter(prefix="/ubs", tags=["ubs"], dependencies=[Depends(somente_UBS)])

# Listar notificações associadas aos agentes da UBS logada
@ubs_router.get("/notificacoes")
async def listar_notificacoes_ubs(session: Session = Depends(create_session)):
    try:
        notificacoes = session.query(Notificacao).filter(Notificacao.rascunho == False).all()
        return {"notificacoes": notificacoes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notificações: {str(e)}")

# Validar Notificação
@ubs_router.patch("/notificacoes/{notificacao_id}/validar")
async def validar_notificacao(notificacao_id: int, session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id).first()
    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")
    
    notificacao.status = "VALIDADA"
    session.commit()
    return {"message": "Notificação validada com sucesso!"}

# Encaminhar Notificação
@ubs_router.patch("/notificacoes/{notificacao_id}/encaminhar")
async def encaminhar_notificacao(notificacao_id: int, session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id).first()
    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")
    
    notificacao.status = "ENCAMINHADA"
    session.commit()
    return {"message": "Notificação encaminhada com sucesso!"}

# Complementar Notificação
@ubs_router.patch("/notificacoes/{notificacao_id}/complementar")
async def complementar_notificacao(notificacao_id: int, informacao_extra: str, session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id).first()
    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")
    
    notificacao.descricao += f"\n[Complemento UBS]: {informacao_extra}"
    session.commit()
    return {"message": "Notificação complementada com sucesso!"}

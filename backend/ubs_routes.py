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

@ubs_router.get("/notificacoes/{notificacao_id}")
async def obter_detalhes_notificacao(notificacao_id: int, session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id).first()
    
    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")
    
    # Recuperar URLs das mídias vinculadas
    medias = [media.url for media in notificacao.media_urls]
    
    return {
        "id": notificacao.id,
        "nome": notificacao.nome,
        "tipo_evento": notificacao.tipo_evento,
        "categoria": notificacao.categoria,
        "data_envio": notificacao.data_envio,
        "pessoas_animais_infectados_afetados": notificacao.pessoas_animais_infectados_afetados,
        "local_ocorrencia": notificacao.local_ocorrencia,
        "continuidade_situacao": notificacao.continuidade_situacao,
        "descricao": notificacao.descricao,
        "status": notificacao.status,
        "acs_ace_id": notificacao.acs_ace_id,
        "medias": medias
    }
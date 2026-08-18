from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import create_session, somente_CM, get_usuario
from security import get_hashed_password
from models import Notificacao, Coordenador_Municipal
from schemas import CMSchema

cm_router = APIRouter(prefix="/cm", tags=["cm"], dependencies=[Depends(somente_CM)])


#Criaçaõ de conta CM
@cm_router.post("/criar_conta")
async def criar_cm(cm_schema : CMSchema, session : Session = Depends(create_session)): 
    cm = session.query(Coordenador_Municipal).filter(Coordenador_Municipal.email == cm_schema.email).first()

    if cm:
        raise HTTPException(status_code=400, detail="UBS já cadastrada no sistema!")
    
    senha_hashed = get_hashed_password(cm_schema.senha)
    cm_novo = Coordenador_Municipal(cm_schema.email, senha_hashed, cm_schema.nome, cm_schema.municipio)
    session.add(cm_novo)
    session.commit()
    
    return {"message": "Coordenador Municipal criado com sucesso!"}


#Lista notificações da região
@cm_router.get("/listar_notificacoes")
async def listar_notificacoes_ubs(usuario = Depends(get_usuario), session : Session = Depends(create_session)):
    try:
        notificacoes = session.query(Notificacao).filter(Notificacao.municipio == usuario.municipio, Notificacao.validado == True).all()      #RETORNA TODAS AS NOTIFICAÇÕOS DA REGIÃO QUE FORAM VALIDADAS

        return {"notificacoes": notificacoes, "quantidade": len(notificacoes)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notificações: {str(e)}")


#Alteração dos status de uma notificação
@cm_router.patch("/notificacoes/{notificacao_id}/status_recebido")
async def validar_notificacao(notificacao_id: int, usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id, Notificacao.municipio == usuario.municipio, Notificacao.validado == True).first()

    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")

    notificacao.status = "RECEBIDO"
    session.commit()

    return {"message":"Notificação recebida!"}


@cm_router.patch("/notificacoes/{notificacao_id}/status_em_investigacao")
async def validar_notificacao(notificacao_id: int, usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id, Notificacao.municipio == usuario.municipio, Notificacao.validado == True).first()

    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")

    notificacao.status = "EM INVESTIGAÇÃO"
    session.commit()

    return {"message":"Notificação em investigação!"}


@cm_router.patch("/notificacoes/{notificacao_id}/status_confirmado")
async def validar_notificacao(notificacao_id: int, usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id, Notificacao.municipio == usuario.municipio, Notificacao.validado == True).first()

    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")

    notificacao.status = "CONFIRMADO"
    session.commit()

    return {"message":"Notificação confirmada!"}


@cm_router.patch("/notificacoes/{notificacao_id}/status_descartado")
async def validar_notificacao(notificacao_id: int, usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id, Notificacao.municipio == usuario.municipio, Notificacao.validado == True).first()

    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")

    notificacao.status = "DESCARTADO"
    session.commit()

    return {"message":"Notificação descartada!"}


@cm_router.patch("/notificacoes/{notificacao_id}/status_encerrado")
async def validar_notificacao(notificacao_id: int, usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    notificacao = session.query(Notificacao).filter(Notificacao.id == notificacao_id, Notificacao.municipio == usuario.municipio, Notificacao.validado == True).first()

    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada.")

    notificacao.status = "ENCERRADO"
    session.commit()

    return {"message":"Notificação encerrada!"}

# Adicionar em cm_router.py

# Métricas resumidas do município
@cm_router.get("/dashboard_stats")
async def obter_estatisticas(usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    try:
        total = session.query(Notificacao).filter(Notificacao.municipio == usuario.municipio, Notificacao.validado == True).count()
        investigacao = session.query(Notificacao).filter(Notificacao.municipio == usuario.municipio, Notificacao.validado == True, Notificacao.status == "EM INVESTIGAÇÃO").count()
        confirmados = session.query(Notificacao).filter(Notificacao.municipio == usuario.municipio, Notificacao.validado == True, Notificacao.status == "CONFIRMADO").count()
        
        return {
            "total": total,
            "em_investigacao": investigacao,
            "confirmados": confirmados
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar estatísticas: {str(e)}")

@cm_router.get("/exportar_relatorio")
async def exportar_relatorio(usuario = Depends(get_usuario), session: Session = Depends(create_session)):
    try:
        notificacoes = session.query(Notificacao).filter(
            Notificacao.municipio == usuario.municipio, 
            Notificacao.validado == True
        ).all()
        
        relatorio = [
            {
                "id": n.id,
                "categoria": getattr(n, 'categoria', 'N/A'),
                "tipo": getattr(n, 'tipo', 'N/A'),
                "status": n.status,
                "data": getattr(n, 'data_criacao', 'N/A'),
                "local": getattr(n, 'local', 'N/A')
            }
            for n in notificacoes
        ]
        
        return {"relatorio": relatorio, "municipio": usuario.municipio}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {str(e)}")


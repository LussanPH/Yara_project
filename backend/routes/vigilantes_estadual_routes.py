from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import create_session, get_usuario, somente_VE
from security import get_hashed_password
from models import Notificacao, Vigilancia_Estadual
from schemas import VigilanteEstadualSchema


ve_router = APIRouter(prefix="/ve", tags=['ve'], dependencies=[Depends(somente_VE)])


@ve_router.post('/criar_conta_vr')
async def criar_ve(ve_schema : VigilanteEstadualSchema, session : Session = Depends(create_session)):
    ve = session.query(Vigilancia_Estadual).filter(Vigilancia_Estadual.cpf == ve_schema.cpf).first()

    if ve:
        raise HTTPException(status_code=400, detail='Vigilante Estadual já existente no sistema!')

    senha_hashed = get_hashed_password(ve_schema.senha)
    ve_novo = Vigilancia_Estadual(ve_schema.cpf, senha_hashed, ve_schema.nome)
    session.add(ve_novo)
    session.commit()

    return {'message' : 'Vigilante Estadual criado com sucesso!'}


@ve_router.get('/notificacoes')
async def listar_notificacoes(session : Session = Depends(create_session)):
    try:
        notificacoes = session.query(Notificacao).all()

        return{
            "Notificações" : notificacoes,
            "Quantidade" : len(notificacoes)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao retornar notificações: {e}")
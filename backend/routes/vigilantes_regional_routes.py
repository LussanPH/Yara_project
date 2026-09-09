from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import create_session, somente_UBS, get_usuario, somente_VR
from security import get_hashed_password
from models import Notificacao, Vigilancia_Regional, Superintendencias_Ceara
from schemas import VigilanteRegionalSchema



vr_router = APIRouter(prefix='/vr', tags=['vr'], dependencies=[])


@vr_router.post('/criar_conta_vr')
async def criar_vr(vr_schema : VigilanteRegionalSchema, session : Session = Depends(create_session)):
    vr = session.query(Vigilancia_Regional).filter(Vigilancia_Regional.cpf == vr_schema.cpf)

    if vr:
        raise HTTPException(status_code=400, detail="Vigilante Regional já cadastrado no sistema!")

    senha_hashed = get_hashed_password(vr_schema.senha)
    vr_novo = Vigilancia_Regional(vr_schema.cpf, senha_hashed, vr_schema.nome, vr_schema.superintendencia)
    session.add(vr_novo)
    session.commit()

    return {'message': 'Vigilante Regional cadastrado com sucesso!'}


@vr_router.get('/notificacoes')
async def listar_notificacoes(usuario = Depends(get_usuario), session : Session = Depends(create_session)):
    try:
        resultados = session.query(Notificacao, Superintendencias_Ceara).join(Superintendencias_Ceara, Notificacao.municipio).filter(Superintendencias_Ceara.id == usuario.superintendencia, Notificacao.rascunho == False).all()
        
    
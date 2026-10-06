from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from dependencies import create_session, get_usuario, somente_VR
from security import get_hashed_password
from models import Notificacao, Vigilancia_Regional, Superintendencias_Ceara, Coordenador_Municipal
from schemas import VigilanteRegionalSchema, CMSchema



vr_router = APIRouter(prefix='/vr', tags=['vr'], dependencies=[Depends(somente_VR)])



#Criação de conta CM
@vr_router.post("/criar_conta_coordenador")
async def criar_cm(cm_schema : CMSchema, session : Session = Depends(create_session)): 
    cm = session.query(Coordenador_Municipal).filter(Coordenador_Municipal.cpf == cm_schema.cpf).first()

    if cm:
        raise HTTPException(status_code=400, detail="Coordenador já cadastrado no sistema!")
    
    senha_hashed = get_hashed_password(cm_schema.senha)
    cm_novo = Coordenador_Municipal(cm_schema.cpf, senha_hashed, cm_schema.nome, cm_schema.municipio)
    session.add(cm_novo)
    session.commit()
    
    return {"message": "Coordenador Municipal criado com sucesso!"}



@vr_router.get('/notificacoes')
async def listar_notificacoes(  
    usuario=Depends(get_usuario),
    session: Session = Depends(create_session),
):
    municipios = (
        select(func.jsonb_array_elements_text(Superintendencias_Ceara.municipio))
        .select_from(Vigilancia_Regional)
        .join(
            Superintendencias_Ceara,
            Vigilancia_Regional.superintendencia == Superintendencias_Ceara.id,
        )
        .where(Vigilancia_Regional.id == usuario.id)
        .scalar_subquery()
    )

    notificacoes = session.scalars(
        select(Notificacao)
        .where(Notificacao.municipio.in_(municipios))
        .where(Notificacao.rascunho.is_(False))
    ).all()

    return {"notificacoes": notificacoes}
    

@vr_router.get('/dados_superintendencia')
async def dados_superintendencia(usuario = Depends(get_usuario), session : Session = Depends(create_session)):
    try:
        dados_superintendencia = session.query(Superintendencias_Ceara).filter(Superintendencias_Ceara.id == usuario.superintendencia).first()
        
        if not dados_superintendencia:
            raise HTTPException(status_code=400, detail='Superintendência do usuário não encontrada.')
        
        return {'Dados da Superintendência' : dados_superintendencia}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao tentar encontrar dados da superintendência: {e}')

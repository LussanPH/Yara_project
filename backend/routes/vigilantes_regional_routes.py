from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from dependencies import create_session, somente_UBS, get_usuario, somente_VR
from security import get_hashed_password
from models import Notificacao, Vigilancia_Regional, Superintendencias_Ceara
from schemas import VigilanteRegionalSchema



vr_router = APIRouter(prefix='/vr', tags=['vr'], dependencies=[Depends(somente_VR)])


@vr_router.post('/criar_conta_vr')
async def criar_vr(vr_schema : VigilanteRegionalSchema, session : Session = Depends(create_session)):
    vr = session.query(Vigilancia_Regional).filter(Vigilancia_Regional.cpf == vr_schema.cpf).first()

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
        municipio_superintendencia = func.json_each(Superintendencias_Ceara.municipio).table_valued("value")

        notificacoes = (
            session.query(Notificacao)
            .select_from(Vigilancia_Regional)
            .join(Superintendencias_Ceara, Vigilancia_Regional.superintendencia == Superintendencias_Ceara.id)
            .join(municipio_superintendencia, Notificacao.municipio == municipio_superintendencia.c.value)
            .filter(Vigilancia_Regional.id == usuario.id, Notificacao.rascunho == False)
            .all()
        )
        """
        notificacoes = []

        for notificacao, superintendencia in resultados:
            notificacoes.append({
                "id": notificacao.id,
                "nome": notificacao.nome,
                "tipo_evento": notificacao.tipo_evento,
                "categoria": notificacao.categoria,
                "data_envio": notificacao.data_envio,
                "pessoas_animais_infectados_afetados": notificacao.pessoas_animais_infectados_afetados,
                "local_ocorrencia": notificacao.local_ocorrencia,
                "continuidade_situacao": notificacao.continuidade_situacao,
                "descricao": notificacao.descricao,
                "acs_ace_id": notificacao.acs_ace_id,
                "status": notificacao.status,
                "rascunho": notificacao.rascunho,
            })
        """
        return {'notificacoes' : notificacoes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notificações: {e}")


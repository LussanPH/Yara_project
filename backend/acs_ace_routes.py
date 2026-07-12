from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from dependencies import create_session, token_verification, somente_Agente, get_usuario
from schemas import NotificacaoSchema, AgenteSchema
from models import Agente, UBS, Notificacao
from sqlalchemy.orm import Session
from security import get_hashed_password
import datetime
from config import GROK_API_KEY
from groq import Groq


acs_ace_router = APIRouter(prefix="/agentes", tags=["Agentes"], dependencies=[Depends(somente_Agente)])
client = Groq(api_key=GROK_API_KEY)


#Lista as notificações de um agente com base em quem está logado
@acs_ace_router.get("/listar_notificacoes")
async def listar_notificacoes(session : Session = Depends(create_session), usuario = Depends(get_usuario)):
    notificacoes = session.query(Notificacao).filter(Notificacao.acs_ace_id == usuario.id).all()

    return {
        "Notificações" : notificacoes
    }


#Endpoint para transcrição do áudio enviado pelo agente
@acs_ace_router.post("/transcricao_audio")
async def transcricao_audio(audio:UploadFile = File(...)):
    if not audio.filename:
        raise HTTPException(status_code=400, detail='Nenhum áudio encontrado.')
    
    try:
        audio_bytes = await audio.read()

        transcricao = client.audio.transcriptions.create(
            file = (audio.filename, audio_bytes),
            model = "whisper-large-v3",
            response_format='json',
            language='pt'
        )

        return {'texto_transcrito': transcricao.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro na transcrição: {str(e)}')


#Criação de uma notificação com base no agente que está logado
@acs_ace_router.post("/criar_notificacao")
async def criar_notificacao(notificacao : NotificacaoSchema, session : Session = Depends(create_session), usuario = Depends(get_usuario)):
    data_hora = datetime.datetime.now()
    data_hora = data_hora.strftime("%d/%m/%Y %H:%M")
    
    notificacao_nova = Notificacao(notificacao.nome,
                              notificacao.tipo_evento,
                              notificacao.categoria,  
                              notificacao.data_envio, 
                              notificacao.pessoas_animais_infectados_afetados, 
                              notificacao.local_ocorrencia, 
                              notificacao.meio_identificacao, 
                              notificacao.continuidade_situacao, 
                              notificacao.descricao, 
                              usuario.id, 
                              notificacao.status, 
                              notificacao.rascunho)
    
    session.add(notificacao_nova)
    session.commit()

    return {
        "response" : f"Notificação {notificacao_nova.nome} com id {notificacao_nova.id} Criada com sucesso!"
    }



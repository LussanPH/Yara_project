from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from dependencies import create_session, token_verification, somente_Agente, get_usuario
from models import Agente, UBS, Notificacao
from typing import List, Annotated
from sqlalchemy.orm import Session
from security import get_hashed_password
import datetime
from config import GROK_API_KEY, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD_NAME
from groq import Groq
import cloudinary
import cloudinary.uploader


cloudinary.config(
    cloud_name = CLOUDINARY_CLOUD_NAME,
    api_key = CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET,
    secure = True
)


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
async def transcricao_audio(audio : UploadFile = File(...)):
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
async def criar_notificacao(nome : str = Form(...), 
                            tipo_evento : str = Form(...),
                            categoria : str = Form(...),
                            pessoas_animais_infectados_afetados : int = Form(...),
                            local_ocorrencia : str = Form(...),
                            continuidade_situacao : str = Form(...), 
                            descricao : str = Form(...),
                            medias : list[UploadFile] = File(...),
                            status : str = Form(...),
                            rascunho : bool = Form(...), 
                            session : Session = Depends(create_session), usuario = Depends(get_usuario)):
    
    data_envio = datetime.datetime.now()

    urls_media = []

    for media in medias:
        if media.filename:
            try:
                resultado = cloudinary.uploader.upload(media.file)

                url_final = resultado.get("secure_url")

                urls_media.append(url_final)

            except Exception as e:
                return {"Erro":f"Falha ao enviar imagem {media.filename}: {str(e)}"}


    
    
    notificacao_nova = Notificacao(nome,
                              tipo_evento,
                              categoria,  
                              data_envio, 
                              pessoas_animais_infectados_afetados, 
                              local_ocorrencia,  
                              continuidade_situacao, 
                              descricao, 
                              urls_media,
                              usuario.id, 
                              status, 
                              rascunho)
    
    session.add(notificacao_nova)
    session.commit()

    return {
        "response" : f"Notificação {notificacao_nova.nome} com id {notificacao_nova.id} Criada com sucesso!"
    }



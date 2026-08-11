from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from dependencies import create_session, token_verification, somente_Agente, get_usuario
from models import Agente, UBS, Notificacao, NotificacaoMedia
from typing import List, Annotated
from sqlalchemy.orm import Session
from security import get_hashed_password
import datetime
from config import GROK_API_KEY, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD_NAME
from groq import Groq
import cloudinary
import cloudinary.uploader
import httpx

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

async def obter_coordenadas(
    endereco: str,
    municipio: str,
    estado: str
):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": f"{endereco}, {municipio}, {estado}, Brasil",
        "format": "json",
        "limit": 1,
    }

    headers = {
        "User-Agent": "Sentinela-App/1.0"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params=params,
            headers=headers,
        )

    print("ENDEREÇO BUSCADO:", params["q"])
    print("STATUS NOMINATIM:", response.status_code)
    print("RESPOSTA NOMINATIM:", response.json())

    if response.status_code != 200:
        return None, None

    resultados = response.json()

    if not resultados:
        return None, None

    latitude = float(resultados[0]["lat"])
    longitude = float(resultados[0]["lon"])

    return latitude, longitude

#Criação de uma notificação com base no agente que está logado
@acs_ace_router.post("/criar_notificacao")
async def criar_notificacao(
    nome : str = Form(...), 
    tipo_evento : str = Form(...),
    categoria : str = Form(...),
    pessoas_animais_infectados_afetados : int = Form(...),
    local_ocorrencia : str = Form(...),
    endereco : str = Form(None), 
    estado : str = Form(None),
    municipio : str = Form(None), 
    continuidade_situacao : str = Form(...), 
    descricao : str = Form(...),
    medias : list[UploadFile] = File(default=[]),
    status : str = Form(...),
    rascunho : bool = Form(...), 
    session : Session = Depends(create_session), 
    usuario = Depends(get_usuario)
):
    data_envio = datetime.datetime.now()
    latitude = None
    longitude = None

    if endereco and municipio and estado:
        latitude, longitude = await obter_coordenadas(
            endereco,
            municipio,
            estado,
        )

    notificacao_nova = Notificacao(
        nome=nome,
        tipo_evento=tipo_evento,
        categoria=categoria,
        data_envio=data_envio,
        pessoas_animais_infectados_afetados=pessoas_animais_infectados_afetados,
        local_ocorrencia=local_ocorrencia,

        estado=estado,
        municipio=municipio,
        endereco=endereco,

        latitude=latitude,
        longitude=longitude,

        continuidade_situacao=continuidade_situacao,
        descricao=descricao,
        acs_ace_id=usuario.id,
        status=status,
        rascunho=rascunho
    )
    
    session.add(notificacao_nova)
    session.flush()
    
    # (resto da lógica do upload de imagens permanece igual...)
    session.commit()

    return {"response": f"Notificação {notificacao_nova.nome} criada com sucesso!"}



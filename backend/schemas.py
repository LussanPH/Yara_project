from pydantic import BaseModel
from typing import Optional, List
from fastapi import UploadFile
import datetime

#Schema dos Agentes ACS/ACE
class AgenteSchema(BaseModel):
    senha : str
    cargo : str
    nome : str
    ubs_atuante : int
    email : str

    class Config:
        from_attributes = True

#Schema da conta UBS
class UBSSchema(BaseModel):
    senha : str
    ubs : int
    nome : str
    municipio : str
    email : str
    
    class Config:
        from_attributes = True

#Schema das notificações a serem postadas pelos agentes acs/ace
class NotificacaoSchema(BaseModel):
    nome : str
    tipo_evento : str
    categoria : str
    data_envio : datetime.datetime
    pessoas_animais_infectados_afetados : int
    local_ocorrencia : str
    continuidade_situacao : str
    descricao : str
    status : str
    rascunho : bool
    
    class Config:
        from_attributes = True

#Schema dos dados de uma UBS
class DadosUBSSchema(BaseModel):
    nome: str
    municipio: str
    estado: str

    class Config:
        from_attributes = True
    
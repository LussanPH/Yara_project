from pydantic import BaseModel
from typing import Optional
import datetime

class AgenteSchema(BaseModel):
    senha : str
    cargo : str
    nome : str
    ubs_atuante : int
    email : str

    class Config:
        from_attributes = True

class UBSSchema(BaseModel):
    senha : str
    ubs : str
    nome : str
    municipio : str
    email : str
    
    class Config:
        from_attributes = True

class NotificacaoSchema(BaseModel):
    nome : str
    tipo_evento : str
    categoria : str
    data_envio : datetime.datetime
    pessoas_animais_infectados_afetados : int
    local_ocorrencia : str
    meio_identificacao : str
    continuidade_situacao : str
    descricao : str
    acs_ace_id : int
    status : str
    rascunho : bool
    
    class Config:
        from_attributes = True

    
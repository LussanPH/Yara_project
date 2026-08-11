from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, MetaData
from sqlalchemy.orm import declarative_base, relationship

convention = {
    "ix": "ix_%(column_0_label)s",                                 
    "uq": "uq_%(table_name)s_%(column_0_name)s",                        
    "ck": "ck_%(table_name)s_%(constraint_name)s",                      
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s", 
    "pk": "pk_%(table_name)s"                                           
}

metadata = MetaData(naming_convention=convention)

db = create_engine("sqlite:///banco.db", echo=True)
Base = declarative_base(metadata=metadata)

class Agente(Base):
    __tablename__ = "Agentes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    senha = Column("senha", String)
    cargo = Column("cargo", String)
    nome = Column("nome", String)
    ubs_atuante = Column("ubs_atuante", ForeignKey("Dados_UBS.id"))
    email = Column("email", String)

    def __init__(self, senha, cargo, nome, ubs_atuante, email):
        self.senha = senha
        self.cargo = cargo
        self.nome = nome
        self.ubs_atuante = ubs_atuante
        self.email = email


class UBS(Base): 
    __tablename__ = "UBS"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    senha = Column("senha", String)
    nome = Column("nome", String)
    ubs = Column("ubs", ForeignKey("Dados_UBS.id"))
    municipio = Column("municipio", ForeignKey("Dados_UBS.municipio"))
    email = Column("email", String)

    def __init__(self, senha, nome, ubs, municipio, email):
        self.senha = senha
        self.nome = nome
        self.ubs = ubs
        self.municipio = municipio
        self.email = email


class Notificacao(Base):
    __tablename__ = "Notificaçoes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    tipo_evento = Column("tipo_evento", String)
    categoria = Column("categoria", String)
    data_envio = Column("data_envio", DateTime)
    pessoas_animais_infectados_afetados = Column("pessoas_animais_infectados_afetados", Integer)
    local_ocorrencia = Column("local_ocorrencia", String)
    estado = Column("estado", String, nullable=True)
    municipio = Column("municipio", String, nullable=True)
    endereco = Column("endereco", String, nullable=True) 
    latitude = Column("latitude", Float, nullable=True)
    longitude = Column("longitude", Float, nullable=True)
    
    continuidade_situacao = Column("continuidade_situacao", String)
    descricao = Column("descricao", String)
    media_urls = relationship("NotificacaoMedia", back_populates="notificacao")
    acs_ace_id = Column("acs_ace_id", ForeignKey("Agentes.id"))
    status = Column("status", String)
    rascunho = Column("rascunho", Boolean)

    def __init__(
        self,
        nome,
        tipo_evento,
        categoria,
        data_envio,
        pessoas_animais_infectados_afetados,
        local_ocorrencia,
        continuidade_situacao,
        descricao,
        acs_ace_id,
        status="EM ANDAMENTO",
        rascunho=True,
        estado=None,
        municipio=None,
        endereco=None,
        latitude=None,
        longitude=None
    ):
        self.nome = nome
        self.tipo_evento = tipo_evento
        self.categoria = categoria
        self.data_envio = data_envio
        self.pessoas_animais_infectados_afetados = pessoas_animais_infectados_afetados
        self.local_ocorrencia = local_ocorrencia

        self.estado = estado
        self.municipio = municipio
        self.endereco = endereco

        self.latitude = latitude
        self.longitude = longitude

        self.continuidade_situacao = continuidade_situacao
        self.descricao = descricao
        self.acs_ace_id = acs_ace_id
        self.status = status
        self.rascunho = rascunho


class NotificacaoMedia(Base):
    __tablename__ = "Notificacoes_Media"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    url = Column("url", String)
    notificacao_id = Column("notificacao_id", ForeignKey("Notificaçoes.id"))

    notificacao = relationship("Notificacao", back_populates="media_urls")

    def __init__(self, url, notificacao_id):
        self.url = url
        self.notificacao_id = notificacao_id


class Dados_UBS(Base):
    __tablename__ = "Dados_UBS"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    municipio = Column("municipio", String, nullable=False)
    estado = Column("estado", String, nullable=False)

    def __init__(self, nome, municipio, estado):
        self.nome = nome
        self.municipio = municipio
        self.estado = estado



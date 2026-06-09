from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base

db = create_engine("sqlite:///banco.db", echo=True)
Base = declarative_base()

class Agente(Base):
    __tablename__ = "Agentes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    senha = Column("senha", String)
    cargo = Column("cargo", String)
    nome = Column("nome", String)
    ubs_atuante = Column("ubs_atuante", ForeignKey("UBS.id"))
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
    ubs = Column("ubs", String)
    municipio = Column("municipio", String)
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
    meio_identificacao = Column("meio_identificacao", String)
    continuidade_situacao = Column("continuidade_situacao", String)
    descricao = Column("descricao", String)
    acs_ace_id = Column("acs_ace_id", ForeignKey("Agentes.id"))
    status = Column("status", String)
    rascunho = Column("rascunho", Boolean)

    def __init__(self, nome, tipo_evento, categoria, data_envio, pessoas_animais_infectados_afetados, local_ocorrencia, meio_identificacao, continuidade_situacao, descricao, acs_ace_id, status="EM ANDAMENTO", rascunho=True):
        self.nome = nome
        self.tipo_evento = tipo_evento
        self.categoria = categoria
        self.data_envio = data_envio
        self.pessoas_animais_infectados_afetados = pessoas_animais_infectados_afetados
        self.local_ocorrencia = local_ocorrencia
        self.meio_identificacao = meio_identificacao
        self.continuidade_situacao = continuidade_situacao
        self.descricao = descricao
        self.acs_ace_id = acs_ace_id
        self.status = status
        self.rascunho = rascunho
        
    

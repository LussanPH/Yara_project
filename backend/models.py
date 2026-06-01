from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base

db = create_engine("sqlite:///banco.bd", echo=True)
Base = declarative_base()

class Agente(Base):
    __tablename__ = "Agentes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    senha = Column("senha", String)
    cargo = Column("cargo", String)
    nome = Column("nome", String)
    ubs_atuante = Column("usb_atuante", ForeignKey("UBS.id"))
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
    

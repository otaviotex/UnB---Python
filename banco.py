from sqlalchemy import create_engine, Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import hashlib

db = create_engine("sqlite:///agendaut.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()

class Medico(Base):
    __tablename__ = "medicos"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    sobrenome = Column("sobrenome", String)
    idade = Column("idade", Integer)
    genero = Column("genero", String)
    crm = Column("CRM", String)
    especialidade = Column("especialidade", String)
    senha_hash = Column("senha", String)
    
    consultas = relationship("Consulta", back_populates="medico")
    
    def __init__(self, nome, sobrenome, idade, genero, crm, especialidade, senha):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade
        self.genero = genero
        self.crm = crm
        self.especialidade = especialidade
        self.senha_hash = hash_senha(senha)
        
    def verific_senha(self, senha_dig):
        return self.senha_hash == hash_senha(senha_dig)
    
class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    sobrenome = Column("sobrenome", String)
    idade = Column("idade", Integer)
    genero = Column("genero", String)
    numero = Column("numero", String)
    convenio = Column("convenio", String)
    email = Column("email", String)
    
    consultas = relationship("Consulta", back_populates="paciente")
    
    def __init__(self, nome, sobrenome, idade, genero, numero, convenio, email):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade
        self.genero = genero
        self.numero = numero
        self.convenio = convenio
        self.email = email
        
class Consulta(Base):
    __tablename__ = "consultas"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    data = Column("data", Date)
    hora = Column("hora", String)
    id_medico = Column("id_medico", Integer, ForeignKey("medicos.id"))
    id_paciente = Column("id_paciente", Integer, ForeignKey("pacientes.id"))
    
    medico = relationship("Medico", back_populates="consultas")
    paciente = relationship("Paciente", back_populates="consultas")
    
    def __init__(self, data, hora, medico, paciente):
        self.data = data
        self.hora = hora 
        self.medico = medico
        self.paciente = paciente
        

def criar_banco():
    Base.metadata.create_all(bind=db)
    print("Banco de dados criado com sucesso!")


from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from .db import engine

Base=declarative_base()

# Tabla asociativa
email_list_asociation=Table(
    "email_list",
    Base.metadata,
    Column("email_id", Integer, ForeignKey("emails.id")),
    Column("list_id", Integer, ForeignKey("lists.id"))
    )

class Email(Base):
    __tablename__="emails"
    id=Column(Integer, primary_key=True)
    email=Column(String, unique=True, nullable=False)
    name=Column(String, nullable=False)
    lists=relationship("List", secondary=email_list_asociation, back_populates="emails")

class List(Base):
    __tablename__="lists"
    id=Column(Integer, primary_key=True)
    name=Column(String, unique=True, nullable=False)
    emails=relationship("Email", secondary=email_list_asociation, back_populates="lists")

# Creación de la Base de Datos
Base.metadata.create_all(engine)
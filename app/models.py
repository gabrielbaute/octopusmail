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

class SMTPProfile(Base):
    __tablename__="smtp_profiles"
    id=Column(Integer, primary_key=True)
    service=Column(String, nullable=False) # Servicio SMTP: Google, Outlook, Yahoo
    port=Column(Integer, nullable=False)
    email=Column(String, nullable=False)
    app_pass=Column(String, nullable=False) # Contraseña o app pass)
    from_name=Column(String, nullable=False)

    def __repr__(self):
        return f"<SMTPProfile(service={self.service}, email={self.email})>"

# Creación de la Base de Datos
Base.metadata.create_all(engine)
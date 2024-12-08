from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from flask_login import UserMixin
from .db import engine

Base=declarative_base()

# Tabla asociativa
email_list_asociation=Table(
    "email_list",
    Base.metadata,
    Column("email_id", Integer, ForeignKey("emails.id")),
    Column("list_id", Integer, ForeignKey("lists.id"))
    )

class Role(Base):
    __tablename__="roles"
    id=Column(Integer, primary_key=True)
    name=Column(String, unique=True, nullable=False)
    users=relationship("User", back_populates="role")

class User(UserMixin, Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True)
    username=Column(String, unique=True, nullable=False)
    email=Column(String, unique=True, nullable=False)
    password_hash=Column(String, nullable=False)
    role_id=Column(Integer, ForeignKey('roles.id'))
    role=relationship("Role", back_populates="users")

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Email(Base):
    __tablename__="emails"
    id=Column(Integer, primary_key=True)
    email=Column(String, unique=True, nullable=False)
    name=Column(String, nullable=False)
    lists=relationship("List", secondary=email_list_asociation, back_populates="emails")
    sent_count=Column(Integer, default=0)
    open_count=Column(Integer, default=0)
    send_dates=relationship("SendDate", back_populates="email")

class List(Base):
    __tablename__="lists"
    id=Column(Integer, primary_key=True)
    name=Column(String, unique=True, nullable=False)
    emails=relationship("Email", secondary=email_list_asociation, back_populates="lists")
    send_count=Column(Integer, default=0)
    send_dates=relationship("SendDate", back_populates="list")

class SendDate(Base):
    __tablename__="send_dates"
    id=Column(Integer, primary_key=True)
    email_id=Column(Integer, ForeignKey("emails.id"))
    list_id=Column(Integer, ForeignKey("lists.id"))
    timestamp=Column(DateTime, default=datetime.utcnow)
    email=relationship("Email", back_populates="send_dates")
    list=relationship("List", back_populates="send_dates")

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
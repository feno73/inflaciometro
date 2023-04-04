from db import db
from peewee import *
import datetime


class BaseModel(Model):
    fecha_creacion = DateTimeField(default=datetime.datetime.now)
    fecha_actualizacion = DateTimeField(default=datetime.datetime.now)

    class Meta:
        assert isinstance(db, object)
        database = db


class Marca(BaseModel):
    nombre = CharField(unique=True)


class Categoria(BaseModel):
    nombre = CharField()


class Producto(BaseModel):
    nombre = CharField()
    precio = DecimalField()
    marca = ForeignKeyField(Marca, backref='productos')
    categoria = ForeignKeyField(Categoria, backref='productos')
    supermercado = CharField()
    canasta_basica = BooleanField()


class Seccion(BaseModel):
    nombre = CharField()
    url = CharField()
    supermercado = CharField()
    categoria = ForeignKeyField(Categoria, backref='secciones')


# simple utility function to create tables
#db.create_tables([Seccion])

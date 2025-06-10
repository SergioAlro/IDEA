from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import random
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'questions.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PreguntaDB(Base):
    __tablename__ = 'preguntas'

    id = Column(Integer, primary_key=True, index=True)
    pregunta = Column(String, nullable=False)
    opcion_a = Column(String, nullable=False)
    opcion_b = Column(String, nullable=False)
    opcion_c = Column(String, nullable=False)
    opcion_d = Column(String, nullable=False)
    resultado = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)


class Pregunta(BaseModel):
    pregunta: str
    opcion_a: str
    opcion_b: str
    opcion_c: str
    opcion_d: str
    resultado: str


class PreguntaOut(Pregunta):
    id: int

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.post("/preguntas/", response_model=PreguntaOut)
def crear_pregunta(pregunta: Pregunta, db: Session = Depends(get_db)):
    registro = PreguntaDB(**pregunta.dict())
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro


@app.get("/preguntas/", response_model=List[PreguntaOut])
def listar_preguntas(db: Session = Depends(get_db)):
    return db.query(PreguntaDB).all()


@app.get("/preguntas/{pregunta_id}", response_model=PreguntaOut)
def obtener_pregunta(pregunta_id: int, db: Session = Depends(get_db)):
    registro = db.query(PreguntaDB).get(pregunta_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return registro


@app.put("/preguntas/{pregunta_id}", response_model=PreguntaOut)
def actualizar_pregunta(pregunta_id: int, pregunta: Pregunta, db: Session = Depends(get_db)):
    registro = db.query(PreguntaDB).get(pregunta_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    for campo, valor in pregunta.dict().items():
        setattr(registro, campo, valor)
    db.commit()
    db.refresh(registro)
    return registro


@app.delete("/preguntas/{pregunta_id}")
def eliminar_pregunta(pregunta_id: int, db: Session = Depends(get_db)):
    registro = db.query(PreguntaDB).get(pregunta_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    db.delete(registro)
    db.commit()
    return {"detail": "Pregunta eliminada"}


@app.get("/generar_test/", response_model=List[PreguntaOut])
def generar_test(preguntas: int, db: Session = Depends(get_db)):
    registros = db.query(PreguntaDB).all()
    if preguntas > len(registros):
        raise HTTPException(status_code=400, detail="No hay suficientes preguntas")
    seleccion = random.sample(registros, preguntas)
    return seleccion

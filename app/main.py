from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import engine
from sqlalchemy.orm import Session, joinedload
from app.database import Base, engine, SessionLocal  
from app import models, schemas
from app.enums import Estado
from app.schemas import ZonaCreate, PatineteCreate

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/zonas/", response_model=schemas.ZonaOut)
def crear_zona(zona: ZonaCreate, db: Session = Depends(get_db)):
    nueva = models.Zona(**zona.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@app.post("/patinetes/", response_model=schemas.PatineteOut)
def crear_patinete(p: schemas.PatineteCreate, db: Session = Depends(get_db)):
    patinete = models.Patinete(
        **p.model_dump(exclude={"estado"}), 
        estado=p.estado if p.estado else Estado.disponible)
    db.add(patinete)
    db.commit()
    db.refresh(patinete)
    return patinete

@app.get("/patinetes/", response_model=list[schemas.PatineteOut])
def obtener_patinetes(db: Session = Depends(get_db)):
    return db.query(models.Patinete).all()

@app.get("/zonas/", response_model=list[schemas.ZonaConPatinetes])
def obtener_zonas_con_patinetes(db: Session = Depends(get_db)):
    zonas = db.query(models.Zona).options(joinedload(models.Zona.patinetes)).all()
    return zonas

@app.post("/zonas/{zona_id}/mantenimiento", response_model=list[schemas.PatineteOut])
def mantenimiento(zona_id: int, db: Session = Depends(get_db)):
    patinetes = db.query(models.Patinete).filter(
        models.Patinete.zona_id == zona_id,
        models.Patinete.bateria < 15).all()

    for p in patinetes:
        p.estado = Estado.mantenimiento

    db.commit()

    return patinetes
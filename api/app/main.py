from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Panier

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AntiGaspi API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class PanierIn(BaseModel):
    commerce: str
    titre: str
    description: str = ""
    prix_initial: float = Field(gt=0)
    prix_reduit: float = Field(gt=0)
    quantite: int = Field(default=1, ge=0)


class PanierOut(PanierIn):
    id: int

    model_config = {"from_attributes": True}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/paniers", response_model=list[PanierOut])
def lister_paniers(db: Session = Depends(get_db)):
    return db.scalars(select(Panier).order_by(Panier.id.desc())).all()


@app.post("/paniers", response_model=PanierOut, status_code=201)
def creer_panier(data: PanierIn, db: Session = Depends(get_db)):
    if data.prix_reduit >= data.prix_initial:
        raise HTTPException(400, "Le prix réduit doit être inférieur au prix initial")
    panier = Panier(**data.model_dump())
    db.add(panier)
    db.commit()
    db.refresh(panier)
    return panier


@app.post("/paniers/{panier_id}/reserver", response_model=PanierOut)
def reserver_panier(panier_id: int, db: Session = Depends(get_db)):
    panier = db.get(Panier, panier_id)
    if panier is None:
        raise HTTPException(404, "Panier introuvable")
    if panier.quantite <= 0:
        raise HTTPException(400, "Plus de panier disponible")
    panier.quantite -= 1
    db.commit()
    db.refresh(panier)
    return panier


@app.delete("/paniers/{panier_id}", status_code=204)
def supprimer_panier(panier_id: int, db: Session = Depends(get_db)):
    panier = db.get(Panier, panier_id)
    if panier is None:
        raise HTTPException(404, "Panier introuvable")
    db.delete(panier)
    db.commit()
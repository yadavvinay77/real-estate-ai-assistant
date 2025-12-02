# app/router.py

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models.user_models import User
from app.models.rental_models import RentalSearch, RentalMatch
from app.models.repair_models import RepairRequest


router = APIRouter(prefix="/api")


@router.get("/users")
def list_users(db: Session = Depends(get_session)):
    return db.exec(select(User)).all()


@router.get("/rental-searches")
def list_rental_searches(db: Session = Depends(get_session)):
    return db.exec(select(RentalSearch)).all()


@router.get("/rental-matches")
def list_rental_matches(db: Session = Depends(get_session)):
    return db.exec(select(RentalMatch)).all()


@router.get("/repairs")
def list_repairs(db: Session = Depends(get_session)):
    return db.exec(select(RepairRequest)).all()

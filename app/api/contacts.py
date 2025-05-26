from typing import List
from datetime import date, datetime

from fastapi import APIRouter, Path, Query, Depends
from sqlalchemy.orm import Session

from app.models import contact_model as cm
from app.database.db import get_db
from app.crud import contact_crud

router = APIRouter(prefix='/api', tags=['contact'])


@router.post('/contact', response_model=cm.ResponseMessageModel)
async def create_contact(
        contact: cm.PostRequestModel,
        db: Session = Depends(get_db)
):
    await contact_crud.create_contact_crud(body=contact, db=db)
    return cm.ResponseMessageModel(message="Contact is added")


@router.get('/contacts', response_model=cm.GetAllResponseModel)
async def get_all_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return await contact_crud.get_contacts_crud(skip=skip, limit=limit, db=db)


@router.get('/contact/{contact_id}', response_model=cm.DBModel)
async def get_contact(
        contact_id: int = Path(),
        db: Session = Depends(get_db)
):
    return await contact_crud.get_contact_crud(contact_id=contact_id, db=db)


@router.put('/contact', response_model=cm.ResponseMessageModel)
async def update_contact(
        contact: cm.PutRequestModel,
        contact_id: int = Query(..., description="Identificator contact"),
        db: Session = Depends(get_db)
):
    await contact_crud.update_contact_crud(body=contact, contact_id=contact_id, db=db)
    return cm.ResponseMessageModel(message="Contact success updated")


@router.delete('/contact', response_model=cm.ResponseMessageModel)
async def delete_contact(
        contact_id: int = Query(..., description="Identificator contact"),
        db: Session = Depends(get_db)
):
    await contact_crud.remove_contact_crud(contact_id=contact_id, db=db)
    return cm.ResponseMessageModel(message="Contact success deleted")


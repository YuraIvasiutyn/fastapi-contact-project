from typing import List
from datetime import date, datetime

from fastapi import APIRouter, Path, Query, Depends
from sqlalchemy.orm import Session

from app.models import contact_model as cm
from app.models.db_models import User
from app.database.db import get_db
from app.crud import contact_crud
from app.auth.auth import Hash

router = APIRouter(prefix='/api', tags=['contact'])
hash_handler = Hash()


@router.post('/contact', response_model=cm.ResponseMessageModel)
async def create_contact(
        contact: cm.PostRequestModel,
        current_user: User = Depends(hash_handler.get_current_user),
        db: Session = Depends(get_db)
):
    await contact_crud.create_contact_crud(body=contact, user=current_user, db=db)
    return cm.ResponseMessageModel(message="Contact is added")


@router.get('/contacts', response_model=cm.GetAllResponseModel)
async def get_all_contacts(
        skip: int = 0,
        limit: int = 10,
        current_user: User = Depends(hash_handler.get_current_user),
        db: Session = Depends(get_db)
):
    return await contact_crud.get_contacts_crud(skip=skip, limit=limit, user=current_user, db=db)


@router.get('/contact/{contact_id}', response_model=cm.DBModel)
async def get_contact(
        contact_id: int = Path(),
        current_user: User = Depends(hash_handler.get_current_user),
        db: Session = Depends(get_db)
):
    return await contact_crud.get_contact_crud(contact_id=contact_id, user=current_user, db=db)


@router.put('/contact', response_model=cm.ResponseMessageModel)
async def update_contact(
        contact: cm.PutRequestModel,
        contact_id: int = Query(..., description="Identificator contact"),
        current_user: User = Depends(hash_handler.get_current_user),
        db: Session = Depends(get_db)
):
    await contact_crud.update_contact_crud(body=contact, contact_id=contact_id, user=current_user, db=db)
    return cm.ResponseMessageModel(message="Contact success updated")


@router.delete('/contact', response_model=cm.ResponseMessageModel)
async def delete_contact(
        contact_id: int = Query(..., description="Identificator contact"),
        current_user: User = Depends(hash_handler.get_current_user),
        db: Session = Depends(get_db)
):
    await contact_crud.remove_contact_crud(contact_id=contact_id, user=current_user, db=db)
    return cm.ResponseMessageModel(message="Contact success deleted")


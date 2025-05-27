from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi import HTTPException


from app.models.db_models import Contact, User
from app.models.contact_model import GetAllResponseModel, PostRequestModel, DBModel, PutRequestModel


async def create_contact_crud(body: PostRequestModel, user: User, db: Session) -> None:
    try:
        contact = Contact(
            first_name=body.first_name,
            last_name=body.last_name,
            email=body.email,
            phone_number=body.phone_number,
            birthday=body.birthday,
            user_id=user.id
        )
        db.add(contact)
        db.commit()
        db.refresh(contact)
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Problem with create contact. {e}")


async def get_contacts_crud(skip: int, limit: int, user: User, db: Session) -> GetAllResponseModel:
    contacts = db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()
    return GetAllResponseModel(
        contacts=[DBModel.from_orm(c) for c in contacts],
        skip=skip,
        limit=limit
)


async def get_contact_crud(contact_id: int, user: User, db: Session) -> DBModel:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact is None:
        raise HTTPException(status_code=404,
                            detail="Contact not found")

    return DBModel.from_orm(contact)


async def update_contact_crud(body: PutRequestModel, contact_id: int, user: User, db: Session) -> None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.updated_at = datetime.now()
        db.commit()
    else:
        raise HTTPException(status_code=404,
                            detail="Contact not found")


async def remove_contact_crud(contact_id: int, user: User, db: Session) -> None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    else:
        raise HTTPException(status_code=404,
                            detail="Contact not found")


async def found_contact(db: Session, first_name: str = None, last_name: str = None, email: str = None, user: User = None):
    """Додаткові функції до майбутнього використання в API"""
    filters = []
    if first_name:
        filters.append(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        filters.append(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        filters.append(Contact.email.ilike(f"%{email}%"))

    if not filters:
        return []

    result = db.query(Contact).filter(or_(*filters)).all()
    return result

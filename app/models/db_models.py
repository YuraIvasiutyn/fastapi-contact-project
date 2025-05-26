from sqlalchemy import Column, Integer, String, func
from sqlalchemy.sql.sqltypes import DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone_number = Column(String(12), nullable=False)
    birthday = Column(Date, nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())

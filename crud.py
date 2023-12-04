from sqlalchemy.orm import Session
from fastapi import HTTPException
import schemas
import models
import os

from database import SessionLocal


def create_document(db: Session, document: schemas.DocumentCreate):
    path = "documents/" + document.path
    db_document = models.DocumentDB(path=path, date=document.date)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def delete_document(db: Session, document_id: int):
    # Найти документ по его id
    document = db.query(models.DocumentDB).filter(models.DocumentDB.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Удалить запись из базы данных
    db.delete(document)
    db.commit()

    # Удалить файл с диска
    file_path = document.path
    try:
        os.remove(file_path)
    except OSError:
        raise HTTPException(status_code=500, detail="Failed to delete file from disk")

    return {"message": "Document deleted successfully"}


def create_document_text( id_doc: int, text: str):
    """
    Создайем новую запись в таблице Documents_text
    """
    with SessionLocal() as ses:
        document_text = models.DocumentTextDB(id_doc=id_doc, text=text)
        print("пишем в бд")
        ses.add(document_text)
        ses.commit()
    return document_text


def get_text(db: Session, document_id: int):
    # Найти документ по его id
    document = db.query(models.DocumentTextDB).filter(models.DocumentTextDB.id_doc == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Получить текст из найденного документа
    text = document.text

    return {"text": text}
from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI, UploadFile
from sqlalchemy.orm import Session
import os
import schemas
import models
import crud
from config import DOC_PATH
from database import SessionLocal, engine

from fastapi import HTTPException
from tasks import process_document

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/upload_doc')
async def up_file(file: UploadFile):
    """Здесь нужно загрузить файл"""
    file_contents = await file.read()

    file_path = os.path.join(DOC_PATH, file.filename)
    with open(file_path, "wb") as f:
        f.write(file_contents)

    with SessionLocal() as ses:
        db_document = models.DocumentDB(path=DOC_PATH + file.filename, date=datetime.now())
        ses.add(db_document)
        ses.commit()

    return {"messege": f"Файл {file.filename} добавлен в базу данных"}

"""
@app.post('/upload_doc/')
async def up_file(file: UploadFile, document: schemas.DocumentCreate = Depends()):

    db = SessionLocal()
    db_document = crud.create_document(db, document)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    document_id = db_document.id
    db.close()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    documents_dir = os.path.join(current_dir, "documents")

    file_path = os.path.join(documents_dir, f"{document_id}.jpg")
    print(f"Saved file as: {file_path}")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"message": "File uploaded successfully"}
"""

@app.delete("/doc_delete/{document_id}")
def doc_delete(document_id: int, db: Session = Depends(get_db)):

    file_path = f"documents/{document_id}.jpg"

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

    result = crud.delete_document(db, document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "Document deleted successfully"}


@app.post("/doc_analyse")
def doc_analyse(document_id: int):
    with SessionLocal() as ses:
        db_doc_path = ses.query(models.DocumentDB.path).filter(models.DocumentDB.id==int(document_id)).scalar()
        if db_doc_path is None:
            document_text = ses.query(models.DocumentTextDB).filter(models.DocumentTextDB.id_doc==int(document_id)).one_or_none()

    try:
    # Отправляем задачу в Celery
        document_path = db_doc_path
        result = process_document.delay(document_id, document_path)

        if result is None:
            raise HTTPException(status_code=500, detail="Failed to send task to Celery")
        return {"task_id": result.id}
    except Exception as e:
        print(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



@app.get("/get_text/{document_id}")
def get_document_text(document_id: int, db: Session = Depends(get_db)):
    result = crud.get_text(db, document_id)
    return result

if __name__ == '__main__':
    uvicorn.run(app)
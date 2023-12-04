from celery import Celery
from crud import create_document_text
import pytesseract
from PIL import Image

capp = Celery('myapp', broker='amqp://guest:guest@rabbit:5672//')

@capp.task
def process_document(document_id, document_path):
    try:
        print('вошли в таску')
        image = Image.open(document_path)
        text = pytesseract.image_to_string(image)
        create_document_text(id_doc=document_id, text=text)
    except Exception as e:
        print(f"Ошибка при анализе документа: {e}")


from sqlalchemy import Date, Column, ForeignKey, Integer, String

from database import Base


class DocumentDB(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, index=True)
    date = Column(Date)

class DocumentTextDB(Base):
    __tablename__ = "documents_text"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    id_doc = Column(Integer, ForeignKey("documents.id"))


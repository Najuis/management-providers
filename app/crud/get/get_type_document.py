from sqlalchemy.orm import Session
from app.models.model_type_document import TypeDocument
from fastapi import HTTPException

async def get_type_document_db(db: Session):
    try:
        type_document = db.query(TypeDocument).all()
        return [t.to_dict() for t in type_document]
    except HTTPException:
        raise   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

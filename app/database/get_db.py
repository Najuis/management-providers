from sqlalchemy.orm import sessionmaker
from app.database.core import engine

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    db = SessionLocal()
    try: 
        yield db

    finally:
        db.close()
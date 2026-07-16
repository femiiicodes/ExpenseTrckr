from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import app.models as models
from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL,connect_args={'check_same_thread':False})
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base = declarative_base()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
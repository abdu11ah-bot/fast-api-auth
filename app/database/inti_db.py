from app.database.base import Base
from app.database.connection import engine

from app.model.user import User

def init_db():
    Base.metadata.create_all(bind=engine)
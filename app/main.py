from fastapi import FastAPI

from app.database.base import Base
from app.database.connection import engine

# Important: import models before create_all()
from app.models.user import User

from app.router.auth import router as auth_router
from app.router.user import router as user_router


app = FastAPI(title="Forge API")


# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Forge API is running"}

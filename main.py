from fastapi import FastAPI, Depends
import models
from database import engine
from routers import mmt

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(mmt.router)
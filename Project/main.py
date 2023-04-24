from fastapi import FastAPI,Response,status,HTTPException,Depends,UploadFile,File
from sqlalchemy.orm import Session
from .database import get_db,engine
from typing import Annotated
from pydantic import BaseModel,EmailStr

from .Routers import Document_upload, Drivers,DriverLogin
from . import dotenv,models
from . External_API import phoneverification
from . import referal_code
app = FastAPI()

app.include_router(Document_upload.router)
app.include_router(Drivers.router)
app.include_router(DriverLogin.router)

models.Base.metadata.create_all(bind=engine)
# dotenv.Process.Abstract_api_key
# querstring = {
#     "api_key": f"{dotenv.Process.Abstract_api_key}",
#     "phone" : "+2348036699890"
# }
# phoneverification.PhoneVerify(querstring)
# @app.get("/")
# # def root():
    

# @app.get("/")
# def Root(db: Session = Depends(get_db)):
#     return {"hello":"world"}

referal_code.id_generator()
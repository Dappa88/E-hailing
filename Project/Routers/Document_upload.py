from typing import List
from fastapi import FastAPI,Response,status,HTTPException,Depends ,APIRouter,UploadFile,File

from ..database import engine,get_db
from .. import dotenv,oauth2,models,Schema

from sqlalchemy.orm import Session
from typing import Annotated
import cloudinary
from ..External_API import idanalyzer
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url



cloudinary.config(
  cloud_name = dotenv.Process.cloud_name,
  api_key = dotenv.Process.cloudapi_key,
  api_secret = dotenv.Process.cloudapi_secret,
  secure = "true"
)

# idanalyzer.ValidDocument()

router = APIRouter(tags=["Docs"],prefix="/upload")

@router.post("/{Driver_id}",status_code=status.HTTP_201_CREATED,response_model=Schema.DriverDocumentReturn)
def DriverLisence(Driver_id:int,token:str,file: UploadFile,db : Session = Depends(get_db)):
  Driverauth = oauth2.get_currentuser(token)
  
  
  
  
  
  
  
  
  Driver_query = db.query(models.Driver).filter(models.Driver.id == Driver_id)
  Driver_payload = Driver_query.first()
  
  if Driver_payload.id != int(Driverauth.user_id):
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid logins")
    
    
  

  result=upload(file.file)
  url=result.get("url")
  
    
    
    
    
  verification = idanalyzer.ValidDocument(url)
  if verification == url:
    db_document= models.DriverDocument(image = verification, Driverid = Driverauth.user_id)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document
    # Driver_payload.is_verified = True
    # Driver_payload.driverlisence = verification

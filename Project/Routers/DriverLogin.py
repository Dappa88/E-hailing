from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from  .. import models, Schema ,utils,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends ,APIRouter
from datetime import timedelta
from ..database import get_db


router = APIRouter(tags=["Driver"])

@router.post("/login",status_code=status.HTTP_202_ACCEPTED,response_model=Schema.AccessToken)
def Driver_login(driver: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    # print("driver",driver.username)
    driver_details_query = db.query(models.Driver).filter(models.Driver.email == driver.username)
    
    
    driver_details = driver_details_query.first()
    
    
    
    if driver_details == None:
        # print("i am here",driver_details)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")
    if not(utils.Verify(driver.password,driver_details.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")
        
    access_token = oauth2.create_access_token({"id":driver_details.id,"email":driver_details.email,"phone":driver_details.phone},expires_delta=timedelta(minutes=60))
    return {"accesstoken" : access_token,
            "token_type" : "bearer"
            

            }
        
        
        




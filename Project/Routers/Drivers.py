from fastapi import FastAPI,Response,status,HTTPException,Depends ,APIRouter,UploadFile,File
from ..database import engine,get_db
from  .. import models, Schema,dotenv,utils,Email_validation,oauth2,referal_code
from typing import List
from sqlalchemy.orm import Session
from ..External_API import phoneverification
from sqlalchemy import  or_




router = APIRouter(tags=["Driver"],prefix="/Driver")

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Schema.Driver_return)
def createDriver(Driver_payload:Schema.Driver,  db:Session = Depends(get_db)):
    # Driver_payload.email = 
   
    Email = db.query(models.Driver).filter(models.Driver.email == Driver_payload.email).first()
    
    
  
    
    
    Driver_payload.phone = phoneverification.International(Driver_payload.phone)
    querstring = {
    "api_key": f"{dotenv.Process.Abstract_api_key}",
    "phone" : Driver_payload.phone
}
    phoneNo = db.query(models.Driver).filter(models.Driver.phone == Driver_payload.phone).first()
  
    if phoneNo:
        
        raise HTTPException(status_code=status.HTTP_226_IM_USED,detail="Phone number already in use")
    

    if Email:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,detail="Email already in use")
    if phoneverification.PhoneVerify(querstring)==None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="invalid phone number")
    
    if Driver_payload.age < 18:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Drivers age should be more than 18")
    
    Driver_payload.password = utils.hash(Driver_payload.password)
    db_driver = models.Driver(**Driver_payload.dict())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver
    
    
    
    
        
@router.put("/{Driver_id}",status_code=status.HTTP_200_OK,response_model=Schema.Driver_return)
def UpdateDriver(Driver_id:int,  Driver_payload:Schema.Driver_update, db:Session = Depends(get_db), Driverauth:str=Depends(oauth2.get_currentuser)):
    
    
    Driver_query = db.query(models.Driver).filter(models.Driver.id == Driver_id)
    
    Driver_details = Driver_query.first()
    
    Details_check = db.query(models.Driver).filter(or_(models.Driver.email == Driver_payload.email),(models.Driver.phone == Driver_payload.phone)).first()
    
    Driver_payload.phone = phoneverification.International(Driver_payload.phone)
    querstring = {
    "api_key": f"{dotenv.Process.Abstract_api_key}",
    "phone" : Driver_payload.phone
}
    
    if Details_check:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,detail="Detail provided already in memory")
    
    
    if Driver_details == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid logins")
    
    print("Driverauth", type(Driverauth.user_id))
    print("Driver_details",type(Driver_details.id))
    
    if Driver_details.id != int(Driverauth.user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authorized to make changes")
    
    if phoneverification.PhoneVerify(querstring)==None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="invalid phone number")
    
    Driver_query.update(Driver_payload.dict(),synchronize_session=False)
    db.commit()
    
    return Driver_query.first()
    
        
    
# DRIVER CAR

@router.post("/car/{Driver_id}",status_code=status.HTTP_201_CREATED,response_model=Schema.CarReturn)
def Carinfo(Driver_id:int,Car_details:Schema.CarDetails,db : Session = Depends(get_db),Driverauth:str=Depends(oauth2.get_currentuser)):
    
    Driver_query = db.query(models.Driver).filter(models.Driver.id == Driver_id)
    
    Car_payload = db.query(models.Car).filter(models.Car.licenseplate == Car_details.licenseplate).first()
    
    Driver_details = Driver_query.first()
    
    print("Driverdetails",Driver_details)
    
    if Driver_details == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid logins")
    
    if Driver_details.id != int(Driverauth.user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authorized to make changes")
    
    
    if Car_details.year < 2006:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail ="Car version has to be 2006 or newer")
    
    
    
    
    
    
    if Driver_details.is_verified == False:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,detail="Please update Drivers Lisence")
    
    if Car_payload:
        
        raise HTTPException(status_code=status.HTTP_226_IM_USED,detail="Car already exists in memory")
    
    
    db_car= models.Car(Driverid = int(Driverauth.user_id),**Car_details.dict())
    
    db.add(db_car)
    
    db.commit()
    
    db.refresh(db_car)
    return db_car
    
    

        
        
    
# Driver Referral code
@router.post("/referals/{Driver_id}",status_code=status.HTTP_201_CREATED,response_model=Schema.Driver_referalcode_return)
# user needs to be login and verified to generate the code
def GenerateCode(Driver_id:int, db : Session = Depends(get_db),Driverauth:str =Depends(oauth2.get_currentuser)):
    driver_query = db.query(models.Driver).filter(models.Driver.id == Driver_id)
    
    driver_payload = driver_query.first()
    
    if driver_payload == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Driver not found")
    
    if int(Driverauth.user_id) != driver_payload.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authorized to make changes")
    
    if driver_payload.is_verified == False:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,detail="Please update Drivers Lisence")
    
    check_driver = db.query(models.DriverReferralCode).filter(models.DriverReferralCode.Driverid == Driverauth.user_id).first()
    
    if check_driver:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,detail="Driver already has unique code")
    
    refferalcode = referal_code.id_generator()
    check_referal = db.query(models.DriverReferralCode).filter(models.DriverReferralCode.refferalcode == refferalcode).first()
    if check_referal:
        
        refferalcode = referal_code.id_generator(1)
    
        
        
    db_refereed= models.DriverReferralCode(Driverid = Driverauth.user_id,refferalcode = refferalcode)
    db.add(db_refereed)
    db.commit()
    db.refresh(db_refereed)
    return db_refereed
    
        
        
    
@router.patch("/{Driver_id}",status_code=status.HTTP_202_ACCEPTED,response_model=Schema.Driver_return)
def Verifieduser(Driver_id:int, db : Session = Depends(get_db),Driverauth:str =Depends(oauth2.get_currentuser)):
    driver_query = db.query(models.Driver).filter(models.Driver.id == Driver_id)
    
    driver_payload = driver_query.first()
    
    
    if driver_payload == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Driver not found")
    
    if int(Driverauth.user_id) != driver_payload.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authorized to make changes")
    
    driver_Document = db.query(models.DriverDocument).filter(models.Driver.id == Driver_id).first()
    
    if driver_Document:
        driver_query.update(is_verified= True,synchronize_session=False)
        db.commit()
    
    return driver_query.first()
             
     
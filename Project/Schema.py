from typing import Optional
from pydantic import BaseModel,EmailStr


class Driver(BaseModel):
    email:EmailStr
    password :str
    name:str
    age:int 
    
    phone:str
    city : str
    languages:str
    
class Driver_update(BaseModel):
    email:EmailStr
    name:str
    phone:str
    city:str
    languages:str
class Driver_return(BaseModel):
    email:EmailStr
    name:str
    phone:str
    city:str
    is_verified:bool
    class Config:
        orm_mode = True
    
    
class AccessToken(BaseModel):
    accesstoken:str
    token_type:str
    
    
    
class TokenData(BaseModel):
   
    user_id : Optional[str] = None


class CarDetails(BaseModel):
    manufacturer:str
    model:str
    name:str
    year:int
    colour:str
    licenseplate:str
    # Driverid:int

class CarReturn(BaseModel):
    colour:str
    name:str
    year:int
    Drivers: Driver_return
    
    class Config:
        orm_mode = True
        
class Driver_referralcode(BaseModel):
    refferalcode:int
    


class Driver_referalcode_return(BaseModel):
    refferalcode:int
    Driverid:str
    Drivers: Driver_return
    class Config:
        orm_mode = True
        
class DriverDocumentReturn(BaseModel):
    image:str
    Driverid:str
    Drivers: Driver_return
    
    
    class Config:
        orm_mode = True
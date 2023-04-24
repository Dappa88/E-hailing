import requests
from fastapi import FastAPI,Response,status,HTTPException
url = "https://phonevalidation.abstractapi.com/v1/"

def International(phone:str):
    if phone.startswith("0"):
        phone = "+234"+phone[1:]
        return phone
    else:
        return phone

def PhoneVerify(querstring,url=url):
    try:
        response = requests.get(url, params=querstring)
        
        responseValue = response.json()["valid"]
        
        
        if responseValue == False:
            print("none")
            
            return None
        else:
            
            return response.json()["phone"]
    except Exception as e:
        
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="verification failed")
        
    
    

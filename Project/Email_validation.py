from email_validator import validate_email, EmailNotValidError
from fastapi import FastAPI,Response,status,HTTPException,Depends ,APIRouter
 
def Emailcheck(email):
    try:
      # validate and get info
        v = validate_email(email)
        print("v",v)
        # replace with normalized form
        email = v["email"]
        return email
    except EmailNotValidError as e:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,detail=e)
        
        # email is not valid, exception message is human-readable
        
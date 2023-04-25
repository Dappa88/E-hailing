import idanalyzer
from ..import dotenv
from fastapi import FastAPI,Response,status,HTTPException


# image="C:\\Users\\HP PC\\Desktop\\Beast_backend\\Bolt\\Project\\External_API\\test.png"
def ValidDocument(image:str):
    
    try:
        
        coreapi = idanalyzer.CoreAPI(f"{dotenv.Process.coreapikeys}", "US")
        
        coreapi.enable_dualside_check(True)
        coreapi.enable_authentication(1)
        coreapi.restrict_type(document_type="D")
        # coreapi.enable_vault(no_duplicate_image=True)
        
        response = coreapi.scan(document_primary=image)
        
       
        
        
        
        if response["verification"]["passed"] == False or response["verification"]["result"]["notexpired"] == False:
            
            
            
            
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Document not valid or expired")
            
        
       
        else:
            if response["verification"]["passed"] == True:
                return image
            if response["error"]:
               
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=response["error"]["message"])
       
    except idanalyzer.APIError as e:
        
    # If API returns an error, catch it
        details = e.args[0]
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=details["message"])
       
        

    except Exception as e:
        # status_code = status.HTTP_406_NOT_ACCEPTABLE
       
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="error")


    

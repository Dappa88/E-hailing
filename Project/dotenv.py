from pydantic import BaseSettings
 
# from .utils import pwd_context
#Format SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
class Settings(BaseSettings):
    Database_username : str = "postgres"
    Database_password : str
    Database_name:str
    SQLALCHEMY_DATABASE_URL:str
    coreapikeys:str
    cloud_name:str
    cloudapi_key:str
    cloudapi_secret:str
    Abstract_api_key:str
    JWTSECRET_KEY:str
    JWTALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    
    
    
    class Config:
        env_file = "C:\\Users\\HP PC\\Desktop\\Beast_backend\\Bolt\\.env"
# if it doesnt work add the port number in the sql url
Process = Settings()

print(Process.Database_username)

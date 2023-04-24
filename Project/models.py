from logging import NullHandler
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship
from .database import Base

from sqlalchemy.sql.expression import text


class Driver(Base):
    __tablename__ = "driver"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True,nullable=False)
    password = Column(String,nullable=False)
    is_verified = Column(Boolean, server_default="False")
    name = Column(String,nullable=False)
    age = Column(Integer,nullable=False)
    phone = Column(String,nullable=False,unique=True,index=True)
    city = Column(String,nullable=False)
    languages = Column(String,nullable=False)
    referedby = Column(String,nullable=True)
    # driverlisence = Column(String,nullable=True)
    createdAt = Column(TIMESTAMP(timezone=True),nullable=False,server_default = text("now()"))
   
    # referalcode = Column(String,unique=True,nullable=True)

    Car_owner = relationship("Car",back_populates="Drivers")
    
class DriverReferralCode(Base):
    __tablename__ = "referralcode"
    id = Column(Integer, primary_key=True, index=True)
    refferalcode = Column(Integer,index=True,unique=True,nullable=False)
    
    Driverid = Column(Integer,ForeignKey("driver.id",ondelete="CASCADE"),nullable=False)
    
    Drivers = relationship(Driver)
    
class DriverDocument(Base):
    __tablename__ = "Document"
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String,nullable= False,index = True)
    
    
    Driverid = Column(Integer,ForeignKey("driver.id",ondelete="CASCADE"),nullable=False)
    
    Drivers = relationship(Driver)

class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    manufacturer = Column(String, nullable=False)
    model = Column(String, nullable=False)
    name = Column(String, nullable=False)
    year = Column(Integer,nullable=False)
    colour = Column(String, nullable=False)
    licenseplate =  Column(String, nullable=False)
    Driverid = Column(Integer,ForeignKey("driver.id",ondelete="CASCADE"),nullable=False)
    
    Drivers = relationship(Driver,back_populates="Car_owner")
    
    
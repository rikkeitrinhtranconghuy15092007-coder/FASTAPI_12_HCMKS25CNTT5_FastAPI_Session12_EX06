from sqlalchemy import Column, Integer, String
from BT6.database import Base

class MedicalDeviceModel(Base):
    __tablename__ = "medical_devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_code = Column(String(50), unique=True, nullable=False, index=True)
    device_name = Column(String(255), nullable=False)
    department = Column(String(100), nullable=False)
    status = Column(String(50), default='ACTIVE')
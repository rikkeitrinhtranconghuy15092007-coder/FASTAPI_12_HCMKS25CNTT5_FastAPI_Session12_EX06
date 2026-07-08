from sqlalchemy.orm import Session
from BT6.model import MedicalDeviceModel

def get_device_by_code(db: Session, device_code: str):
    return db.query(MedicalDeviceModel).filter(MedicalDeviceModel.device_code == device_code).first()

def get_device_by_id(db: Session, device_id: int):
    return db.query(MedicalDeviceModel).filter(MedicalDeviceModel.id == device_id).first()

def get_all_devices(db: Session):
    return db.query(MedicalDeviceModel).all()

def create_medical_device(db: Session, device_code: str, device_name: str, department: str, status: str):
    new_device = MedicalDeviceModel(
        device_code=device_code,
        device_name=device_name,
        department=department,
        status=status
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device
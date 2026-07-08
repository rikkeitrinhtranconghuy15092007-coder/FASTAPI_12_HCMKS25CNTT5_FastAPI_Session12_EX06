import uvicorn
from fastapi import FastAPI, status, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from BT6.database import engine, Base, get_db
import BT6.employee_service as employee_service

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medical Devices Multi-file API")

class MedicalDeviceCreate(BaseModel):
    device_code: str = Field(..., min_length=1)
    device_name: str = Field(..., min_length=3)
    department: str = Field(..., min_length=1)
    status: Literal['ACTIVE', 'INACTIVE'] = 'ACTIVE'

class APIStandardResponse(BaseModel):
    statusCode: int
    message: str
    error: Optional[str] = None
    data: Optional[dict] = None
    path: str
    timestamp: str

class APIListStandardResponse(BaseModel):
    statusCode: int
    message: str
    error: Optional[str] = None
    data: List[dict]
    path: str
    timestamp: str

@app.post("/devices", status_code=status.HTTP_201_CREATED, response_model=APIStandardResponse)
async def create_device(request: Request, payload: MedicalDeviceCreate, db: Session = Depends(get_db)):
    existing_device = employee_service.get_device_by_code(db, payload.device_code.strip())
    if existing_device:
        return APIStandardResponse(
            statusCode=400,
            message="Mã thiết bị y tế này đã tồn tại trên hệ thống",
            error="Bad Request",
            data=None,
            path=str(request.url.path),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        
    try:
        new_device = employee_service.create_medical_device(
            db=db,
            device_code=payload.device_code.strip(),
            device_name=payload.device_name.strip(),
            department=payload.department.strip(),
            status=payload.status
        )
        return APIStandardResponse(
            statusCode=201,
            message="Thêm thiết bị y tế thành công",
            error=None,
            data={
                "id": new_device.id,
                "device_code": new_device.device_code,
                "device_name": new_device.device_name,
                "department": new_device.department,
                "status": new_device.status
            },
            path=str(request.url.path),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    except Exception as e:
        db.rollback()
        return APIStandardResponse(
            statusCode=500,
            message="Lỗi hệ thống khi lưu trữ dữ liệu",
            error=str(e),
            data=None,
            path=str(request.url.path),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

@app.get("/devices", status_code=status.HTTP_200_OK, response_model=APIListStandardResponse)
async def get_all_devices(request: Request, db: Session = Depends(get_db)):
    devices = employee_service.get_all_devices(db)
    data_list = [
        {
            "id": dev.id,
            "device_code": dev.device_code,
            "device_name": dev.device_name,
            "department": dev.department,
            "status": dev.status
        } for dev in devices
    ]
    return APIListStandardResponse(
        statusCode=200,
        message="Lấy danh sách thiết bị y tế thành công",
        error=None,
        data=data_list,
        path=str(request.url.path),
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

@app.get("/devices/{device_id}", status_code=status.HTTP_200_OK, response_model=APIStandardResponse)
async def get_device_detail(device_id: int, request: Request, db: Session = Depends(get_db)):
    device = employee_service.get_device_by_id(db, device_id)
    if not device:
        return APIStandardResponse(
            statusCode=404,
            message="Device not found",
            error="Not Found",
            data=None,
            path=str(request.url.path),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    return APIStandardResponse(
        statusCode=200,
        message="Lấy thông tin chi tiết thiết bị thành công",
        error=None,
        data={
            "id": device.id,
            "device_code": device.device_code,
            "device_name": device.device_name,
            "department": device.department,
            "status": device.status
        },
        path=str(request.url.path),
        timestamp=datetime.utcnow().isoformat() + "Z"
    )
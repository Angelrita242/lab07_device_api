from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="SmartBuilding Devices API")

class Device(BaseModel):
    id: int
    name: str
    energy_usage: int
    location: str
    status: str = "inactive"

class DeviceCreate(BaseModel):
    name: str
    energy_usage: int
    location: str
    status: str = "inactive"

# In-memory "database"
devices = [
    {
        "id": 1,
        "name": "coffee_machine",
        "energy_usage": 120,
        "status": "active",
        "location": "kitchen"
    },
    {
        "id": 2,
        "name": "smart_lamp",
        "energy_usage": 40,
        "status": "inactive",
        "location": "office"
    }
]

@app.get("/")
def home():
    return {"message": "Smart Building Device API"}

@app.get("/devices")
def get_all_devices(status: Optional[str] = None):
    if status is not None:
        return [device for device in devices if device["status"] == status]
    return devices

@app.post("/devices", response_model=Device)
def create_device(device: DeviceCreate):
    new_id = max([d["id"] for d in devices], default=0) + 1
    new_device = {
        "id": new_id,
        **device.dict()
    }
    devices.append(new_device)
    return new_device

@app.get("/devices/{device_id}", response_model=Device)
def get_device(device_id: int):
    for device in devices:
        if device["id"] == device_id:
            return device
    raise HTTPException(status_code=404, detail="Device Not Found")

@app.put("/devices/{device_id}", response_model=Device)
def update_device(device_id: int, updated_device: DeviceCreate):
    for device in devices:
        if device["id"] == device_id:
            device.update(updated_device.dict())
            return device
    raise HTTPException(status_code=404, detail="Device Not Found")

@app.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int):
    global devices
    for index, device in enumerate(devices):
        if device["id"] == device_id:
            devices.pop(index)
            return
    raise HTTPException(status_code=404, detail="Device Not Found")

@app.get("/analytics/total-energy")
def get_total_energy_usage():
    total_energy_usage = sum(device["energy_usage"] for device in devices)
    return {"total_energy_usage": total_energy_usage}


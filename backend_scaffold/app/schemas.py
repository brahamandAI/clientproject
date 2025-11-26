from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date
import uuid

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    role: str

class ProjectBase(BaseModel):
    jan: str
    company: str
    po_no: Optional[str] = None
    work_order_no: Optional[str] = None
    work_name: str
    site_location: Optional[str] = None
    client_name: Optional[str] = None
    billing_address: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    work_value: Optional[float] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: uuid.UUID
    status: str

class RABillBase(BaseModel):
    project_id: uuid.UUID
    ra_bill_no: str
    ra_bill_date: date
    basic_amount: float
    deduction: Optional[float] = 0.0

class RABillCreate(RABillBase):
    pass

class RABillOut(RABillBase):
    id: uuid.UUID
    net_pay: float
    status: str

class GSTEntryBase(BaseModel):
    project_id: uuid.UUID
    ra_bill_id: uuid.UUID
    taxable_amount: float

class GSTEntryCreate(GSTEntryBase):
    pass

class GSTEntryOut(GSTEntryBase):
    id: uuid.UUID
    igst_amount: float
    invoice_value: float
    gst_status: str

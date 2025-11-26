from fastapi import APIRouter, HTTPException
from app.db import database
from app.models import ra_bills, projects
from app.schemas import RABillCreate, RABillOut
from sqlalchemy import insert, select
from uuid import UUID
from decimal import Decimal

router = APIRouter()

@router.post('/', response_model=RABillOut)
async def create_ra_bill(payload: RABillCreate):
    # check project exists
    q = select([projects.c.id]).where(projects.c.id == payload.project_id)
    if not await database.fetch_one(q):
        raise HTTPException(status_code=400, detail='Project not found')
    # compute net_pay
    net = Decimal(str(payload.basic_amount)) - Decimal(str(payload.deduction or 0))
    ins = insert(ra_bills).values(
        project_id=payload.project_id,
        ra_bill_no=payload.ra_bill_no,
        ra_bill_date=payload.ra_bill_date,
        basic_amount=payload.basic_amount,
        deduction=payload.deduction or 0,
        net_pay=net
    )
    await database.execute(ins)
    q2 = select([ra_bills]).where(ra_bills.c.ra_bill_no == payload.ra_bill_no)
    row = await database.fetch_one(q2)
    return row

@router.get('/project/{project_id}', response_model=list[RABillOut])
async def list_by_project(project_id: UUID):
    q = select([ra_bills]).where(ra_bills.c.project_id == project_id)
    rows = await database.fetch_all(q)
    return rows

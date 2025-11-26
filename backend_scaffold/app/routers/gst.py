from fastapi import APIRouter, HTTPException
from app.db import database
from app.models import gst_entries, ra_bills, projects
from app.schemas import GSTEntryCreate, GSTEntryOut
from sqlalchemy import insert, select
from decimal import Decimal

router = APIRouter()

@router.post('/', response_model=GSTEntryOut)
async def create_gst_entry(payload: GSTEntryCreate):
    # validations
    if not await database.fetch_one(select([projects.c.id]).where(projects.c.id == payload.project_id)):
        raise HTTPException(status_code=400, detail='Project not found')
    if not await database.fetch_one(select([ra_bills.c.id]).where(ra_bills.c.id == payload.ra_bill_id)):
        raise HTTPException(status_code=400, detail='RA bill not found')
    taxable = Decimal(str(payload.taxable_amount))
    igst = taxable * Decimal('0.18')
    invoice = taxable + igst
    ins = insert(gst_entries).values(
        project_id=payload.project_id,
        ra_bill_id=payload.ra_bill_id,
        taxable_amount=payload.taxable_amount,
        igst_amount=igst,
        invoice_value=invoice
    )
    await database.execute(ins)
    q2 = select([gst_entries]).where(gst_entries.c.ra_bill_id == payload.ra_bill_id)
    row = await database.fetch_one(q2)
    return row

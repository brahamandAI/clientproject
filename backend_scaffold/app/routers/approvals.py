from fastapi import APIRouter, HTTPException
from app.db import database
from app.models import approvals, projects, ra_bills, gst_entries
from sqlalchemy import insert, select, update
from uuid import UUID

router = APIRouter()

@router.post('/{entity_type}/{entity_id}/approve')
async def approve(entity_type: str, entity_id: UUID, notes: str = None):
    # minimal approve flow
    table_map = {'project': projects, 'ra_bill': ra_bills, 'gst': gst_entries}
    if entity_type not in table_map:
        raise HTTPException(status_code=400, detail='Invalid entity type')
    tbl = table_map[entity_type]
    # update status
    upd = update(tbl).where(tbl.c.id == entity_id).values(status='approved')
    await database.execute(upd)
    # create approval record
    ins = insert(approvals).values(entity_type=entity_type, entity_id=entity_id, status='approved', notes=notes)
    await database.execute(ins)
    return {'status': 'approved'}

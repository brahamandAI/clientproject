from fastapi import APIRouter, HTTPException, Depends
from app.db import database
from app.models import projects
from app.schemas import ProjectCreate, ProjectOut
from sqlalchemy import insert, select, update
from uuid import UUID

router = APIRouter()

@router.post('/', response_model=ProjectOut)
async def create_project(payload: ProjectCreate):
    # simple JAN check uniqueness
    q = select([projects.c.id]).where(projects.c.jan == payload.jan)
    if await database.fetch_one(q):
        raise HTTPException(status_code=400, detail='JAN already exists')
    ins = insert(projects).values(**payload.dict())
    await database.execute(ins)
    q2 = select([projects]).where(projects.c.jan == payload.jan)
    p = await database.fetch_one(q2)
    return p

@router.get('/', response_model=list[ProjectOut])
async def list_projects():
    q = select([projects])
    rows = await database.fetch_all(q)
    return rows

@router.get('/{project_id}', response_model=ProjectOut)
async def get_project(project_id: UUID):
    q = select([projects]).where(projects.c.id == project_id)
    p = await database.fetch_one(q)
    if not p:
        raise HTTPException(status_code=404, detail='Not found')
    return p

@router.put('/{project_id}', response_model=ProjectOut)
async def update_project(project_id: UUID, payload: ProjectCreate):
    q = select([projects]).where(projects.c.id == project_id)
    if not await database.fetch_one(q):
        raise HTTPException(status_code=404, detail='Not found')
    upd = update(projects).where(projects.c.id == project_id).values(**payload.dict())
    await database.execute(upd)
    p = await database.fetch_one(select([projects]).where(projects.c.id == project_id))
    return p

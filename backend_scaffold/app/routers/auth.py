from fastapi import APIRouter, HTTPException, Depends
from app.db import database
from app.models import users
from app.schemas import UserCreate, UserOut
from app.utils import hash_password, verify_password, create_access_token
from sqlalchemy import select, insert

router = APIRouter()

@router.post('/register', response_model=UserOut)
async def register(payload: UserCreate):
    query = select([users.c.email]).where(users.c.email == payload.email)
    row = await database.fetch_one(query)
    if row:
        raise HTTPException(status_code=400, detail='Email already registered')
    pwd = hash_password(payload.password)
    ins = insert(users).values(name=payload.name, email=payload.email, password_hash=pwd)
    r = await database.execute(ins)
    # fetch created user
    q2 = select([users]).where(users.c.email == payload.email)
    user = await database.fetch_one(q2)
    return {k: user[k] for k in ('id','name','email','role')}

@router.post('/login')
async def login(payload: UserCreate):
    q = select([users]).where(users.c.email == payload.email)
    user = await database.fetch_one(q)
    if not user:
        raise HTTPException(status_code=400, detail='Invalid credentials')
    if not verify_password(payload.password, user['password_hash']):
        raise HTTPException(status_code=400, detail='Invalid credentials')
    token = create_access_token({'sub': str(user['id']), 'role': user['role']})
    return {'access_token': token, 'token_type': 'bearer'}

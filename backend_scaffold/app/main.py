from fastapi import FastAPI
from app.db import database, metadata, engine
from app.routers import auth, projects, ra_bills, gst, approvals

app = FastAPI(title='CPMS - Backend')

# Include routers
app.include_router(auth.router, prefix='/api/auth', tags=['auth'])
app.include_router(projects.router, prefix='/api/projects', tags=['projects'])
app.include_router(ra_bills.router, prefix='/api/ra_bills', tags=['ra_bills'])
app.include_router(gst.router, prefix='/api/gst', tags=['gst'])
app.include_router(approvals.router, prefix='/api/approvals', tags=['approvals'])

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

import os
from databases import Database
from sqlalchemy import MetaData, create_engine
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:password@localhost:5432/cpms_db')

# databases supports async queries, SQLAlchemy engine is used for metadata / Alembic
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL.replace('+asyncpg',''), future=True)
metadata = MetaData()

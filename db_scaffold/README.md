# PostgreSQL Database Scaffold for CPMS

## Files
- schema.sql — full database structure
- seed.sql — optional sample data

## Usage
1. Start PostgreSQL locally.
2. Create a database:
   createdb cpms_db
3. Run schema:
   psql cpms_db < schema.sql
4. Load sample data (optional):
   psql cpms_db < seed.sql

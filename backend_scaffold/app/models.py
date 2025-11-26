from sqlalchemy import Table, Column, String, Date, Numeric, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa
from .db import metadata
import enum
import uuid
from sqlalchemy.sql import func

class StatusEnum(str, enum.Enum):
    pending = 'pending'
    approved = 'approved'
    rejected = 'rejected'

class RoleEnum(str, enum.Enum):
    user = 'user'
    admin = 'admin'

users = Table(
    'users', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('name', String, nullable=False),
    Column('email', String, nullable=False, unique=True),
    Column('password_hash', String, nullable=False),
    Column('role', Enum(RoleEnum), nullable=False, server_default=RoleEnum.user.value),
    Column('created_at', TIMESTAMP, server_default=func.now())
)

projects = Table(
    'projects', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('jan', String, nullable=False, unique=True),
    Column('company', String, nullable=False),
    Column('po_no', String),
    Column('work_order_no', String),
    Column('work_name', String, nullable=False),
    Column('site_location', String),
    Column('client_name', String),
    Column('billing_address', String),
    Column('start_date', Date),
    Column('end_date', Date),
    Column('work_value', Numeric(15,2)),
    Column('status', Enum(StatusEnum), nullable=False, server_default=StatusEnum.pending.value),
    Column('created_by', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('approved_by', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('created_at', TIMESTAMP, server_default=func.now()),
    Column('updated_at', TIMESTAMP, server_default=func.now(), onupdate=func.now())
)

ra_bills = Table(
    'ra_bills', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('project_id', UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
    Column('ra_bill_no', String, nullable=False),
    Column('ra_bill_date', Date, nullable=False),
    Column('basic_amount', Numeric(15,2), nullable=False),
    Column('deduction', Numeric(15,2), server_default='0'),
    Column('net_pay', Numeric(15,2)),
    Column('status', Enum(StatusEnum), nullable=False, server_default=StatusEnum.pending.value),
    Column('created_by', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('approved_by', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('created_at', TIMESTAMP, server_default=func.now()),
    Column('updated_at', TIMESTAMP, server_default=func.now(), onupdate=func.now())
)

gst_entries = Table(
    'gst_entries', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('project_id', UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
    Column('ra_bill_id', UUID(as_uuid=True), ForeignKey('ra_bills.id', ondelete='CASCADE'), nullable=False),
    Column('taxable_amount', Numeric(15,2), nullable=False),
    Column('igst_amount', Numeric(15,2)),
    Column('invoice_value', Numeric(15,2)),
    Column('gst_status', Enum(StatusEnum), server_default=StatusEnum.pending.value),
    Column('created_by', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('approved_by', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('created_at', TIMESTAMP, server_default=func.now()),
    Column('updated_at', TIMESTAMP, server_default=func.now(), onupdate=func.now())
)

approvals = Table(
    'approvals', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('entity_type', String, nullable=False),
    Column('entity_id', UUID(as_uuid=True), nullable=False),
    Column('approved_by', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('notes', String),
    Column('status', Enum(StatusEnum), nullable=False),
    Column('approved_at', TIMESTAMP, server_default=func.now())
)

audit_logs = Table(
    'audit_logs', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('entity_type', String, nullable=False),
    Column('entity_id', UUID(as_uuid=True), nullable=False),
    Column('action', String, nullable=False),
    Column('performed_by', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('details', sa.dialects.postgresql.JSONB),
    Column('timestamp', TIMESTAMP, server_default=func.now())
)

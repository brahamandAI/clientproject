-- PostgreSQL schema for CPMS
CREATE TYPE status_enum AS ENUM ('pending','approved','rejected');
CREATE TYPE role_enum AS ENUM ('user','admin');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role role_enum NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    jan VARCHAR(50) UNIQUE NOT NULL,
    company VARCHAR(10) NOT NULL,
    po_no TEXT,
    work_order_no TEXT,
    work_name TEXT NOT NULL,
    site_location TEXT,
    client_name TEXT,
    billing_address TEXT,
    start_date DATE,
    end_date DATE,
    work_value NUMERIC(15,2),
    status status_enum NOT NULL DEFAULT 'pending',
    created_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE ra_bills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    ra_bill_no TEXT NOT NULL,
    ra_bill_date DATE NOT NULL,
    basic_amount NUMERIC(15,2) NOT NULL,
    deduction NUMERIC(15,2) DEFAULT 0,
    net_pay NUMERIC(15,2),
    status status_enum NOT NULL DEFAULT 'pending',
    created_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE gst_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    ra_bill_id UUID NOT NULL REFERENCES ra_bills(id) ON DELETE CASCADE,
    taxable_amount NUMERIC(15,2) NOT NULL,
    igst_amount NUMERIC(15,2),
    invoice_value NUMERIC(15,2),
    gst_status status_enum DEFAULT 'pending',
    created_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE approvals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    approved_by UUID REFERENCES users(id),
    notes TEXT,
    status status_enum NOT NULL,
    approved_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    action TEXT NOT NULL,
    performed_by UUID REFERENCES users(id),
    details JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);

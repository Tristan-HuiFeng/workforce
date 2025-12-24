-- =========================================================
-- Workforce Compliance & Scheduling Assistant
-- Database Schema (PostgreSQL)
-- =========================================================

-- Required extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================
-- ENUM TYPES
-- =====================
CREATE TYPE user_role AS ENUM ('staff', 'supervisor', 'manager');
CREATE TYPE shift_type AS ENUM ('morning', 'afternoon', 'night');
CREATE TYPE compliance_status AS ENUM ('ok', 'needs_attention', 'critical');
CREATE TYPE incident_type AS ENUM ('incident', 'commendation');

-- =====================
-- SITES
-- =====================
CREATE TABLE sites (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  location TEXT
);

-- =====================
-- USERS
-- =====================
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role user_role NOT NULL,
  site_id UUID REFERENCES sites(id) ON DELETE SET NULL, -- supervisor assigned site
  created_at TIMESTAMP DEFAULT now(),
  CONSTRAINT supervisor_site_check CHECK (
      (role = 'supervisor' AND site_id IS NOT NULL) OR
      (role != 'supervisor' AND site_id IS NULL)
  )
);

-- =====================
-- JOB ROLES
-- =====================
CREATE TABLE job_roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE
);

-- =====================
-- STAFF
-- =====================
CREATE TABLE staff (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  role_id UUID REFERENCES job_roles(id),
  full_name TEXT NOT NULL,
  active BOOLEAN DEFAULT true
);

-- Staff ↔ Sites mapping (staff can work at multiple sites)
CREATE TABLE staff_sites (
  staff_id UUID REFERENCES staff(id) ON DELETE CASCADE,
  site_id UUID REFERENCES sites(id) ON DELETE CASCADE,
  PRIMARY KEY (staff_id, site_id)
);

-- =====================
-- CERTIFICATIONS
-- =====================
CREATE TABLE certifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT
);

CREATE TABLE staff_certifications (
  staff_id UUID REFERENCES staff(id) ON DELETE CASCADE,
  certification_id UUID REFERENCES certifications(id) ON DELETE CASCADE,
  expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
  status compliance_status DEFAULT 'ok',
  PRIMARY KEY (staff_id, certification_id)
);

-- =====================
-- SCHEDULING
-- =====================
CREATE TABLE shifts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  site_id UUID REFERENCES sites(id) ON DELETE CASCADE,
  shift_date DATE NOT NULL,
  shift_type shift_type NOT NULL,
  start_time TIMESTAMP WITH TIME ZONE NOT NULL,
  end_time TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE certification_roles (
  certification_id UUID REFERENCES certifications(id) ON DELETE CASCADE,
  role_id UUID REFERENCES job_roles(id) ON DELETE CASCADE,
  PRIMARY KEY (certification_id, role_id)
);

CREATE TABLE certification_shift_types (
  certification_id UUID REFERENCES certifications(id) ON DELETE CASCADE,
  shift_type shift_type NOT NULL,
  PRIMARY KEY (certification_id, shift_type)
);

CREATE TABLE shift_assignments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  shift_id UUID REFERENCES shifts(id) ON DELETE CASCADE,
  staff_id UUID REFERENCES staff(id) ON DELETE CASCADE,
  UNIQUE (shift_id, staff_id)
);

-- =====================
-- NOTES & INCIDENTS
-- =====================
CREATE TABLE staff_notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  staff_id UUID REFERENCES staff(id) ON DELETE CASCADE,
  shift_id UUID REFERENCES shifts(id) ON DELETE SET NULL,
  note TEXT NOT NULL,
  status compliance_status NOT NULL,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE incidents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  staff_id UUID REFERENCES staff(id) ON DELETE CASCADE,
  description TEXT NOT NULL,
  type incident_type NOT NULL,
  occurred_at TIMESTAMP DEFAULT now()
);

-- =====================
-- INDEXES
-- =====================
CREATE INDEX idx_staff_cert_expiry ON staff_certifications(expires_at);
CREATE INDEX idx_shift_date ON shifts(shift_date);
CREATE INDEX idx_shift_site ON shifts(site_id);
CREATE INDEX idx_incidents_staff ON incidents(staff_id);
CREATE INDEX idx_notes_staff ON staff_notes(staff_id);

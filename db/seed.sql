-- =========================================================
-- Workforce Compliance & Scheduling Assistant
-- Seed Data (PostgreSQL)
-- =========================================================

-- =====================
-- SITES
-- =====================
INSERT INTO sites (id, name, location) VALUES
  ('11111111-aaaa-1111-aaaa-111111111111', 'Downtown Office', 'City Center'),
  ('22222222-bbbb-2222-bbbb-222222222222', 'Industrial Park', 'West Zone');

-- =====================
-- USERS
-- =====================
INSERT INTO users (id, email, password_hash, role, site_id) VALUES
  ('aaaa1111-1111-aaaa-1111-aaaaaaaa1111', 'alice@company.com', '$2b$12$ruKupbD8Lye61389NAXqNObxLHsG.oyzA8/gPy2WbZTztESdU2k36', 'manager', NULL),
  ('bbbb2222-2222-bbbb-2222-bbbbbbbb2222', 'bob@company.com', '$2b$12$ruKupbD8Lye61389NAXqNObxLHsG.oyzA8/gPy2WbZTztESdU2k36', 'supervisor', '11111111-aaaa-1111-aaaa-111111111111'),
  ('cccc3333-3333-cccc-3333-cccccccc3333', 'carol@company.com', '$2b$12$ruKupbD8Lye61389NAXqNObxLHsG.oyzA8/gPy2WbZTztESdU2k36', 'staff', NULL),
  ('dddd4444-4444-dddd-4444-dddddddd4444', 'dave@company.com', '$2b$12$ruKupbD8Lye61389NAXqNObxLHsG.oyzA8/gPy2WbZTztESdU2k36', 'staff', NULL),
  ('eeee5555-5555-eeee-5555-eeeeeeee5555', 'erin@company.com', '$2b$12$ruKupbD8Lye61389NAXqNObxLHsG.oyzA8/gPy2WbZTztESdU2k36', 'staff', NULL),
  ('ffff6666-6666-ffff-6666-ffffffff6666', 'dan@company.com', '$2b$12$ruKupbD8Lye61389NAXqNObxLHsG.oyzA8/gPy2WbZTztESdU2k36', 'staff', NULL);

-- =====================
-- JOB ROLES
-- =====================
INSERT INTO job_roles (id, name) VALUES
  ('11111111-1111-1111-1111-111111111111', 'Security Guard'),
  ('22222222-2222-2222-2222-222222222222', 'Cleaner'),
  ('33333333-3333-3333-3333-333333333333', 'Technician');

-- =====================
-- STAFF
-- =====================
INSERT INTO staff (id, user_id, role_id, full_name) VALUES
  ('aaaaaaaa-1111-1111-1111-aaaaaaaa1111', 'cccc3333-3333-cccc-3333-cccccccc3333', '11111111-1111-1111-1111-111111111111', 'Carol Smith'),
  ('bbbbbbbb-2222-2222-2222-bbbbbbbb2222', 'dddd4444-4444-dddd-4444-dddddddd4444', '22222222-2222-2222-2222-222222222222', 'Dave Johnson'),
  ('cccccccc-3333-3333-3333-cccccccc3333', 'eeee5555-5555-eeee-5555-eeeeeeee5555', '11111111-1111-1111-1111-111111111111', 'Erin Lee'),
  ('dddddddd-4444-4444-4444-dddddddd4444', 'bbbb2222-2222-bbbb-2222-bbbbbbbb2222', '33333333-3333-3333-3333-333333333333', 'Bob Supervisor'),
  ('eeeeeeee-5555-5555-5555-eeeeeeee5555', 'ffff6666-6666-ffff-6666-ffffffff6666', '33333333-3333-3333-3333-333333333333', 'Dan Tan');

-- =====================
-- STAFF ↔ SITES
-- =====================
INSERT INTO staff_sites (staff_id, site_id) VALUES
  ('aaaaaaaa-1111-1111-1111-aaaaaaaa1111', '11111111-aaaa-1111-aaaa-111111111111'),
  ('bbbbbbbb-2222-2222-2222-bbbbbbbb2222', '11111111-aaaa-1111-aaaa-111111111111'),
  ('cccccccc-3333-3333-3333-cccccccc3333', '22222222-bbbb-2222-bbbb-222222222222'),
  ('eeeeeeee-5555-5555-5555-eeeeeeee5555', '11111111-aaaa-1111-aaaa-111111111111');

-- =====================
-- CERTIFICATIONS
-- =====================
INSERT INTO certifications (id, name, description) VALUES
  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Security License', 'Mandatory for Security'),
  ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'First Aid', 'Mandatory for all'),
  ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'Night Shift Clearance', 'Required for night shifts');

-- =====================
-- CERTIFICATION ROLES
-- =====================
INSERT INTO certification_roles (certification_id, role_id) VALUES
  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111'),
  ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '11111111-1111-1111-1111-111111111111'),
  ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '33333333-3333-3333-3333-333333333333');

-- =====================
-- STAFF CERTIFICATIONS
-- =====================
-- INSERT INTO staff_certifications (staff_id, certification_id, expires_at, status) VALUES
--   ('aaaaaaaa-1111-1111-1111-aaaaaaaa1111', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', CURRENT_DATE + INTERVAL '120 days', 'ok'),
--   ('cccccccc-3333-3333-3333-cccccccc3333', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', CURRENT_DATE + INTERVAL '15 days', 'needs_attention');
INSERT INTO staff_certifications (staff_id, certification_id, expires_at, status) VALUES
  (
    'aaaaaaaa-1111-1111-1111-aaaaaaaa1111',
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    CURRENT_DATE + INTERVAL '120 days' AT TIME ZONE 'UTC',
    'ok'
  ),
  (
    'cccccccc-3333-3333-3333-cccccccc3333',
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    CURRENT_DATE + INTERVAL '15 days' AT TIME ZONE 'UTC',
    'needs_attention'
  );

-- =====================
-- SHIFTS
-- =====================
-- INSERT INTO shifts (id, site_id, shift_date, shift_type, start_time, end_time) VALUES
--   ('aaaaaaaa-aaaa-1111-1111-aaaaaaaaaaaa', '11111111-aaaa-1111-aaaa-111111111111', CURRENT_DATE, 'morning', CURRENT_DATE + TIME '08:00', CURRENT_DATE + TIME '16:00'),
--   ('bbbbbbbb-bbbb-2222-2222-bbbbbbbbbbbb', '11111111-aaaa-1111-aaaa-111111111111', CURRENT_DATE, 'night', CURRENT_DATE + TIME '22:00', (CURRENT_DATE + INTERVAL '1 day') + TIME '06:00');
INSERT INTO shifts (id, site_id, shift_date, shift_type, start_time, end_time) VALUES
  (
    'aaaaaaaa-aaaa-1111-1111-aaaaaaaaaaaa',
    '11111111-aaaa-1111-aaaa-111111111111',
    CURRENT_DATE,
    'morning',
    CURRENT_DATE + TIME '08:00' AT TIME ZONE 'UTC',
    CURRENT_DATE + TIME '16:00' AT TIME ZONE 'UTC'
  ),
  (
    'bbbbbbbb-bbbb-2222-2222-bbbbbbbbbbbb',
    '11111111-aaaa-1111-aaaa-111111111111',
    CURRENT_DATE,
    'night',
    CURRENT_DATE + TIME '22:00' AT TIME ZONE 'UTC',
    (CURRENT_DATE + INTERVAL '1 day') + TIME '06:00' AT TIME ZONE 'UTC'
  );
  
-- =====================
-- SHIFT ASSIGNMENTS
-- =====================
INSERT INTO shift_assignments (shift_id, staff_id) VALUES
  ('aaaaaaaa-aaaa-1111-1111-aaaaaaaaaaaa', 'aaaaaaaa-1111-1111-1111-aaaaaaaa1111'),
  ('bbbbbbbb-bbbb-2222-2222-bbbbbbbbbbbb', 'cccccccc-3333-3333-3333-cccccccc3333');

-- =====================
-- INCIDENTS
-- =====================
INSERT INTO incidents (staff_id, description, type) VALUES
  ('aaaaaaaa-1111-1111-1111-aaaaaaaa1111', 'Arrived late to shift', 'incident'),
  ('aaaaaaaa-1111-1111-1111-aaaaaaaa1111', 'Handled emergency calmly', 'commendation');

-- =====================
-- STAFF NOTES
-- =====================
INSERT INTO staff_notes (staff_id, note, status, created_by) VALUES
  ('cccccccc-3333-3333-3333-cccccccc3333', 'Missing PPE on Tuesday shift', 'needs_attention', 'bbbb2222-2222-bbbb-2222-bbbbbbbb2222'),
  ('aaaaaaaa-1111-1111-1111-aaaaaaaa1111', 'Excellent customer feedback', 'ok', 'bbbb2222-2222-bbbb-2222-bbbbbbbb2222');

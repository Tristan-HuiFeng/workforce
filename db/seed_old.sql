-- =========================================================
-- Fixed Seed Data for Workforce Compliance & Scheduling Assistant
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
INSERT INTO users (id, email, password_hash, role) VALUES
  ('aaaa1111-1111-aaaa-1111-aaaaaaaa1111', 'alice@company.com', '$2b$12$ruKupbD8Lye61389NAXqNObxLHsG.oyzA8/gPy2WbZTztESdU2k36', 'manager'),
  ('bbbb2222-2222-bbbb-2222-bbbbbbbb2222', 'bob@company.com', '$2b$12$ruKupbD8Lye61389NAXqNObxLHsG.oyzA8/gPy2WbZTztESdU2k36', 'supervisor'),
  ('cccc3333-3333-cccc-3333-cccccccc3333', 'carol@company.com', '$2b$12$ruKupbD8Lye61389NAXqNObxLHsG.oyzA8/gPy2WbZTztESdU2k36', 'staff'),
  ('dddd4444-4444-dddd-4444-dddddddd4444', 'dave@company.com', '$2b$12$ruKupbD8Lye61389NAXqNObxLHsG.oyzA8/gPy2WbZTztESdU2k36', 'staff'),
  ('eeee5555-5555-eeee-5555-eeeeeeee5555', 'erin@company.com', '$2b$12$ruKupbD8Lye61389NAXqNObxLHsG.oyzA8/gPy2WbZTztESdU2k36', 'staff');
  ('ffff6666-6666-ffff-6666-ffffffff6666', 'dan@company.com', '$2b$12$ruKupbD8Lye61389NAXqNObxLHsG.oyzA8/gPy2WbZTztESdU2k36', 'staff');

-- =====================
-- JOB ROLES
-- =====================
INSERT INTO job_roles (id, name) VALUES
  ('r1111111-1111-r111-1111-111111111111', 'Security Guard'),
  ('r2222222-2222-r222-2222-222222222222', 'Cleaner'),
  ('r3333333-3333-r333-3333-333333333333', 'Technician');

-- =====================
-- STAFF
-- =====================
INSERT INTO staff (id, user_id, role_id, full_name) VALUES
  ('s1111111-1111-s111-1111-111111111111', 'cccc3333-3333-cccc-3333-cccccccc3333', 'r1111111-1111-r111-1111-111111111111', 'Carol Smith'),
  ('s2222222-2222-s222-2222-222222222222', 'dddd4444-4444-dddd-4444-dddddddd4444', 'r2222222-2222-r222-2222-222222222222', 'Dave Johnson'),
  ('s3333333-3333-s333-3333-333333333333', 'eeee5555-5555-eeee-5555-eeeeeeee5555', 'r1111111-1111-r111-1111-111111111111', 'Erin Lee'),
  ('s4444444-4444-s444-4444-444444444444', 'bbbb2222-2222-bbbb-2222-bbbbbbbb2222', 'r3333333-3333-r333-3333-333333333333', 'Bob Supervisor'),
  ('s5555555-5555-s555-5555-555555555555', 'ffff6666-6666-ffff-6666-ffffffff6666', 'r3333333-3333-r333-3333-333333333333', 'Dan Tan');

-- =====================
-- STAFF ↔ SITES
-- =====================
INSERT INTO staff_sites (staff_id, site_id) VALUES
  ('s1111111-1111-s111-1111-111111111111', '11111111-aaaa-1111-aaaa-111111111111'),
  ('s2222222-2222-s222-2222-222222222222', '11111111-aaaa-1111-aaaa-111111111111'),
  ('s3333333-3333-s333-3333-333333333333', '22222222-bbbb-2222-bbbb-222222222222'),
  ('s4444444-4444-s444-4444-444444444444', '11111111-aaaa-1111-aaaa-111111111111'),
  ('s5555555-5555-s555-5555-555555555555', '22222222-bbbb-2222-bbbb-222222222222');

-- =====================
-- CERTIFICATIONS
-- =====================
INSERT INTO certifications (id, name, description) VALUES
  ('c1111111-1111-c111-1111-111111111111', 'Security License', 'Mandatory for Security'),
  ('c2222222-2222-c222-2222-222222222222', 'First Aid', 'Mandatory for all'),
  ('c3333333-3333-c333-3333-333333333333', 'Night Shift Clearance', 'Required for night shifts');

-- =====================
-- CERTIFICATION_ROLES
-- =====================
INSERT INTO certification_roles (certification_id, role_id) VALUES
  ('c1111111-1111-c111-1111-111111111111', 'r1111111-1111-r111-1111-111111111111'),
  ('c2222222-2222-c222-2222-222222222222', 'r1111111-1111-r111-1111-111111111111'),
  ('c2222222-2222-c222-2222-222222222222', 'r3333333-3333-r333-3333-333333333333');

-- =====================
-- STAFF CERTIFICATIONS
-- =====================
INSERT INTO staff_certifications (staff_id, certification_id, expires_at, status) VALUES
  ('s1111111-1111-s111-1111-111111111111', 'c1111111-1111-c111-1111-111111111111', CURRENT_DATE + INTERVAL '120 days', 'ok'),
  ('s3333333-3333-s333-3333-333333333333', 'c1111111-1111-c111-1111-111111111111', CURRENT_DATE + INTERVAL '15 days', 'needs_attention');

-- =====================
-- SHIFTS
-- =====================
INSERT INTO shifts (id, site_id, shift_date, shift_type, start_time, end_time) VALUES
  ('sh111111-1111-sh111-1111-111111111111', '11111111-aaaa-1111-aaaa-111111111111', CURRENT_DATE, 'morning', CURRENT_DATE + TIME '08:00', CURRENT_DATE + TIME '16:00'),
  ('sh222222-2222-sh222-2222-222222222222', '11111111-aaaa-1111-aaaa-111111111111', CURRENT_DATE, 'night',  CURRENT_DATE + TIME '22:00', (CURRENT_DATE + INTERVAL '1 day') + TIME '06:00');

-- =====================
-- SHIFT ASSIGNMENTS
-- =====================
INSERT INTO shift_assignments (shift_id, staff_id) VALUES
  ('sh111111-1111-sh111-1111-111111111111', 's1111111-1111-s111-1111-111111111111'),
  ('sh222222-2222-sh222-2222-222222222222', 's3333333-3333-s333-3333-333333333333');

-- =====================
-- INCIDENTS
-- =====================
INSERT INTO incidents (staff_id, description, type) VALUES
  ('s1111111-1111-s111-1111-111111111111', 'Arrived late to shift', 'incident'),
  ('s1111111-1111-s111-1111-111111111111', 'Handled emergency calmly', 'commendation');

-- =====================
-- STAFF NOTES
-- =====================
INSERT INTO staff_notes (staff_id, note, status, created_by) VALUES
  ('s3333333-3333-s333-3333-333333333333', 'Missing PPE on Tuesday shift', 'needs_attention', 'bbbb2222-2222-bbbb-2222-bbbbbbbb2222'),
  ('s1111111-1111-s111-1111-111111111111', 'Excellent customer feedback', 'ok', 'bbbb2222-2222-bbbb-2222-bbbbbbbb2222');

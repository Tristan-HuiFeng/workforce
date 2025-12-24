import uuid
from datetime import datetime, timedelta, timezone
from src.db.models.shift import Shift
from src.db.models.user import UserRole
from src.db.models.user import User
from src.db.models.staff import Staff

def test_list_shifts_manager(manager_client):
    response = manager_client.get("/shifts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_shifts_staff(staff_client):
    response = staff_client.get("/shifts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_shift_manager(manager_client, db):

    # Login simulation or token bypass depends on your auth setup
    shift_data = {
        "site_id": "11111111-aaaa-1111-aaaa-111111111111",
        "shift_date": datetime.now(timezone.utc).date().isoformat(),
        "shift_type": "morning",
        "start_time": datetime.now(timezone.utc).isoformat(),
        "end_time": (datetime.now(timezone.utc) + timedelta(hours=8)).isoformat()
    }
    response = manager_client.post("/shifts/", json=shift_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data

    shift_id = data["id"]

    # Cleanup
    db.query(Shift).filter(Shift.id == shift_id).delete()
    db.commit()

def test_create_shift_manager_no_site(manager_client, db):

    # Login simulation or token bypass depends on your auth setup
    shift_data = {
        "site_id": "11111111-aaaa-1111-aaaa-111111111112",
        "shift_date": datetime.now(timezone.utc).date().isoformat(),
        "shift_type": "morning",
        "start_time": datetime.now(timezone.utc).isoformat(),
        "end_time": (datetime.now(timezone.utc) + timedelta(hours=8)).isoformat()
    }
    response = manager_client.post("/shifts/", json=shift_data)
    assert response.status_code == 400

def test_create_shift_staff(staff_client, db):
    shift_data = {
        "site_id": "11111111-aaaa-1111-aaaa-111111111111",
        "shift_date": datetime.now(timezone.utc).date().isoformat(),
        "shift_type": "morning",
        "start_time": datetime.now(timezone.utc).isoformat(),
        "end_time": (datetime.now(timezone.utc) + timedelta(hours=8)).isoformat()
    }
    response = staff_client.post("/shifts/", json=shift_data)
    assert response.status_code == 403

def test_shift_overlap(manager_client, db):
    # Create an initial shift
    shift_data_1 = {
        "site_id": "11111111-aaaa-1111-aaaa-111111111111",
        "shift_date": "2025-12-25",
        "shift_type": "morning",
        "start_time": "2025-12-25T08:00:00Z",
        "end_time": "2025-12-25T16:00:00Z"
    }
    response_1 = manager_client.post("/shifts/", json=shift_data_1)
    assert response_1.status_code == 200
    shift_id_1 = response_1.json()["id"]

    # Attempt to create overlapping shift
    shift_data_2 = {
        "site_id": "11111111-aaaa-1111-aaaa-111111111111",
        "shift_date": "2025-12-25",
        "shift_type": "morning",
        "start_time": "2025-12-25T12:00:00Z",  # overlaps
        "end_time": "2025-12-25T20:00:00Z"
    }
    response_2 = manager_client.post("/shifts/", json=shift_data_2)
    assert response_2.status_code == 400  # should reject
    assert "overlap" in response_2.json()["detail"].lower()

    db.query(Shift).filter(Shift.id == shift_id_1).delete()
    db.commit()

def test_list_shifts_filters(manager_client):
    response = manager_client.get("/shifts/?site_id=11111111-aaaa-1111-aaaa-111111111111")
    assert response.status_code == 200
    for shift in response.json():
        assert shift["site_id"] == "11111111-aaaa-1111-aaaa-111111111111"

# def test_assign_staff_to_shift(manager_client, db):
#     # Create shift
#     shift_data = {
#         "site_id": "11111111-aaaa-1111-aaaa-111111111111",
#         "shift_date": "2025-12-26",
#         "shift_type": "morning",
#         "start_time": "2025-12-26T08:00:00Z",
#         "end_time": "2025-12-26T16:00:00Z"
#     }
#     shift_resp = manager_client.post("/shifts/", json=shift_data)
#     shift_id = shift_resp.json()["id"]

#     # Assign staff
#     staff_id = "cccccccc-3333-3333-3333-cccccccc3333"  # existing staff
#     assign_resp = manager_client.post(f"/shifts/{shift_id}/assign", json={"staff_id": staff_id})
#     assert assign_resp.status_code == 200

#     # Attempt to assign same staff to overlapping shift
#     overlapping_shift_resp = manager_client.post("/shifts/", json={
#         "site_id": "11111111-aaaa-1111-aaaa-111111111111",
#         "shift_date": "2025-12-26",
#         "shift_type": "afternoon",
#         "start_time": "2025-12-26T12:00:00Z",
#         "end_time": "2025-12-26T20:00:00Z"
#     })
#     overlapping_shift_id = overlapping_shift_resp.json()["id"]
#     resp_overlap_assign = manager_client.post(f"/shifts/{overlapping_shift_id}/assign", json={"staff_id": staff_id})
#     assert resp_overlap_assign.status_code == 400
#     assert "overlap" in resp_overlap_assign.json()["detail"].lower()

# def test_assign_staff_wrong_site(manager_client):
#     shift_data = {
#         "site_id": "22222222-bbbb-2222-bbbb-222222222222",  # different site
#         "shift_date": "2025-12-27",
#         "shift_type": "morning",
#         "start_time": "2025-12-27T08:00:00Z",
#         "end_time": "2025-12-27T16:00:00Z"
#     }
#     shift_resp = manager_client.post("/shifts/", json=shift_data)
#     shift_id = shift_resp.json()["id"]

#     staff_id = "aaaaaaaa-1111-1111-1111-aaaaaaaa1111"  # linked to site 11111111-aaaa
#     resp = manager_client.post(f"/shifts/{shift_id}/assign", json={"staff_id": staff_id})
#     assert resp.status_code == 400
#     assert "site" in resp.json()["detail"].lower()


# def test_invalid_shift_times(manager_client):
#     shift_data = {
#         "site_id": "11111111-aaaa-1111-aaaa-111111111111",
#         "shift_date": "2025-12-28",
#         "shift_type": "morning",
#         "start_time": "2025-12-28T16:00:00Z",
#         "end_time": "2025-12-28T08:00:00Z"
#     }
#     response = manager_client.post("/shifts/", json=shift_data)
#     assert response.status_code == 400
#     assert "start" in response.json()["detail"].lower()

# def test_assign_staff_validation(client, db, sample_shift):
#     from src.db.models.staff import Staff
#     # Create staff
#     staff_id = uuid.uuid4()
#     staff = Staff(id=staff_id, user_id=uuid.uuid4(), role_id=str(uuid.uuid4()), full_name="Test Staff")
#     db.add(staff)
#     db.commit()
    
#     # Assign staff to shift
#     assign_data = {"shift_id": str(sample_shift.id), "staff_id": str(staff.id)}
#     response = client.post("/shifts/assign", json=assign_data)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["shift_id"] == str(sample_shift.id)
#     assert data["staff_id"] == str(staff.id)

# def test_assign_staff_overlap(client, db, sample_shift):
#     from src.db.models.staff import Staff
#     staff_id = uuid.uuid4()
#     staff = Staff(id=staff_id, user_id=uuid.uuid4(), role_id=str(uuid.uuid4()), full_name="Overlap Staff")
#     db.add(staff)
#     db.commit()
    
#     # First assignment
#     assign_data = {"shift_id": str(sample_shift.id), "staff_id": str(staff.id)}
#     client.post("/shifts/assign", json=assign_data)

#     # Attempt overlapping assignment
#     assign_data2 = {"shift_id": str(sample_shift.id), "staff_id": str(staff.id)}
#     response = client.post("/shifts/assign", json=assign_data2)
#     assert response.status_code == 400
#     assert "overlapping" in response.json()["detail"].lower()

# def test_assign_staff_missing_certification(client, db, sample_shift):
#     from src.db.models.staff import Staff
#     import uuid

#     # Create staff WITHOUT certification
#     staff = Staff(
#         id=uuid.uuid4(),
#         user_id=uuid.uuid4(),
#         role_id=uuid.uuid4(),
#         full_name="No Cert Staff"
#     )
#     db.add(staff)
#     db.commit()

#     payload = {
#         "shift_id": str(sample_shift.id),
#         "staff_id": str(staff.id)
#     }

#     response = client.post("/shifts/assign", json=payload)
#     assert response.status_code == 400
#     assert "certification" in response.json()["detail"].lower()

# from datetime import datetime, timedelta

# def test_assign_staff_expired_certification(client, db, sample_shift):
#     from src.db.models.staff import Staff
#     from src.db.models.staff_certification import StaffCertification
#     import uuid

#     staff = Staff(
#         id=uuid.uuid4(),
#         user_id=uuid.uuid4(),
#         role_id=uuid.uuid4(),
#         full_name="Expired Cert Staff"
#     )
#     db.add(staff)
#     db.commit()

#     expired_cert = StaffCertification(
#         staff_id=staff.id,
#         certification_id=uuid.uuid4(),
#         expires_at=datetime.utcnow() - timedelta(days=1),
#         status="expired"
#     )
#     db.add(expired_cert)
#     db.commit()

#     payload = {
#         "shift_id": str(sample_shift.id),
#         "staff_id": str(staff.id)
#     }

#     response = client.post("/shifts/assign", json=payload)
#     assert response.status_code == 400
#     assert "expired" in response.json()["detail"].lower()

# def test_assign_staff_weekly_overtime(client, db):
#     from src.db.models.shift import Shift, ShiftTypeEnum
#     from src.db.models.staff import Staff
#     from src.db.models.shift_assignment import ShiftAssignment
#     from src.db.models.site import Site
#     import uuid
#     from datetime import datetime, timedelta

#     site = Site(id=uuid.uuid4(), name="OT Site", location="X")
#     db.add(site)
#     db.commit()

#     staff = Staff(
#         id=uuid.uuid4(),
#         user_id=uuid.uuid4(),
#         role_id=uuid.uuid4(),
#         full_name="Overtime Staff"
#     )
#     db.add(staff)
#     db.commit()

#     # Create 5 shifts (8h each = 40h)
#     for i in range(5):
#         shift = Shift(
#             id=uuid.uuid4(),
#             site_id=site.id,
#             shift_date=datetime.utcnow().date() - timedelta(days=i),
#             shift_type=ShiftTypeEnum.morning,
#             start_time=datetime.utcnow(),
#             end_time=datetime.utcnow() + timedelta(hours=8)
#         )
#         db.add(shift)
#         db.commit()

#         assignment = ShiftAssignment(shift_id=shift.id, staff_id=staff.id)
#         db.add(assignment)
#         db.commit()

#     # 6th shift → should exceed weekly hours
#     extra_shift = Shift(
#         id=uuid.uuid4(),
#         site_id=site.id,
#         shift_date=datetime.utcnow().date(),
#         shift_type=ShiftTypeEnum.morning,
#         start_time=datetime.utcnow(),
#         end_time=datetime.utcnow() + timedelta(hours=8)
#     )
#     db.add(extra_shift)
#     db.commit()

#     payload = {
#         "shift_id": str(extra_shift.id),
#         "staff_id": str(staff.id)
#     }

#     response = client.post("/shifts/assign", json=payload)
#     assert response.status_code == 400
#     assert "overtime" in response.json()["detail"].lower()

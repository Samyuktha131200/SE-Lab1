from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints
)


def test_invalid_groups():
    try:
        process_ride_admissions("invalid", 5)
        assert False
    except ValueError:
        pass


def test_negative_fee():
    try:
        process_ride_admissions([], -1)
        assert False
    except ValueError:
        pass


def test_closed_ride():
    result = process_ride_admissions(
        [{"is_open": False}], 5
    )
    assert result["status"] == "ZERO_ADMISSIONS"


def test_all_ride_types():
    groups = [
        {"is_open": True, "ride_type": "roller_coaster",
         "patrons": [{"height_cm": 150}]},
        {"is_open": True, "ride_type": "water_ride",
         "patrons": [{"height_cm": 150}]},
        {"is_open": True, "ride_type": "family",
         "patrons": [{"height_cm": 150}]},
        {"is_open": True, "ride_type": "unknown",
         "patrons": [{"height_cm": 150}]}
    ]
    process_ride_admissions(groups, 5)


def test_patron_conditions():
    groups = [
        {"is_open": True, "ride_type": "family",
         "patrons": [
             {"height_cm": 0},
             {"height_cm": 100},
             {"height_cm": 130, "is_child": True},
             {"height_cm": 150, "health_warning": True},
             {"height_cm": 150}
         ]}
    ]
    process_ride_admissions(groups, 5)


def test_roller_coaster_health_warning():
    groups = [
        {"is_open": True, "ride_type": "roller_coaster",
         "has_fast_lane": True,
         "patrons": [
             {"height_cm": 150, "health_warning": True},
             {"height_cm": 160}
         ]}
    ]
    process_ride_admissions(groups, 5)


def test_fast_lane():
    groups = [
        {"is_open": True, "ride_type": "family",
         "has_fast_lane": True,
         "patrons": [{"height_cm": 150}]}
    ]
    result = process_ride_admissions(groups, 5)
    assert result["total_revenue"] == 15.0


def test_safety_audit():
    groups = [
        {"is_open": True, "ride_type": "unknown"}
        for _ in range(5)
    ]
    result = process_ride_admissions(groups, 5)
    assert result["status"] == "SAFETY_AUDIT"


def test_completed_status():
    result = process_ride_admissions(
        [{"is_open": True, "ride_type": "family",
          "patrons": [{"height_cm": 150}]}], 5
    )
    assert result["status"] == "COMPLETED"


def test_restraints_no_data():
    assert inspect_safety_restraints([]) == "NO_DATA"


def test_restraints_emergency():
    assert inspect_safety_restraints([[1, 0, 0]]) == "EMERGENCY_LOCK"


def test_restraints_safe():
    assert inspect_safety_restraints([[1, 0, 1]]) == "SAFE"
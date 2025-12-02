# app/services/repair_engine.py

from sqlmodel import Session
from app.models.repair_models import RepairRequest


class RepairEngine:

    # FULL LIST OF 29 CATEGORIES
    REPAIR_CATEGORIES = [
        "Bathroom and Toilet",
        "Kitchen",
        "Heating and boiler",
        "Water and Leaks",
        "Doors, Garages and Locks",
        "Internal floors, walls and ceilings",
        "Lighting",
        "Window",
        "Exterior and Garden",
        "Laundry",
        "Furniture",
        "Electricity",
        "Hot Water",
        "Alarms and Smoke Detectors",
        "Pests/Vermin",
        "Roof",
        "Communal/Shared Facilities",
        "Audiovisual",
        "Utility Meters",
        "Internet",
        "Stairs",
        "Property services",
        "Smell Gas?",
        "Air Conditioning",
        "Smell Oil?",
        "Fire",
        "Capex",
        "Property Inspection",
        "Other"
    ]

    # SAVE REPAIR REQUEST TO DB
    def save_request(self, db: Session, user_id: int, data: dict) -> RepairRequest:
        req = RepairRequest(
            user_id=user_id,
            category=data["category"],
            address=data["address"],
            description=data["description"],
        )
        db.add(req)
        db.commit()
        db.refresh(req)
        return req

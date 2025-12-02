# app/services/rental_engine.py

import json
import os
from sqlmodel import Session
from app.models.rental_models import RentalSearch, RentalMatch
from typing import List, Dict


class RentalEngine:

    def __init__(self):
        # Build a robust path to properties.json
        base_dir = os.path.dirname(os.path.dirname(__file__))  # .../real_estate_ai/app
        data_path = os.path.join(base_dir, "data", "properties.json")

        self.properties = []

        if os.path.exists(data_path):
            try:
                with open(data_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        self.properties = json.loads(content)
                    else:
                        print("⚠️ properties.json is empty. No rental properties loaded.")
            except json.JSONDecodeError as e:
                print("❌ JSON error in properties.json:", e)
                self.properties = []
        else:
            print("⚠️ properties.json not found at:", data_path)

    # -------------------------------------------------------------
    # SCORE PROPERTY AGAINST REQUIREMENTS
    # -------------------------------------------------------------
    def _score(self, req: dict, prop: dict) -> int:
        score = 0

        # Location
        if req.get("location"):
            if req["location"].lower() in prop["location"].lower():
                score += 30

        # Property Type
        if req.get("property_type"):
            if req["property_type"] in prop["property_type"].lower():
                score += 20

        # Bedrooms
        if req.get("bedrooms"):
            if prop["bedrooms"] >= req["bedrooms"]:
                score += 20

        # Budget
        if req.get("budget"):
            if prop["price_per_month"] <= req["budget"]:
                score += 25

        # Furnished
        if req.get("furnished") is not None:
            if req["furnished"] == prop["furnished"]:
                score += 10

        # Garden
        if req.get("garden"):
            if prop.get("has_garden"):
                score += 10

        # Parking
        if req.get("parking"):
            if prop.get("parking"):
                score += 10

        return score

    # -------------------------------------------------------------
    # FIND MATCHES
    # -------------------------------------------------------------
    def find_matches(self, requirements: dict) -> List[Dict]:
        if not self.properties:
            # No properties loaded
            return []

        results = []

        for p in self.properties:
            score = self._score(requirements, p)
            if score > 0:
                prop = p.copy()
                prop["score"] = score
                results.append(prop)

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:6]

    # -------------------------------------------------------------
    # SAVE RENTAL SEARCH REQUEST + MATCHES TO DB
    # -------------------------------------------------------------
    def save_search(self, db: Session, user_id: int, req: dict, results: list) -> RentalSearch:
        search = RentalSearch(
            user_id=user_id,
            location=req.get("location"),
            bedrooms=req.get("bedrooms"),
            property_type=req.get("property_type"),
            furnished=req.get("furnished"),
            budget=req.get("budget"),
            garden=req.get("garden"),
            parking=req.get("parking"),
        )
        db.add(search)
        db.commit()
        db.refresh(search)

        for r in results:
            match = RentalMatch(
                search_id=search.id,
                property_id=r["id"],
                title=r["title"],
                location=r["location"],
                price_per_month=r["price_per_month"],
                bedrooms=r["bedrooms"],
                furnished=r["furnished"],
                has_garden=r.get("has_garden"),
                parking=r.get("parking"),
                url=r["url"],
                score=r.get("score"),
            )
            db.add(match)

        db.commit()
        return search

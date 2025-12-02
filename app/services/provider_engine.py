# app/services/provider_engine.py

import json
from typing import List
from app.models.provider_models import ServiceProvider
from sqlmodel import Session, select


class ProviderEngine:

    def __init__(self):
        try:
            with open("app/data/service_providers.json", "r") as f:
                self.providers_data = json.load(f)
        except:
            self.providers_data = []

    # MATCH PROVIDERS BY CATEGORY
    def find_matching(self, category: str) -> List[ServiceProvider]:

        results = []

        for p in self.providers_data:
            if p["category"].lower() == category.lower():
                provider = ServiceProvider(
                    category=p["category"],
                    name=p["name"],
                    phone=p.get("phone"),
                    email=p.get("email"),
                    rating=p.get("rating", 4.5)
                )
                results.append(provider)

        # fallback: show all providers if none match
        if not results:
            for p in self.providers_data[:5]:
                provider = ServiceProvider(
                    category=p["category"],
                    name=p["name"],
                    phone=p.get("phone"),
                    email=p.get("email"),
                    rating=p.get("rating", 4.5)
                )
                results.append(provider)

        return results

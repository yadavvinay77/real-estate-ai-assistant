# app/services/conversation_engine.py

from app.models.chat_models import (
    ChatBotResponse,
    ChatClientMessage,
    ChatOption,
    ChatPropertyCard,
)

from app.models.user_models import User
from app.services.rental_engine import RentalEngine
from app.services.repair_engine import RepairEngine
from app.services.provider_engine import ProviderEngine
from app.services.rag_engine import RAGEngine
from app.services.ollama_client import OllamaClient

from sqlmodel import select
from app.database import Session


class ConversationEngine:

    def __init__(self):
        self.state = {}
        self.rag = RAGEngine()
        self.rental = RentalEngine()
        self.repair = RepairEngine()
        self.providers = ProviderEngine()
        self.ollama = OllamaClient()

    # -------------------------------------------------------------
    # INTERNAL HELPERS
    # -------------------------------------------------------------
    def _get_state(self, session_id: str):
        if session_id not in self.state:
            self.state[session_id] = {
                "stage": "start",
                "user_id": None,
                "history": "",
                "rental": {},
                "repair": {},
            }
        return self.state[session_id]

    def _set_stage(self, st, stage: str):
        st["stage"] = stage

    # -------------------------------------------------------------
    # LLM + RAG
    # -------------------------------------------------------------
    def ask_llm(self, user_message: str, st) -> str:

        rag_context = self.rag.answer(user_message)

        prompt = f"""
You are a professional Real Estate & Property Services Assistant.

RULES:
- NEVER hallucinate.
- If unsure, ask a follow-up question.
- Keep answers short and helpful.
- Use RAG context below.

RAG context:
{rag_context}

Conversation history:
{st.get("history", "")}

User message:
{user_message}

Your response:
"""

        reply = self.ollama.generate(prompt)
        st["history"] += f"User: {user_message}\nAssistant: {reply}\n"
        return reply

    # -------------------------------------------------------------
    # USER CREATION
    # -------------------------------------------------------------
    def _ensure_user(self, db: Session, st, name, phone=None, email=None):
        if st.get("user_id"):
            return st["user_id"]

        q = select(User).where(User.phone == phone)
        user = db.exec(q).first()

        if not user:
            user = User(name=name, phone=phone, email=email)
            db.add(user)
            db.commit()
            db.refresh(user)

        st["user_id"] = user.id
        return user.id

    # -------------------------------------------------------------
    # MAIN ENTRY POINT
    # -------------------------------------------------------------
    def handle(self, session_id: str, message: ChatClientMessage, db: Session):

        st = self._get_state(session_id)
        text = message.text.strip()
        stage = st["stage"].lower()

        # ---------------------------------------------------------
        # UNIVERSAL MAIN MENU RESET
        # ---------------------------------------------------------
        if text.lower() in ["menu", "main menu", "restart", "home"]:
            self._set_stage(st, "choose_intent")
            return ChatBotResponse(
                text="What would you like help with today?",
                options=[
                    ChatOption(label="🏠 Rent a Property", value="rent"),
                    ChatOption(label="🛠 Request a Repair / Service", value="repair"),
                    ChatOption(label="💬 General Questions", value="general"),
                ]
            )

        # ---------------------------------------------------------
        # ONBOARDING FLOW
        # ---------------------------------------------------------
        if stage == "start":
            self._set_stage(st, "ask_name")
            return ChatBotResponse(text="👋 Hi! I’m your Property Assistant.\nWhat’s your *name*?")

        if stage == "ask_name":
            st["user_name"] = text
            self._set_stage(st, "ask_phone")
            return ChatBotResponse(text=f"Nice to meet you, {text}! 📱\nYour *phone number*?")

        if stage == "ask_phone":
            st["user_phone"] = text
            self._set_stage(st, "ask_email")
            return ChatBotResponse(text="Great! What’s your *email address*?")

        if stage == "ask_email":
            st["user_email"] = text

            self._ensure_user(db, st, st["user_name"], st["user_phone"], st["user_email"])

            self._set_stage(st, "choose_intent")
            return ChatBotResponse(
                text="Thanks! What would you like help with today?",
                options=[
                    ChatOption(label="🏠 Rent a Property", value="rent"),
                    ChatOption(label="🛠 Request a Repair / Service", value="repair"),
                    ChatOption(label="💬 General Questions", value="general"),
                ]
            )

        # ---------------------------------------------------------
        # INTENT SELECTION
        # ---------------------------------------------------------
        if stage == "choose_intent":

            low = text.lower()

            # NEW SEARCH
            if low in ["new search", "rent again"]:
                st["rental"] = {}
                self._set_stage(st, "rental_location")
                return ChatBotResponse(text="Sure! Which *area or postcode* are you interested in?")

            # RENT
            if "rent" in low:
                st["rental"] = {}
                self._set_stage(st, "rental_location")
                return ChatBotResponse(text="Great! Which *area or postcode* are you interested in?")

            # REPAIR
            if "repair" in low or "service" in low:
                st["repair"] = {}
                self._set_stage(st, "repair_category")
                return ChatBotResponse(
                    text="What type of issue are you having?",
                    options=[ChatOption(label=f"🔧 {c}", value=c) for c in self.repair.REPAIR_CATEGORIES]
                )

            # GENERAL QUESTIONS → LLM
            if "general" in low:
                return ChatBotResponse(text=self.ask_llm(text, st))

            return ChatBotResponse(text="Please choose an option.")

        # -------------------- RENTAL LOGIC ------------------------
        if stage.startswith("rental"):
            return self._handle_rental(st, message, db)

        # -------------------- REPAIR LOGIC ------------------------
        if stage.startswith("repair"):
            return self._handle_repair(st, message, db)

        # FALLBACK → LLM
        return ChatBotResponse(text=self.ask_llm(text, st))

    # -------------------------------------------------------------
    # RENTAL FLOW HANDLER
    # -------------------------------------------------------------
    def _handle_rental(self, st, message, db):
        text = message.text.strip()

        # LOCATION
        if st["stage"] == "rental_location":
            st["rental"]["location"] = text
            self._set_stage(st, "rental_property_type")
            return ChatBotResponse(
                text="What type of property?",
                options=[
                    ChatOption(label="🏡 House", value="house"),
                    ChatOption(label="🏢 Flat", value="flat"),
                    ChatOption(label="🏙 Apartment", value="apartment"),
                    ChatOption(label="🏬 Studio", value="studio"),
                ]
            )

        # PROPERTY TYPE
        if st["stage"] == "rental_property_type":
            st["rental"]["property_type"] = text.lower()
            self._set_stage(st, "rental_bedrooms")
            return ChatBotResponse(
                text="How many bedrooms?",
                options=[ChatOption(label=str(i), value=str(i)) for i in [1, 2, 3, 4]]
            )

        # BEDROOM COUNT
        if st["stage"] == "rental_bedrooms":
            try:
                st["rental"]["bedrooms"] = int(text.replace("+", ""))
            except:
                st["rental"]["bedrooms"] = 1
            self._set_stage(st, "rental_budget")
            return ChatBotResponse(text="Your *maximum monthly budget*?")

        # BUDGET
        if st["stage"] == "rental_budget":
            digits = ''.join([d for d in text if d.isdigit()])
            st["rental"]["budget"] = int(digits) if digits else None
            self._set_stage(st, "rental_furnished")
            return ChatBotResponse(
                text="Do you prefer furnished?",
                options=[
                    ChatOption(label="✅ Furnished", value="furnished"),
                    ChatOption(label="❌ Unfurnished", value="unfurnished"),
                    ChatOption(label="🤷 Doesn't matter", value="none"),
                ]
            )

        # FURNISHED
        if st["stage"] == "rental_furnished":
            if "furnished" in text.lower():
                st["rental"]["furnished"] = True
            elif "unfurnished" in text.lower():
                st["rental"]["furnished"] = False
            else:
                st["rental"]["furnished"] = None

            self._set_stage(st, "rental_garden")
            return ChatBotResponse(
                text="Garden needed?",
                options=[
                    ChatOption(label="🌿 Yes", value="yes"),
                    ChatOption(label="❌ No", value="no"),
                ]
            )

        # GARDEN
        if st["stage"] == "rental_garden":
            st["rental"]["garden"] = ("yes" in text.lower())
            self._set_stage(st, "rental_parking")
            return ChatBotResponse(
                text="Parking needed?",
                options=[
                    ChatOption(label="🚗 Yes", value="yes"),
                    ChatOption(label="❌ No", value="no"),
                ]
            )

        # FINAL STEP → MATCH
        if st["stage"] == "rental_parking":
            st["rental"]["parking"] = ("yes" in text.lower())

            results = self.rental.find_matches(st["rental"])
            self.rental.save_search(db, st["user_id"], st["rental"], results)

            cards = [
                ChatPropertyCard(
                    id=p["id"],
                    title=p["title"],
                    price_per_month=p["price_per_month"],
                    location=p["location"],
                    bedrooms=p["bedrooms"],
                    furnished=p["furnished"],
                    has_garden=p.get("has_garden"),
                    parking=p.get("parking"),
                    url=p["url"],
                    score=p.get("score"),
                ) for p in results
            ]

            self._set_stage(st, "choose_intent")

            return ChatBotResponse(
                text="Here are your matched properties:",
                properties=cards,
                options=[
                    ChatOption(label="🔎 New Search", value="new search"),
                    ChatOption(label="🏠 Main Menu", value="menu"),
                ]
            )

        return ChatBotResponse(text="I didn't understand that.")

    # -------------------------------------------------------------
    # REPAIR FLOW HANDLER
    # -------------------------------------------------------------
    def _handle_repair(self, st, message, db):

        text = message.text.strip().lower()

        # CATEGORY
        if st["stage"] == "repair_category":
            st["repair"]["category"] = message.text
            self._set_stage(st, "repair_address")
            return ChatBotResponse(text="What is the *address* of the property?")

        # ADDRESS
        if st["stage"] == "repair_address":
            st["repair"]["address"] = message.text
            self._set_stage(st, "repair_description")
            return ChatBotResponse(text="Please describe the issue in detail.")

        # DESCRIPTION
        if st["stage"] == "repair_description":

            st["repair"]["description"] = message.text

            providers = self.providers.find_matching(st["repair"]["category"])

            options = [
                ChatOption(
                    label=f"📞 {p.name} ({p.rating}⭐)",
                    value=p.name
                )
                for p in providers
            ]

            self.repair.save_request(db, st["user_id"], st["repair"])
            self._set_stage(st, "repair_provider_confirm")

            return ChatBotResponse(
                text="Here are recommended service providers.\nYou may choose one or type 'done'.",
                options=options
            )

        # PROVIDER CONFIRMATION
        if st["stage"] == "repair_provider_confirm":

            endings = ["done", "thanks", "thank you", "ok", "okay", "fine", "no", "no thanks"]

            if text in endings:
                self._set_stage(st, "choose_intent")
                return ChatBotResponse(
                    text="Your repair request is logged. Anything else?",
                    options=[
                        ChatOption(label="🏠 Rent a Property", value="rent"),
                        ChatOption(label="🛠 Request Another Repair", value="repair"),
                        ChatOption(label="🏠 Main Menu", value="menu"),
                    ]
                )

            self._set_stage(st, "choose_intent")
            return ChatBotResponse(
                text=f"{message.text} has been noted! They may contact you soon.\nNeed anything else?",
                options=[
                    ChatOption(label="🏠 Rent a Property", value="rent"),
                    ChatOption(label="🛠 Request Another Repair", value="repair"),
                    ChatOption(label="🏠 Main Menu", value="menu"),
                ]
            )

        return ChatBotResponse(text="I didn't understand that.")

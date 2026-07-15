from enum import Enum
from datetime import datetime
from pydantic import model_validator, BaseModel, Field, ValidationError


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: str | None = Field(None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_contact_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError(
                "Strong signals (>7.0) should include received messages")
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 40)

    try:
        v_contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type="radio",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greeting from Zeta Reticuli"
        )

        print("Valid contact report:")
        print(f"ID: {v_contact.contact_id}")
        print(f"Type: {v_contact.contact_type.value}")
        print(f"Location: {v_contact.location}")
        print(f"Signal: {v_contact.signal_strength}/10")
        print(f"Duration: {v_contact.duration_minutes} minutes")
        print(f"Witnesses: {v_contact.witness_count}")
        print(f"Message: '{v_contact.message_received}'")

    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print()
    print("=" * 40)

    try:
        i_contact = AlienContact(
            contact_id="AC_INVALID",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type="telepathic",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greeting from Zeta Reticuli"
        )

        print("Valid contact report:")
        print(f"ID: {i_contact.contact_id}")
        print(f"Type: {i_contact.contact_type.value}")
        print(f"Location: {i_contact.location}")
        print(f"Signal: {i_contact.signal_strength}/10")
        print(f"Duration: {i_contact.duration_minutes} minutes")
        print(f"Witnesses: {i_contact.witness_count}")
        print(f"Message: '{i_contact.message_received}'")

    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()

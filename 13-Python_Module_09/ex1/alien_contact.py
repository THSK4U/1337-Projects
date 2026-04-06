from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(
        None, max_length=500
    )
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def custem_validation_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC" (Alien Contact)')
        if self.contact_type is ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (
            self.contact_type is ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if self.signal_strength > 7 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )

        return self


def main():
    print("Alien Contact Log Validation")
    print("=" * 40)
    try:
        valid_report: AlienContact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
        )

        print(f"""Valid contact report:
ID: {valid_report.contact_id}
Type: {valid_report.contact_type}
Location: {valid_report.location}
Signal: {valid_report.signal_strength}/10
Duration: {valid_report.duration_minutes} minutes
Witnesses: {valid_report.witness_count}
Message: {valid_report.message_received}
""")

        print("=" * 40)
        print("Expected validation error:")
        valid_report: AlienContact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=7.2,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli",
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"])


main()


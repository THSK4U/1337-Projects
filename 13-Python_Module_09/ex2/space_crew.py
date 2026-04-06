from enum import Enum
from pydantic import BaseModel, ValidationError, Field, model_validator
from datetime import datetime


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def custem_validation_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        has_commander_or_captain = False
        for member in self.crew:
            if member.rank in (Rank.COMMANDER, Rank.CAPTAIN):
                has_commander_or_captain = True
                break

        if not has_commander_or_captain:
            raise ValueError("Must have at least one Commander or Captain")

        experience_ = False
        if self.duration_days > 356:
            experience_count = sum(
                1 for exp in self.crew if exp.years_experience > 5
            )

        if (experience_count / len(self.crew) * 100) < 50:
            raise ValueError(
                "Long missions (> 365 days) need 50% experienced crew (5+ years)"
            )

        crews_is_active = False
        for member in self.crew:
            if not member.is_active:
                crews_is_active = True

        if crews_is_active:
            raise ValueError("All crew members must be active")

        return self


def main():
    crews = [
        {
            "member_id": "CM011",
            "name": "Emma Brown",
            "rank": "commander",
            "age": 49,
            "specialization": "Mission Command",
            "years_experience": 27,
            "is_active": True,
        },
        {
            "member_id": "CM012",
            "name": "John Hernandez",
            "rank": "lieutenant",
            "age": 36,
            "specialization": "Science Officer",
            "years_experience": 22,
            "is_active": True,
        },
        {
            "member_id": "CM013",
            "name": "Sofia Rodriguez",
            "rank": "commander",
            "age": 29,
            "specialization": "Life Support",
            "years_experience": 2,
            "is_active": True,
        },
        {
            "member_id": "CM014",
            "name": "Sofia Lopez",
            "rank": "lieutenant",
            "age": 44,
            "specialization": "Systems Analysis",
            "years_experience": 25,
            "is_active": True,
        },
    ]
    print("Space Mission Crew Validation")
    print("=" * 40)
    try:
        mission: SpaceMission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2028, 10, 1),
            duration_days=900,
            crew=crews,
            budget_millions=2500.0,
        )

        crew_lines = "\n".join(
            f"- {member.name} ({member.rank.value}) - {member.specialization}"
            for member in mission.crew
        )

        print(f"""Valid mission created:
Mission: {mission.mission_name}
ID: {mission.mission_id}
Destination: {mission.destination}
Duration: {mission.duration_days} days
Budget: ${mission.budget_millions}M
Crew size: {len(mission.crew)}
Crew members:
{crew_lines}
""")
    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print("=" * 40)
    print("Expected validation error:")
    try:
        crews_invalid = [
            {
                "member_id": "CM011",
                "name": "Emma Brown",
                "rank": "officer",
                "age": 49,
                "specialization": "Mission Command",
                "years_experience": 27,
                "is_active": True,
            }
        ]

        mission: SpaceMission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2028, 10, 1),
            duration_days=900,
            crew=crews_invalid,
            budget_millions=2500.0,
        )

    except ValidationError as e:
        print(e.errors()[0]["msg"])



main()


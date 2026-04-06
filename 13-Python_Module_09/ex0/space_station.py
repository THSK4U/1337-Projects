from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime = Field(le=datetime.now())
    is_operational: bool = Field(default=True)
    notes: str = Field(max_length=200)


def main() -> None:
    print(f"""Space Station Data Validation
{"=" * 40}
Valid station created:""")
    try:
        station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 3, 7),
            notes="Operational",
        )
        print(f"""ID: {station.station_id}
Name: {station.name}
Crew: {station.crew_size} people
Power: {station.power_level}%
Oxygen: {station.oxygen_level}%
Status: {station.notes}
""")
    except ValidationError as e:
        print(e)

    print(f"""{"=" * 40}
Expected validation error:""")
    try:
        station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=100,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 3, 7),
            notes="Operational",
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"])


main()


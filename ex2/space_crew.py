from enum import Enum
from datetime import datetime
from pydantic import model_validator, BaseModel, Field, ValidationError


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_commander = any(
            member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
            for member in self.crew
        )
        if not has_commander:
            raise ValueError(
                "Mission must have at least one Commander or Captain")

        experienced_crew = sum(
            1 for member in self.crew if member.years_experience >= 5
        )

        req_experienced = len(self.crew) / 2

        if self.duration_days > 365 and experienced_crew < req_experienced:
            raise ValueError(
                "Long missions need 50% experienced crew")

        for member in self.crew:
            if not member.is_active:
                raise ValueError("All crew members must be active")

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 40)

    try:
        v_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="CM01",
                    name="Sarah Connor",
                    rank="commander",
                    age=42,
                    specialization="Mission Command",
                    years_experience=25
                ),
                CrewMember(
                    member_id="CM02",
                    name="John Smith",
                    rank="lieutenant",
                    age=33,
                    specialization="Navigation",
                    years_experience=8
                ),
                CrewMember(
                    member_id="CM03",
                    name="Alice Johnson",
                    rank="officer",
                    age=28,
                    specialization="Engineering",
                    years_experience=3
                ),
            ]
        )

        print("Valid mission created:")
        print(f"Mission: {v_mission.mission_name}")
        print(f"ID: {v_mission.mission_id}")
        print(f"Destination: {v_mission.destination}")
        print(f"Duration: {v_mission.duration_days} days")
        print(f"Budget: ${v_mission.budget_millions}M")
        print(f"Crew size: {len(v_mission.crew)}")
        print("Crew memebers:")
        for member in v_mission.crew:
            print(f"- {member.name} ({member.rank.value}) ", end="")
            print(f"- {member.specialization}")

    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print()
    print("=" * 40)

    try:
        i_mission = SpaceMission(
            mission_id="M_INVALID",
            mission_name="Invalid",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="CM01",
                    name="Sarah Connor",
                    rank="cadet",
                    age=42,
                    specialization="Mission Command",
                    years_experience=25
                ),
                CrewMember(
                    member_id="CM02",
                    name="John Smith",
                    rank="lieutenant",
                    age=33,
                    specialization="Navigation",
                    years_experience=8
                ),
                CrewMember(
                    member_id="CM03",
                    name="Alice Johnson",
                    rank="officer",
                    age=28,
                    specialization="Engineering",
                    years_experience=3
                ),
            ]
        )

        print("Valid mission created:")
        print(f"Mission: {i_mission.mission_name}")
        print(f"ID: {i_mission.mission_id}")
        print(f"Destination: {i_mission.destination}")
        print(f"Duration: {i_mission.duration_days} days")
        print(f"Budget: ${i_mission.budget_millions}M")
        print(f"Crew size: {len(i_mission.crew)}")
        print("Crew memebers:")
        for member in i_mission.crew:
            print(f"- {member.name} ({member.rank.value}) ", end="")
            print(f"- {member.specialization}")

    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()

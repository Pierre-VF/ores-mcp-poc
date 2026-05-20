from enum import Enum

from sqlmodel import Field, Session, SQLModel, create_engine, select


class EnumDemandItem(Enum):
    WASHING_MACHINE = "washing machine"
    EV_CHARGING = "EV charging"


_ratings_kw = {
    EnumDemandItem.WASHING_MACHINE: 1.2,
    EnumDemandItem.EV_CHARGING: 8.5,
}

_db_file = "db.sqlite"
_ENGINE = create_engine(f"sqlite:///{_db_file}")


def open_session():
    with Session(_ENGINE) as db:
        yield db


class EnergyFlows(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    grid_import_kw: float
    pv_production_kw: float
    ev_charging_demand_kw: float
    washing_machine_demand_kw: float

    def save_to_database(self, db: Session) -> None:
        self.id = 1
        db.add(self)

    def switch_off(self, d: EnumDemandItem) -> None:
        r: float = _ratings_kw.get(d)
        if d is EnumDemandItem.WASHING_MACHINE:
            self.washing_machine_demand_kw -= r
        elif d is EnumDemandItem.EV_CHARGING:
            self.ev_charging_demand_kw -= r

    def switch_on(self, d: EnumDemandItem) -> None:
        r: float = _ratings_kw.get(d)
        if d is EnumDemandItem.WASHING_MACHINE:
            self.washing_machine_demand_kw += r
        elif d is EnumDemandItem.EV_CHARGING:
            self.ev_charging_demand_kw += r
        return

    @staticmethod
    def load_from_database(db: Session) -> "EnergyFlows":
        x = db.exec(select(EnergyFlows).where(EnergyFlows.id == 1)).first()
        if x is None:
            x = EnergyFlows(
                id=1,
                grid_import_kw=0,
                pv_production_kw=0,
                ev_charging_demand_kw=0,
                washing_machine_demand_kw=0,
            )
        return x


# Creating tables
SQLModel.metadata.create_all(_ENGINE)

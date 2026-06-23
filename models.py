from sqlalchemy.orm import mapped_column,Mapped
from database import Base

class Country(Base):
    __tablename__ = "country"
    name: Mapped[str] = mapped_column(primary_key=True)
    population: Mapped[int] = mapped_column(nullable=False)
    yearly_change: Mapped[float] = mapped_column(nullable=True)
    net_change: Mapped[int] = mapped_column(nullable=True)
    density: Mapped[float] = mapped_column(nullable=True)
    land_area: Mapped[int] = mapped_column(nullable=True) 
    migrants: Mapped[int] = mapped_column(nullable=True)
    median_age: Mapped[float] = mapped_column(nullable=True)
    fertility_rate: Mapped[float] = mapped_column(nullable=True)
    urban_pop: Mapped[float] = mapped_column(nullable=True)
    world_share: Mapped[float] = mapped_column(nullable=True)
    
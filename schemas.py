from pydantic import BaseModel


class Country(BaseModel):
    rank:int
    name: str
    population: int | None
    yearly_change: float | None
    net_change: int | None
    density: int | None
    land_area: int | None
    migrants: int | None
    fertility_rate: float | None
    median_age: float | None
    urban_pop: float | None
    world_share: float | None


class CountryListRespone(BaseModel):
    total_returned: int
    data: list[Country]

class RankResponse(BaseModel):
    metric: str
    limit: int | None
    total_returned: int
    data: list[Country]

class CompareResponse(BaseModel):
    first_country: str
    second_country: str
    data: list[Country]


class RefreshResponse(BaseModel):
     message:str
     total_returned:int


class SingleCountryResponse(BaseModel):
     country:Country
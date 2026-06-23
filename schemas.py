from pydantic import BaseModel
from enum import Enum

class Country(BaseModel):
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

class CountryRank(BaseModel):
    rank: int
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

class Metric(str,Enum):
        population = "population"
        yearly_change = "yearly_change" 
        net_change = "net_change"
        density = "density"
        land_area = "land_area"
        migrants = "migrants"
        fertility_rate = "fertility_rate"
        median_age = "median_age"
        urban_pop = "urban_pop"
        world_share = "world_share"
    

class CountryListRespone(BaseModel):
    total_returned: int
    data: list[Country]

class RankResponse(BaseModel):
    metric: str
    limit: int | None 
    descending_order: bool = False
    total_returned: int
    data: list[CountryRank]

class CompareResponse(BaseModel):
    first_country: str
    second_country: str
    data: list[Country]


class RefreshResponse(BaseModel):
     message:str
     total_returned:int


class SingleCountryResponse(BaseModel):
     country:Country


class PopulationStat(BaseModel):
     country: str
     population: int

class DensityStat(BaseModel):
     country: str
     density: float
class LandAreaStat(BaseModel):
     country: str
     land_area: int

class StatsResponse(BaseModel):

    total_countries: int
    total_world_population: int
    highest_population: PopulationStat
    lowest_population: PopulationStat
    highest_density: DensityStat
    largest_land_area: LandAreaStat
   
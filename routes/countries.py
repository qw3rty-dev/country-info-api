from fastapi import APIRouter,Query,HTTPException,Depends
from scraper import fetch_data
from sqlalchemy.orm import Session
from sqlalchemy import select,func,delete
from models import Country
from database import get_db
from schemas import CountryListRespone,SingleCountryResponse,CompareResponse,RankResponse,RefreshResponse,Country,Metric,StatsResponse
router= APIRouter(prefix="/countries",tags=["Countries"])



@router.get("/", response_model= CountryListRespone)
def get_countries(name:str=Query(default=None,description= "Search any country by name"),
                  db: Session = Depends(get_db)):
    
    query= select(Country)
    if name:
        query= query.where(Country.name.ilike(f"%{name}%"))
    countries = db.scalars(query).all()
    return {
         "total_returned": len(countries),
         "data": countries
    }

@router.get("/rank",response_model=RankResponse)
def rank_countries(metric:Metric=Query(description= "Metric by which results are ranked"),
                   descending_order:bool = Query(False,description="Sort in descending order"),
                   limit:int=Query(default=None, description="Limit the results"),
                   db: Session = Depends(get_db)):
    

   rank_expression = getattr(Country,metric.value)
   order = rank_expression.desc() if descending_order else rank_expression.asc()

   query= select(Country).order_by(order)
   if limit:
       query = query.limit(limit)

   data = db.scalars(query).all()
   response =[]
   for i,c in enumerate(data,1):
       response.append({"rank": i,
                        "name":c.name,
                        "population":c.population,
                        "yearly_change":c.yearly_change,
                        "net_change":c.net_change,
                        "density":c.density,
                        "land_area":c.land_area,
                        "migrants":c.migrants,    
                        "fertility_rate":c.fertility_rate,
                        "median_age":c.median_age,
                        "urban_pop":c.urban_pop,
                        "world_share":c.world_share})    
   return {
        "metric": metric,
        "limit": limit,
        "descending_order":descending_order,
        "total_returned": len(response),
        "data": response
   }



@router.get("/compare",response_model=CompareResponse)
def compare_countries(first_country:str= Query(description="Name of the country for comparison"),
            second_country:str= Query(description="Name of the country for comparison"),
            db: Session = Depends(get_db)):
    
    if first_country.strip().lower() == second_country.strip().lower():
        raise HTTPException(status_code=400,detail="Please provide two different countries")
    

    query= select(Country).where(func.lower(Country.name).in_([first_country.lower(),second_country.lower()]))
    data = db.scalars(query).all()
    if len(data)!=2:
        raise HTTPException(status_code=404,detail="One or both countries were not found")
    countries = {
                c.name.lower(): c.name 
                 for c in data}
    return {
        "first_country": countries[first_country.lower()],
        "second_country": countries[second_country.lower()],
        "data": data
    }



  
@router.post("/refresh",response_model=RefreshResponse)
def refresh_data(db: Session = Depends(get_db)):
   try:
        db.execute(delete(Country))
        db.commit()
        fetch_data(db)
        total = db.scalar(select(func.count(Country.name)))
        return {
            "message":"Success",
            "total returned":total}
   except Exception as e:
       db.rollback()
       raise HTTPException(status_code=500,detail= str(e))
  

@router.get("/stats",response_model=StatsResponse)
def api_stats(db:Session = Depends(get_db)):
    total_countries = db.scalar(select(func.count(Country.name)))
    highest_population = db.scalar(select(func.max(Country.population)))
    highest_population_country = db.scalar(select(Country.name).where(Country.population==highest_population))
    lowest_population = db.scalar(select(func.min(Country.population)))
    lowest_population_country = db.scalar(select(Country.name).where(Country.population==lowest_population))
    total_world_population = db.scalar(select(func.sum(Country.population)))
    highest_density = db.scalar(select(func.max(Country.density)))
    highest_density_country = db.scalar(select(Country.name).where(Country.density==highest_density))
    largest_land_area = db.scalar(select(func.max(Country.land_area)))
    largest_land_area_country = db.scalar(select(Country.name).where(Country.land_area==largest_land_area))

    return {
            "total_countries": total_countries,
            "total_world_population": total_world_population,
            
            "highest_population": {
                "country": highest_population_country,
                "population": highest_population
            },
            "lowest_population": {
                "country": lowest_population_country,
                "population": lowest_population
            },
            "highest_density":{
                "country": highest_density_country,
                "density": highest_density
            },
            "largest_land_area":{
                "country": largest_land_area_country,
                "land_area": largest_land_area
            }
        }

@router.get("/info")
def api_info(db: Session = Depends(get_db)):
    
    total = db.scalar(select(func.count(Country.name)))

    return {
        "source": "Worldometer",
        "total_countries": total,
        "refresh_frequency": "Rarely updated",
        "available_metrics": {
            "population": "Total population",
            "yearly_change": "Annual population growth percentage",
            "net_change": "Population increase/decrease",
            "density": "Population per square kilometer",
            "land_area": "Land area in square kilometers",
            "migrants": "Net migration count",
            "fertility_rate": "Average births per woman",
            "median_age": "Median age of population",
            "urban_pop": "Percentage living in urban areas",
            "world_share": "Country share of world_population"
        }
    }
@router.get("/{name}",response_model=SingleCountryResponse)
def get_country(name:str,db : Session = Depends(get_db)):
    country_info = db.scalar(select(Country).where(func.lower(Country.name) == name.lower()))
    if country_info:
     return {
         "country":country_info
     }
    else:
       raise HTTPException(status_code=404,detail="Country not found")
    

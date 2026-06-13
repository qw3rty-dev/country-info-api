from fastapi import APIRouter,Query,HTTPException
from database import get_connection,init_db
from fastapi.responses import JSONResponse
from scraper import fetch_data
from schemas import CountryListRespone,SingleCountryResponse,CompareResponse,RankResponse,RefreshResponse,Country
router= APIRouter(prefix="/countries",tags=["Countries"])



@router.get("/", response_model= CountryListRespone)
def get_countries(name:str=Query(default=None,description= "Search any country by name")):
    conn= get_connection()
    cursor=conn.cursor()
    query= "SELECT * FROM country"
    params=[]
    if name:
        query+= " WHERE name LIKE ?"
        params.append(f"%{name}%")

    cursor.execute(query,params)
    rows=cursor.fetchall()
    conn.close()
    data=[dict(row) for row in rows]
    return {
         "total_returned": len(data),
         "data": data
    }

@router.get("/rank",response_model=RankResponse)
def rank_countries(metric:str=Query(description= "Metric by which results are ranked"),
               limit:int=Query(default=None, description="Limit the results")):
   allowed_metrics = {
        "population",
        "yearly_change", 
        "net_change",
        "density",
        "land_area",
        "migrants",
        "fertility_rate",
        "median_age",
        "urban_pop",
        "world_share"
    }
   if metric not in allowed_metrics:
      raise HTTPException(status_code=400,detail=f"Invalid metric.Choose from:({','.join(sorted(allowed_metrics))})")
   
   conn= get_connection()
   cursor= conn.cursor()
   query= f"SELECT * FROM country WHERE {metric} IS NOT NULL ORDER BY {metric} DESC"
   if limit:
      query+= " limit ?"
      cursor.execute(query,(limit,))
   else:
      cursor.execute(query)

   rows= cursor.fetchall()
   conn.close()
   data= [dict(row) for row in rows]

   
   for i, country in enumerate(data, 1):
        country["rank"] = i
    
   return {
        "metric": metric,
        "limit": limit,
        "total_returned": len(data),
        "data": data
   }



@router.get("/compare",response_model=CompareResponse)
def compare_countries(first_name:str= Query(description="Name of the country for comparison"),
            second_name:str= Query(description="Name of the country for comparison")):
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM country WHERE LOWER(name) IN (LOWER(?),LOWER(?))",(first_name,second_name))
    rows= cursor.fetchall()
    conn.close()
    data= [dict(row) for row in rows]
    return {
        "first_country": first_name,
        "second_country": second_name,
        "data": data
    }



  
@router.post("/refresh",response_model=RefreshResponse)
def refresh_data():
   conn= get_connection()
   cursor= conn.cursor()
   try:
        cursor.execute("DELETE FROM country")
        conn.commit()
        fetch_data()
        cursor.execute("SELECT COUNT(*) FROM country")
        total= cursor.fetchone()[0]
        

        return {
            "message":"Success",
            "total_returned":total}
   except Exception as e:
       conn.rollback()
       raise HTTPException(status_code=500,detail= str(e))
   finally:
       conn.close()


@router.get("/info")
def api_info():
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM country")
    total= cursor.fetchone()[0]
    conn.close()

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
def get_country(name:str):
    conn= get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM country WHERE LOWER(name) = LOWER(?)",(name,))
    row =cursor.fetchone()
    conn.close()
    if row:
     return {
         "country":dict(row)
     }
    else:
       raise HTTPException(status_code=404,detail="Country not found")
    

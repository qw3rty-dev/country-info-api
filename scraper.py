import requests
from bs4 import BeautifulSoup
from database import get_connection
def parse_int(value:str):
   value= value.replace(",","").replace("−", "-").strip()
   return int(value) if value not in ("","N.A","−") else None


def parse_float(value:str):
   value= value.replace(",","").replace("%","").replace("−", "-").strip()
   if value in ("","N.A.","−","-"):
      return None
   try:
        return float(value) 
   except ValueError:
      return None


def scrape_country():
    url="https://www.worldometers.info/world-population/population-by-country/"
    headers = {"User-Agent": "Mozilla/5.0"}
    session=requests.Session()
    req=session.get(url,headers=headers)
    req.raise_for_status()
    
    if req.status_code!=200:
        print("Request failed")
    else:

        req.encoding="utf-8"
        soup=BeautifulSoup(req.text,"lxml")
        data=[]
        countries=soup.select("tr")
        for row in countries[1:]:
           cols= [col.text.strip() for col in row.select(".border-e")]

           country_data={
              "name":cols[1],
              "population":parse_int(cols[2]),
              "yearly_change":parse_float(cols[3]),
              "net_change":parse_int(cols[4]),
              "density":parse_int(cols[5]),
              "land_area":parse_int(cols[6]),
              "migrants":parse_int(cols[7]),    
              "fertility_rate":parse_float(cols[8]),
              "median_age":parse_float(cols[9]),
              "urban_pop":parse_float(cols[10]),
              "world_share":parse_float(cols[11])
              
           }
           data.append(country_data)
        return data



def fetch_data():
   info=scrape_country()
   conn=get_connection()
   cursor=conn.cursor()
   for row in info:
      cursor.execute("INSERT INTO  country (name,population,yearly_change,net_change,density,land_area,migrants,fertility_rate,median_age,urban_pop,world_share) values(?,?,?,?,?,?,?,?,?,?,?)",
                     (row['name'],row['population'],row['yearly_change'],row['net_change'],row['density'],
                     row['land_area'],row['migrants'],row['fertility_rate'],row['median_age'],row['urban_pop'],
                     row['world_share']))
   conn.commit()
   conn.close()


if __name__=="__main__":
 fetch_data()
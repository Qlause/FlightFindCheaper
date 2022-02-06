import requests

class FlighData:
    def __init__(self, key:str, fr:str) -> None:
        self.head = {"apikey":key}
        self.fr = fr
        self.body = {
                "fly_from":self.fr,
                "curr":"IDR",
                "fly_to":None,
                "date_from":None,
                "date_to":None,
                "flight_type":None,
                "price_to":None,
                "nights_in_dst_from":None,
                "nights_in_dst_to":None
            }
        self.url = "https://tequila-api.kiwi.com/v2"
    
    def get_data(self, **kw):
        result = []
        
        self.body["fly_to"] = kw.get("fly_to")
        self.body["date_from"] = kw.get("date_from")
        self.body["date_to"] = kw.get("date_to")
        self.body["price_to"] = kw.get("price_max", 10000000000)
        self.body["flight_type"] = kw.get("flight_type", "oneway")
        self.body["nights_in_dst_from"] = kw.get("nights_min", None)
        self.body["nights_in_dst_to"] = kw.get("nights_max", None)
        
        res = requests.get(url=f"{self.url}/search", params=self.body, headers=self.head).json()

        try :
            if len(res["data"]) > 0:
                for data in res["data"]:
                    result.append({})
                    result[-1]["token"] = data["booking_token"]
                    result[-1]["city_to"] = data["cityTo"] 
                    result[-1]["country_to"] = data["countryTo"]["name"]
                    result[-1]["price"] = data["price"]
                    result[-1]["transit"] = True if len(data["route"]) > 0 else False
                    result[-1]["airlines"] = data["airlines"]
                    result[-1]["dates"] = [data["local_departure"], data["local_arrival"]]
                    result[-1]["dates_in_utc"] = f'{data["utc_departure"]} ~ {data["utc_arrival"]}'
            
            return result
        
        except:
            
            return result      
              





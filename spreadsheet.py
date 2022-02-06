import requests

class Sheet():
    def __init__(self, key:str, url:str) -> None:
        self.header = {"Authorization":key,
                       "Content-Type":"application/json"}
        self.url = url
        self.query = {"get":requests.get, 
                      "post":requests.post, 
                      "put": requests.put, 
                      "delete":requests.delete}
        
    def retrieve(self, filter_m="", ID=""):    
        data = self.query["get"](url=f"{self.url}/{str(ID)}", params=filter_m, headers=self.header)
        return data
        
    def del_row(self, ID):    
        data = self.query["delete"](url=f"{self.url}/{str(ID)}", headers=self.header)
        return data
                
    def add_row(self, doc_name:str, **kw):
        message = {
            doc_name :
                {}
        }
        
        for k, v in kw.items():
            message[doc_name][k] = v
        
        data = self.query["post"](url=self.url, json=message, headers=self.header)
        return data
            
    def edit_row(self, doc_name, ID, **kw):    
        message = {
            doc_name :
                {}
        }
        
        for k, v in kw.items():
            message[doc_name][str(k)] = str(v)

        data = self.query["put"](url=f"{self.url}/{str(ID)}", json=message, headers=self.header)
        return data

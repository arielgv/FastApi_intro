
from typing import Optional
#optional to indicate a field of the basemodel could be optional
from pydantic import BaseModel
from pydantic import Field
#this is for determinate the Model of FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path


app = FastAPI()

#Model Create
class Person(BaseModel):
    first_name : str
    last_name : str
    age : int
    hair_color: Optional[str] = None
    is_married : Optional[bool] = None

    class Config:
        schema_extra = {
            "example" : {
                "first_name" : "Ariel",
                "last_name" : "Villafane",
                "age" : 37,
                "hair_color" : "brown",
                "is_married" : False
            }
        }

class Location(BaseModel):
    adress : str
    city : str 
    country : str
    class Config:
        schema_extra = {
            "example" : {
                "adress" : "marcos paz",
                "city" : "Tucuman",
                "country" : "Argentina"
            }
        }


@app.get("/")
def home():
    return {"Hello":" World",   "hola ": ("probando"),
    "que onda": 1+2,
    "nuevo diccionario": {
        "clave 2 de 3" : "resultado",
        "nice one ": {
            "tercer": "valorrrr",
            
        }
    }
    }
@app.post("/person/new")
def create_person(person : Person = Body(...)):
    return person

# validaciones: query parameters
@app.get("/person/detail/")
def detail_person(
    name : Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        #title = "Id person",
        #description="This is the person name, its between 1 and 50 characters"
        ),
    age : int = Query(...),
    hair_color: Optional[str] = Query()
):    
    return {name : age}

@app.get("/person/detail/{person_id}")
def detail_person(
    person_id : int = Path(
        ... , 
        ge=1, 
        title="Person Id",        
        description="Person id should be greather than 1. It's required."
        )
):
    return {person_id : "it exist"}

@app.put("/person/{person_id}")
def request_details(
    person_id : int = Path(
        ...,
        title=  "Id person",
        description= "This is the person id",
        ge = 1
    ),
        person : Person = Body(...),
        location : Location = Body(...)

    
):
    results = person.dict()
    results.update(location.dict())
    # with this technique you can combine two or more Json in one output
    return results 
    #return person 




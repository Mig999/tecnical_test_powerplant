from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from algorithm import Problem,Fuels,Powerplant

app = FastAPI()

# Definir un modelo de datos con Pydantic
class Fuelsread(BaseModel):
    gas: float = Field(alias="gas(euro/MWh)")
    kerosine: float = Field(alias="kerosine(euro/MWh)")
    co2: float = Field(alias="co2(euro/ton)")
    wind: float = Field(alias="wind(%)")

class Powerplantread(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: float
    pmax: float

class Productionplan(BaseModel):
    load: float
    fuels: Fuelsread
    powerplants: list[Powerplantread]

class Response(BaseModel):
    name: str
    p: float

@app.post("/productionplan")
async def recibe_json(productionplan: Productionplan):
    fuels = Fuels(productionplan.fuels.gas,productionplan.fuels.kerosine,productionplan.fuels.co2,productionplan.fuels.wind)
    powerplants = []
    for powerplant in productionplan.powerplants:
        powerplants.append(Powerplant(powerplant.name,powerplant.type,powerplant.efficiency,powerplant.pmin,powerplant.pmax))
    new_problem = Problem(productionplan.load,fuels,powerplants)

    load_per_plant = new_problem.calculate_plants_to_turn_on()
    response = []
    for plant in load_per_plant:
        response.append(Response(name=plant[0], p=plant[1]))

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)
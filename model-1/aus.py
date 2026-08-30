from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AusHouseData(BaseModel):
  Bedrooms: int
  Bathrooms: int
  SqFt: int
  City: str
  State: str
  Year_Built: int
  Type: str
  Garage: int


INTERCEPT = -5725341.067030115

COEF = {
    "Bedrooms": 59975.5725302,
    "Bathrooms": 48999.1117196,
    "SqFt": 450.72535783,
    "Year_Built": 3075.85762934,
    "Garage": 40599.3116231,
    "Adelaide": -85591.93482992,
    "Brisbane": -34592.77056938,
    "Melbourne": 64822.76094307,
    "Perth": -59966.18049311,
    "Sydney": 115328.12494934,
    "NSW": 115328.12494934,
    "QLD": -34592.77056938,
    "SA": -85591.93482992,
    "VIC": 64822.76094307,
    "WA": -59966.18049311,
    "Apartment": -45969.2611603,
    "House": 53260.95149003,
    "Townhouse": -7291.69032973,
}


@app.get("/")
def serve_aus_ui():
  return FileResponse("aus.html")


@app.post("/predict-aus")
def predict_aus(data: AusHouseData):
  price = (
      INTERCEPT
      + COEF["Bedrooms"] * data.Bedrooms
      + COEF["Bathrooms"] * data.Bathrooms
      + COEF["SqFt"] * data.SqFt
      + COEF["Year_Built"] * data.Year_Built
      + COEF["Garage"] * data.Garage
  )

  if data.City in COEF:
    price += COEF[data.City]

  if data.State in COEF:
    price += COEF[data.State]

  if data.Type in COEF:
    price += COEF[data.Type]

  return {"price": price}
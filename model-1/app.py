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


# --- NEPAL MODEL DATA ---
class NepalHouseData(BaseModel):
  size: float
  floors: float
  age: float
  location: str


NEPAL_INTERCEPT = 6145322.929727629
NEPAL_COEF = {
    "size_aana": 3501973.01304593,
    "floors": 2227057.24322236,
    "house_age_years": -288452.00283914,
    "Baluwatar": 33174286.94273959,
    "Baneshwor": 1206700.60164427,
    "Bhaktapur": -28689716.68247237,
    "Boudha": -7991566.61665977,
    "Budhanilkantha": -20633733.8935129,
    "Chabahil": -4432801.54614976,
    "Gongabu": -16382068.72103312,
    "Jhamsikhel": 14803988.4678202,
    "Kalanki": -14539552.42503028,
    "Kalimati": -8490092.98831284,
    "Kirtipur": -24102738.45512374,
    "Koteshwor": -10345011.97866113,
    "Lazimpat": 30700234.43617596,
    "Naxal": 36068553.85116125,
    "New Baneshwor": -1328372.41180944,
    "Sanepa": 20981891.41922424,
}


# --- AUSTRALIA MODEL DATA ---
class AusHouseData(BaseModel):
  Bedrooms: int
  Bathrooms: int
  SqFt: int
  City: str
  State: str
  Year_Built: int
  Type: str
  Garage: int


AUS_INTERCEPT = -5725341.067030115
AUS_COEF = {
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


# --- ROUTES FOR HTML PAGES ---
@app.get("/")
def serve_nepal_ui():
  return FileResponse("index.html")


@app.get("/aus.html")
def serve_aus_ui():
  return FileResponse("aus.html")


# --- PREDICTION ENDPOINTS ---
@app.post("/predict-nepal")
def predict_nepal(data: NepalHouseData):
  price = (
      NEPAL_COEF["size_aana"] * data.size
      + NEPAL_COEF["floors"] * data.floors
      + NEPAL_COEF["house_age_years"] * data.age
      + NEPAL_INTERCEPT
  )
  if data.location in NEPAL_COEF:
    price += NEPAL_COEF[data.location]
  return {"price": price}


@app.post("/predict-aus")
def predict_aus(data: AusHouseData):
  price = (
      AUS_INTERCEPT
      + AUS_COEF["Bedrooms"] * data.Bedrooms
      + AUS_COEF["Bathrooms"] * data.Bathrooms
      + AUS_COEF["SqFt"] * data.SqFt
      + AUS_COEF["Year_Built"] * data.Year_Built
      + AUS_COEF["Garage"] * data.Garage
  )
  if data.City in AUS_COEF:
    price += AUS_COEF[data.City]
  if data.State in AUS_COEF:
    price += AUS_COEF[data.State]
  if data.Type in AUS_COEF:
    price += AUS_COEF[data.Type]
  return {"price": price}
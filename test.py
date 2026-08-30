import numpy as np
import pandas as pd

np.random.seed(42)
n_samples = 5000

sqft = np.random.normal(2000, 600, n_samples).clip(800, 5000)
bedrooms = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.05, 0.15, 0.5, 0.2, 0.1])
bathrooms = np.random.choice([1, 2, 3, 4], size=n_samples, p=[0.2, 0.5, 0.2, 0.1])
year_built = np.random.randint(1980, 2024, n_samples)
garage = np.random.choice([0, 1, 2], size=n_samples, p=[0.2, 0.5, 0.3])
lot_area = (sqft * np.random.uniform(1.5, 3.0, n_samples)).astype(int)

cities = np.random.choice(['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'], size=n_samples, p=[0.3, 0.3, 0.2, 0.1, 0.1])
city_bonus = {'Sydney': 450000, 'Melbourne': 350000, 'Brisbane': 150000, 'Perth': 100000, 'Adelaide': 50000}
states_map = {'Sydney': 'NSW', 'Melbourne': 'VIC', 'Brisbane': 'QLD', 'Perth': 'WA', 'Adelaide': 'SA'}
state = [states_map[c] for c in cities]

property_type = np.random.choice(['House', 'Apartment', 'Townhouse'], size=n_samples, p=[0.6, 0.25, 0.15])
type_bonus = {'House': 100000, 'Townhouse': 40000, 'Apartment': 0}

price = (
    100000
    + sqft * 450
    + bedrooms * 60000
    + bathrooms * 50000
    + garage * 40000
    + (year_built - 1980) * 3000
    + np.array([city_bonus[c] for c in cities])
    + np.array([type_bonus[t] for t in property_type])
    + np.random.normal(0, 30000, n_samples)
)

new_df = pd.DataFrame({
    'Price': price.astype(int),
    'Bedrooms': bedrooms,
    'Bathrooms': bathrooms,
    'SqFt': sqft.astype(int),
    'City': cities,
    'State': state,
    'Year_Built': year_built,
    'Type': property_type,
    'Garage': garage,
    'Lot_Area': lot_area
})

new_df.to_csv('aus_real_estate.csv', index=False)
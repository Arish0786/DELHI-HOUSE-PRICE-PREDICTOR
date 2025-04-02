import pickle
import json
import numpy as np
import pandas as pd

# Global variables for storing model and data
__locations = None
__data_columns = None
__model = None
X = None
locality_price_map = None


def load_saved_artifacts():
    """
    Load model, column data, and locality price map from artifacts.
    """
    print("Loading saved artifacts...start")
    global __data_columns, __locations, __model, X, locality_price_map

    try:
        with open("./artifacts/columns.json", "r") as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[5:]

        with open('./artifacts/final_random_forest_model.pkl', 'rb') as f:
            __model = pickle.load(f)

        X = pd.read_csv("./artifacts/MagicBricks.csv")
        print("Dataset loaded successfully!")

        if "Price_per_Sqft" not in X.columns:
            if "Price" in X.columns and "Area" in X.columns:
                X["Price_per_Sqft"] = X["Price"] / X["Area"]
                print("Price_per_Sqft column successfully created!")
            else:
                print("Error: 'Price' column is missing, cannot calculate 'Price_per_Sqft'.")

        with open("./artifacts/locality_price_map.json", "r") as f:
            locality_price_map = json.load(f)

        print("Loading saved artifacts...done")
    except Exception as e:
        print(f"Error loading artifacts: {e}")


def get_estimated_price(locality, area, bhk, bath):
    if __model is None:
        return "Model not loaded. Call load_saved_artifacts() first."

    try:
        locality_avg_price = locality_price_map.get(locality, np.mean(list(locality_price_map.values())))
        per_sqft_mean = X["Per_Sqft"].mean()
        price_per_sqft_mean = X["Price_per_Sqft"].mean()

        x = np.array([area, bhk, bath, per_sqft_mean, price_per_sqft_mean, locality_avg_price]).reshape(1, -1)
        return round(__model.predict(x)[0], 2)
    except Exception as e:
        return f"Prediction Error: {str(e)}"


def get_location_names():
    return __locations if __locations else []


def get_data_columns():
    return __data_columns if __data_columns else []


# Test the functions
if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price("Rohini Sector 25", 800, 3, 2))
    print(get_estimated_price("J R Designers Floors, Rohini Sector 24", 750, 2, 2))
    print(get_estimated_price("Citizen Apartment, Rohini Sector 13", 900, 2, 2))
print(get_estimated_price('Alaknanda', 800, 3, 2))
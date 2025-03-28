import pickle
import json
import numpy as np

# Global variables for storing model and data
__locations = None
__data_columns = None
__model = None

def load_saved_artifacts():
    """
    Load model and column data from artifacts.
    """
    print("Loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    try:
        with open("./artifacts/columns.json", "r") as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[5:]  # First 3 columns are sqft, bhk, bath

        with open('./artifacts/final_random_forest_model.pkl', 'rb') as f:
            __model = pickle.load(f)

        print("Loading saved artifacts...done")
    except Exception as e:
        print(f"Error loading artifacts: {e}")

def get_estimated_price(location, total_sqft, size_bhk, bathroom):
    """
    Predict the price of a property using the loaded model.

    Parameters:
    location (str): Property location
    total_sqft (float): Total area in square feet
    size_bhk (int): Number of bedrooms
    bathroom (int): Number of bathrooms

    Returns:
    float: Estimated property price or error message
    """
    if __model is None or __data_columns is None:
        return "Model or data columns not loaded. Call load_saved_artifacts() first."

    try:
        # Check if location is valid
        loc_index = __data_columns.index(location.lower()) if location.lower() in __data_columns else -1

        # Create input array
        x = np.zeros(len(__data_columns))
        x[0] = total_sqft
        x[1] = size_bhk
        x[2] = bathroom
        if loc_index >= 0:
            x[loc_index] = 1

        # Predict using the model
        predicted_price = __model.predict([x])[0]
        return round(predicted_price, 2)
    except Exception as e:
        return f"Prediction Error: {str(e)}"

def get_location_names():
    """
    Returns the list of location names.
    """
    if __locations is None:
        return "Locations not loaded. Call load_saved_artifacts() first."
    return __locations

def get_data_columns():
    """
    Returns the data column names.
    """
    if __data_columns is None:
        return "Data columns not loaded. Call load_saved_artifacts() first."
    return __data_columns

# Test the functions
if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('Rohini Sector 25', 800, 3, 2))
    print(get_estimated_price('Kalkaji', 800, 3, 2))
    print(get_estimated_price('Alaknanda', 800, 3, 2))
import os
import requests
import numpy as np
import argparse
from lightgbm import Booster
from .features import PEFeatureExtractor

# Download the LightGBM model
LIGHTGBM_MODEL_URL = "http://sorel-20m.s3.amazonaws.com/09-DEC-2020/baselines/checkpoints/lightGBM/seed0/lightgbm.model"
MODEL_PATH = "lightgbm.model"

if not os.path.exists(MODEL_PATH):
    response = requests.get(LIGHTGBM_MODEL_URL)
    with open(MODEL_PATH, "wb") as model_file:
        model_file.write(response.content)

# Load the LightGBM model
model = Booster(model_file=MODEL_PATH)

def predict_sample(lgbm_model, file_data, feature_version=2):
    """
    Predict a PE file with an LightGBM model
    """
    extractor = PEFeatureExtractor(feature_version)
    features = np.array(extractor.feature_vector(file_data), dtype=np.float32)
    return lgbm_model.predict([features])[0]

def main():
    parser = argparse.ArgumentParser(description="Predict a PE file with an LightGBM model")
    parser.add_argument("file_path", help="Path to the PE file to predict")
    args = parser.parse_args()

    with open(args.file_path, "rb") as file:
        file_data = file.read()  # Read the file data

    # Make prediction using the LightGBM model and the predict_sample function
    prediction = predict_sample(model, file_data)

    print({"prediction": prediction.tolist()})

if __name__ == "__main__":
    main()

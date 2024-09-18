# -*- coding: utf-8 -*-
"""mortgage_qualification_predictor.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jIBtlDsND6CTsGSpAXBSVfkMHsYYw7ry
"""

import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import joblib

# Load the fitted preprocessor
preprocessor = joblib.load('/home/azureuser/preprocessor.pkl')

# Define the Streamlit app
def main():
    st.title("Mortgage Qualification Predictor")
    st.write("Enter applicant details to predict if they will qualify for a mortgage.")

    # Create input fields for applicant details
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Marital Status", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    property_type = st.selectbox("Property Type", ["Urban", "Rural", "Semi-Urban"])
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    applicant_income = st.number_input("Applicant Income")
    coapplicant_income = st.number_input("Coapplicant Income")
    loan_amount = st.number_input("Loan Amount")
    loan_term = st.number_input("Loan Term (in months)")
    credit_history = st.selectbox("Credit History", ["Good", "Bad"])

    encoding_dict = {
        "Gender": {"Male": 0, "Female": 1},
        "Married": {"No": 0, "Yes": 1},
        "Dependents": {"0": 0, "1": 1, "2": 2, "3+": 3},
        "Education": {"Graduate": 0, "Not Graduate": 1},
        "Self_Employed": {"Yes": 1, "No": 0},
        "Credit_History": {"Good": 1.0, "Bad": 0.0},
        "Property_Area": {"Urban": 0, "Rural": 1, "Semi-Urban": 2}
    }

    # Collect input data into a DataFrame
    input_data = pd.DataFrame({
        "Gender": [encoding_dict["Gender"][gender]],
        "Married": [encoding_dict["Married"][married]],
        "Dependents": [encoding_dict["Dependents"][dependents]],
        "Education": [encoding_dict["Education"][education]],
        "Self_Employed": [encoding_dict["Self_Employed"][self_employed]],
        "ApplicantIncome": [applicant_income],
        "CoapplicantIncome": [coapplicant_income],
        "LoanAmount": [loan_amount],
        "Loan_Amount_Term": [loan_term],
        "Credit_History": [encoding_dict["Credit_History"][credit_history]],
        "Property_Area": [encoding_dict["Property_Area"][property_type]]
    })

    # Ensure input data has correct column names
    selected_features = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
    input_data = input_data[selected_features]

    # Preprocess the input data
    processed_input = preprocessor.transform(input_data)

    # Load the pre-trained machine learning model
    model = load_model('mortgage_qualification_predictor.h5')

    # Make predictions when the Predict button is clicked
    if st.button("Predict"):
        # Make predictions using the preprocessed input data
        prediction = model.predict(processed_input)

        # Display prediction result
        if prediction[0] >= 0.5:
            st.write("Congratulations! You will qualify for a mortgage.")
        else:
            st.write("Sorry, you will not qualify for a mortgage.")

# Run the Streamlit app
if __name__ == "__main__":
    main()

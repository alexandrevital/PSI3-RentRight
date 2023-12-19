import streamlit as st
import xgboost
import numpy as np
import pickle
from utils import load_data, check_data, title
import pandas as pd

df = pd.read_csv('model\model_input_data.csv')
print(df)

def price_prediction(analysis_df):
    title("Previsão de Preço de Aluguel")
    x = analysis_df.drop('price', axis = 1)
    y = analysis_df['price']
        
    with open('model\model_xgb_mae_123.pkl', 'rb') as file:
        model = pickle.load(file)
    
    st.write("Realizar uma previsão de preço:")
    input_values = []
    for feature in x:
        value = st.number_input(f"Insira o valor de {feature}", value=np.mean(df[feature]))
        input_values.append(value)

    if st.button("Prever"):
        prediction = model.predict([input_values])
        st.write(f"Previsão de Preço: ${prediction[0]:.2f}")

price_prediction(df)
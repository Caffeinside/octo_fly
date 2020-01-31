import pandas as pd
import streamlit as st

st.title('OCTO Fly')
st.markdown('Welcome to the new OCTO Fly app!')

predictions = pd.read_csv('./data/processed/predictions.csv')
predictions_placeholder = st.dataframe(predictions)

button = st.button("Retrieve last predictions")
if button:
    st.balloons()
    predictions = pd.read_csv('./data/processed/predictions.csv')
    predictions_placeholder.dataframe(predictions)

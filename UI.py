import streamlit as st

st.write("First trial")
usename = st.text_input("What is your name?")
st.write(f"\t your name is {usename}")
import streamlit as st
import requests

def ar(text):
    try:
        from arabic_reshaper import reshape
        from bidi.algorithm import get_display
        return get_display(reshape(text))
    except: return text

st.title(ar("ميناء TDZ ALGERIA"))
st.success(ar("المنصة نشطة: عمولة 5% و100 تاجر"))

if st.button(ar("دخول BOSS")):
    st.write(ar("مرحباً بك في لوحة التحكم"))

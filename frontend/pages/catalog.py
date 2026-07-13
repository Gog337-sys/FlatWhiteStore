import requests
import streamlit as st

from frontend.api.client import get_error_message, get_product
from frontend.auth.state import is_admin
from frontend.components.product_card import render_product_card
from frontend.pages.profile import response

st.header("Каталог")

if is_admin():
    if st.button("Создать запись"):
        st.switch_page("pages/create_product.py")

try:
    response = get_product()
except requests.RequestException:
    st.error("Backend недоступен. Проверьте запуск FastAPI.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

products = response.json()

if not products:
    st.info("В каталоге пока нет записей.")
    st.stop()

columns = st.columns(3)

for index, product in enumerate(products):
    with columns[index % 3]:
        render_product_card(product)
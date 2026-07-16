import requests
import streamlit as st

from frontend.api.client import get_error_message, get_product
from frontend.components.product_card import render_product_card

product_id = st.session_state.get("selected_product_id")

if product_id is None:
    st.info("Сначала выберите запись в каталоге.")
    st.page_link("pages/catalog.py", label="Перейти в каталог")
    st.stop()

try:
    response = get_product(product_id)
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

try:
    product = response.json()
except ValueError:
    st.error("Некорректный ответ сервера (не JSON).")
    st.stop()

if not isinstance(product, dict):
    st.error("Некорректный формат данных от сервера.")
    st.stop()

if "title" in product and "name" not in product:
    product["name"] = product["title"]

st.header(product.get("name") or product.get("title", "Без названия"))

render_product_card(product, key_prefix="details")
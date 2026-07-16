import requests
import streamlit as st

from frontend.api.client import get_error_message, get_products, add_favorite
from frontend.auth.state import is_admin, require_login
from frontend.components.product_card import render_product_card

require_login()

st.header("Каталог")


if is_admin():
    if st.button("Создать запись"):
        st.switch_page("pages/create_product.py")


try:
    response = get_products()
except requests.RequestException:
    st.error("Backend недоступен. Проверьте запуск FastAPI.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()


try:
    products = response.json()
except ValueError:
    st.error("Некорректный ответ сервера (не JSON).")
    st.stop()


if not isinstance(products, list):
    st.error("Некорректный формат данных от сервера.")
    st.stop()


if not products:
    st.info("В каталоге пока нет записей.")
    st.stop()



columns = st.columns(3)
for index, product in enumerate(products):
    with columns[index % 3]:
        render_product_card(product)

filter_category = st.session_state.get("filter_category", None)

if filter_category:
    st.info(f"Показаны товары категории «{filter_category}»")
    if st.button("Сбросить фильтр"):
        st.session_state.pop("filter_category", None)
        st.rerun()

try:
    response = get_products(category_name=filter_category)  # передаём параметр
except requests.RequestException:
    st.error("Backend недоступен.")
    st.stop()
import requests
import streamlit as st

from frontend.api.client import get_error_message, get_product
from frontend.components.product_card import render_admin_actions, render_favorite_button
from frontend.pages.profile import response

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

product = response.json()

st.header(product["title"])

if product.get("image_url"):
    st.image(product["image_url"], width=500)

st.write(product.get("description", ""))
render_favorite_button(product, key_prefix="details")
render_admin_actions(product["id"], key_prefix="details")
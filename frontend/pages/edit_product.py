import requests
import streamlit as st

from frontend.api.client import get_error_message, get_product, update_product
from frontend.auth.state import require_admin, require_login

require_login()
require_admin()
st.header("Редактирование записи")

product_id = st.session_state.get("edit_product_id")

if product_id is None:
    st.info("Сначала выберите запись для редактирования.")
    st.stop()

try:
    product_response = get_product(product_id)
except requests.RequestException:
    st.error("Не удалось получить запись с backend.")
    st.stop()

if not product_response.ok:
    st.error(get_error_message(product_response))
    st.stop()

try:
    product = product_response.json()
except ValueError:
    st.error("Некорректный ответ сервера (не JSON).")
    st.stop()

if not isinstance(product, dict):
    st.error("Некорректный формат данных от сервера.")
    st.stop()

name = product.get("name", "")
size = product.get("size", 0)
price = product.get("price", 0)
category_name = product.get("category_name") or ""
image_url = product.get("image_url") or ""

with st.form(f"edit_item_form_{product_id}"):
    name_input = st.text_input("Название", value=name)
    size_input = st.number_input("Размер (число)", value=size, step=1)
    price_input = st.number_input("Цена (руб)", value=price, step=100)
    category_input = st.text_input("Название категории", value=category_name)
    image_input = st.text_input("Ссылка на изображение", value=image_url)

    submitted = st.form_submit_button("Сохранить")

if submitted:
    errors = []
    if not name_input.strip():
        errors.append("Укажите название.")
    if size_input <= 0:
        errors.append("Размер должен быть положительным числом.")
    if price_input <= 0:
        errors.append("Цена должна быть положительным числом.")
    if category_input and not category_input.strip():
        errors.append("Название категории не может состоять только из пробелов.")

    if errors:
        for error in errors:
            st.error(error)
        st.stop()

    payload = {
        "name": name_input.strip(),
        "size": int(size_input),
        "price": int(price_input),
        "category_name": category_input.strip() or None,
        "image_url": image_input.strip() or None,
    }

    try:
        response = update_product(product_id, payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.ok:
        st.session_state["selected_product_id"] = product_id
        st.success("Изменения сохранены.")
        st.switch_page("pages/details.py")
    else:
        st.error(get_error_message(response))
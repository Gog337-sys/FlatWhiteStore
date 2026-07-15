import requests
import streamlit as st

from frontend.api.client import create_product, get_error_message
from frontend.auth.state import require_admin

require_admin()

st.header("Новая запись")

with st.form("create_item_form"):
    name = st.text_input("Название", key="name")
    price = st.text_input("Цена", key="price")
    size = st.text_input("Размер", key="size")
    category_name = st.text_input("Название категории", key="category_name")
    image_url = st.text_input("Ссылка на изображение", key="image_url")
    submitted = st.form_submit_button("Создать")

if submitted:

    errors = []
    if not name.strip():
        errors.append("Укажите название.")
    if not category_name.strip():
        errors.append("Укажите название категории.")


    try:
        price_int = int(price)
        size_int = int(size)
    except ValueError:
        errors.append("Цена и размер должны быть целыми числами.")
    else:
        if price_int <= 0:
            errors.append("Цена должна быть положительным числом.")
        if size_int <= 0:
            errors.append("Размер должен быть положительным числом.")


    if errors:
        for error in errors:
            st.error(error)
        st.stop()


    payload = {
        "name": name.strip(),
        "price": price_int,
        "size": size_int,
        "category_name": category_name.strip(),
        "image_url": image_url.strip() or None,
    }


    try:
        response = create_product(payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.status_code in (200, 201):

        try:
            created_product = response.json()
        except ValueError:
            st.error("Некорректный ответ сервера (не JSON).")
            st.stop()

        if not isinstance(created_product, dict) or "id" not in created_product:
            st.error("Ответ сервера не содержит ожидаемых данных о продукте.")
            st.stop()

        st.session_state["selected_product_id"] = created_product["id"]
        st.success("Товар успешно создан!")
        st.switch_page("pages/details.py")
    else:
        st.error(get_error_message(response))
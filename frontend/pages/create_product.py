import streamlit as st
import requests

from frontend.api.client import (
    create_product,
    update_product,
    upload_image,
    get_error_message,
    BACKEND_URL,
)
from frontend.auth.state import require_admin

require_admin()
st.header("Новая запись")

with st.form("create_item_form"):
    name = st.text_input("Название")
    price = st.number_input("Цена", min_value=1500, max_value=9999, step=100)
    size = st.number_input("Размер", min_value=32, max_value=60, step=1)
    category_name = st.text_input("Категория")
    description = st.text_area("Описание")
    image_url = st.text_input("Ссылка на изображение (URL)")
    uploaded_file = st.file_uploader("Или загрузите файл", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Создать")

if submitted:
    if not name.strip():
        st.error("Введите название")
        st.stop()

    payload = {
        "name": name.strip(),
        "price": price,
        "size": size,
        "category_name": category_name.strip() or None,
        "description": description.strip() or "",
        "image_url": image_url.strip() or None,
    }

    try:
        resp = create_product(payload)
    except requests.RequestException:
        st.error("Сервер недоступен")
        st.stop()

    if resp.status_code not in (200, 201):
        st.error(get_error_message(resp))
        st.stop()

    product = resp.json()
    product_id = product["id"]

    # Если был выбран файл, загружаем его и обновляем товар
    if uploaded_file is not None:
        with st.spinner("Загружаю изображение..."):
            try:
                image_data = upload_image(uploaded_file)  # (1)
                photo_path = image_data.get("photo_path")  # (2)
                if photo_path:
                    from frontend.api.client import BACKEND_URL

                    full_image_url = f"{BACKEND_URL}{photo_path}"
                    update_resp = update_product(product_id, {"image_url": full_image_url})
                    if update_resp.ok:
                        st.success("Товар создан и изображение загружено!")
                    else:
                        st.warning("Товар создан, но не удалось прикрепить изображение")
                else:
                    st.warning("Сервер вернул ответ без photo_path")
            except requests.RequestException:
                st.warning("Ошибка при загрузке изображения")
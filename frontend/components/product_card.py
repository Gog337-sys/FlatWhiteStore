import  requests
import streamlit as st

from frontend.api.client import (
    add_favorite,
    delete_product,
    get_error_message,
    remove_favorite,
)
from frontend.auth.state import is_admin, is_authenticated



def render_favorite_button(product: dict, key_prefix: str) -> None:
    if not is_authenticated():
        st.caption("Войдите, чтобы добавить запись в избранное.")
        return

    product_id = product["id"]
    is_favorite = product.get("is_favorite", False)
    button_text = "Убрать из избранного" if is_favorite else "В избранное"

    if st.button(button_text, key=f"{key_prefix}_favorite_{product_id}"):
        try:
            if is_favorite:
                response = remove_favorite(product_id)
            else:
                response = add_favorite(product_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend")
            return

        if response.ok:
            st.rerun()
        else:
            st.error(get_error_message(response))

def render_admin_actions(product_id: int, key_prefix: str) -> None:
    if not is_admin():
        return

    edit_column, delete_column = st.columns(2)

    if edit_column.button(
        "Редактировать",
        key=f"{key_prefix}_edit_{product_id}",
    ):
        st.session_state["edit_product_id"] = product_id
        st.switch_page("pages/edit_product.py")

    if delete_column.button(
        "Удалить",
        key=f"{key_prefix}_delete{product_id}",
        type="primary",
    ):
        try:
            response = delete_product(product_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend.")
            return

        if response.ok:
            st.success("Запись удаленна")
            st.switch_page("pages/catalog.py")
        else:
            st.error(get_error_message(response))

def render_product_card(product: dict) -> None:
    product_id = product["id"]

    with st.container(border=True):
        if product.get("image_url"):
            st.image(product["image_url"], use_container_width=True)
        else:
            st.info("изображение не добавлено")

        st.subheader(product["title"])
        st.write(product.get("short_description", ""))

        render_favorite_button(product, key_prefix="card")
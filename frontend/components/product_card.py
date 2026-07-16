import streamlit as st
import requests

from frontend.api.client import add_favorite, remove_favorite
from frontend.auth.state import is_authenticated, is_admin


def render_product_card(product: dict, key_prefix: str = "") -> None:

    name = product.get("name") or product.get("title", "Без названия")

    product_id = product.get("id", 0)
    unique_key = f"{key_prefix}_{product_id}" if key_prefix else str(product_id)

    st.subheader(name)

    image_url = product.get("image_url") or product.get("thumbnail")
    if image_url:
        try:
            st.image(image_url, width=200)
        except Exception:
            st.info("Не удалось загрузить изображение")
    else:
        st.info("Изображение не добавлено")

    desc = product.get("description", "")
    if desc:
        st.caption(desc[:150] + "…" if len(desc) > 150 else desc)

    price = product.get("price")
    size = product.get("size")
    if price is not None:
        st.write(f"💰 Цена: {price} руб.")
    if size is not None:
        st.write(f"📏 Размер: {size}")

    if is_authenticated():
        is_fav = product.get("is_favorite", False)

        if is_fav:
            if st.button("❤️ В избранном", key=f"rm_fav_{unique_key}"):
                try:
                    resp = remove_favorite(product_id)
                    if resp.ok:
                        st.success("Удалено из избранного")
                        st.rerun()
                    else:
                        st.error("Не удалось удалить из избранного")
                except requests.RequestException:
                    st.error("Ошибка соединения с сервером")
        else:
            if st.button("🤍 Добавить в избранное", key=f"add_fav_{unique_key}"):
                try:
                    resp = add_favorite(product_id)
                    if resp.ok:
                        st.success("Добавлено в избранное!")
                        st.rerun()
                    else:
                        st.error("Не удалось добавить в избранное")
                except requests.RequestException:
                    st.error("Ошибка соединения с сервером")

    if is_admin():
        with st.expander("⚙️ Администрирование"):
            if st.button("✏️ Редактировать", key=f"edit_{unique_key}"):
                st.session_state["edit_product_id"] = product_id
                st.switch_page("pages/edit_product.py")
            if st.button("🗑️ Удалить", key=f"delete_{unique_key}"):
                from frontend.api.client import delete_product
                try:
                    resp = delete_product(product_id)
                    if resp.ok:
                        st.success("Товар удалён")
                        st.rerun()
                    else:
                        st.error("Не удалось удалить товар")
                except requests.RequestException:
                    st.error("Ошибка соединения с сервером")

    st.divider()
import requests
import streamlit as st

from frontend.api.client import get_error_message, get_favorites, get_product
from frontend.auth.state import require_login
from frontend.components.product_card import render_product_card

require_login()

st.header("Избранное")

try:
    response = get_favorites()
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

try:
    favorites_data = response.json()
except ValueError:
    st.error("Некорректный ответ сервера.")
    st.stop()

if not isinstance(favorites_data, list):
    st.error("Некорректный формат данных от сервера.")
    st.stop()

if not favorites_data:
    st.info("У вас пока нет избранных товаров.")
    st.stop()

# Для каждого избранного получаем полную информацию о продукте
products = []
with st.spinner("Загрузка избранных товаров..."):
    for fav in favorites_data:
        product_id = fav.get("product_id")
        if not product_id:
            continue
        try:
            resp = get_product(product_id)
            if resp.ok:
                product = resp.json()
                # Унификация названия (на случай title vs name)
                if "name" not in product and "title" in product:
                    product["name"] = product["title"]
                if "name" not in product:
                    product["name"] = "Без названия"
                # Помечаем, что товар в избранном
                product["is_favorite"] = True
                products.append(product)
            else:
                st.warning(f"Товар с ID {product_id} не найден")
        except requests.RequestException:
            st.warning(f"Ошибка загрузки товара {product_id}")

if not products:
    st.info("У вас пока нет избранных товаров.")
    st.stop()

# Отрисовка карточек
columns = st.columns(3)
for index, product in enumerate(products):
    with columns[index % 3]:
        render_product_card(product)
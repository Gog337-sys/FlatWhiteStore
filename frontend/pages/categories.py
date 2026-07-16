import streamlit as st
import requests
from frontend.api.client import get_products, get_error_message

st.header("Каталог товаров")

# 1. Извлекаем переданную категорию (если есть)
preselected_category = st.session_state.pop("filter_category", None)

# 2. Загружаем товары
try:
    resp = get_products()
except requests.RequestException:
    st.error("Не удалось загрузить товары. Проверьте соединение с сервером.")
    st.stop()

if not resp.ok:
    st.error(get_error_message(resp))
    st.stop()

try:
    products = resp.json()
except ValueError:
    st.error("Некорректный ответ сервера.")
    st.stop()

if not products:
    st.info("Товары отсутствуют.")
    st.stop()

# 3. Вспомогательная функция для получения названия категории
def get_category_name(product):
    cat = product.get("category")
    if isinstance(cat, dict):
        return cat.get("name", "Без категории")
    return cat or "Без категории"

# 4. Список уникальных категорий (названия)
category_names = sorted({get_category_name(p) for p in products})

# 5. Индекс категории по умолчанию
default_index = 0
if preselected_category and preselected_category in category_names:
    default_index = category_names.index(preselected_category)

# 6. Виджет выбора категории
selected_category = st.selectbox(
    "Фильтр по категории",
    options=category_names,
    index=default_index
)

# 7. Фильтрация товаров
filtered_products = [
    p for p in products
    if get_category_name(p) == selected_category
]

# 8. Отображение
st.subheader(f"Товары в категории «{selected_category}»")
st.write(f"Найдено: {len(filtered_products)}")

for product in filtered_products:
    with st.container():
        st.markdown(f"**{product.get('name', 'Без названия')}**")
        st.write(f"Цена: {product.get('price', '—')} руб.")
        if product.get("description"):
            st.caption(product["description"])
        st.divider()
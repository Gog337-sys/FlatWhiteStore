import requests
import streamlit as st

from frontend.api.client import get_error_message, get_profile
from frontend.auth.state import clear_auth, require_login

require_login()
st.header("Профиль")

# Профиль уже должен быть загружен в is_authenticated() или из прошлых запросов
profile = st.session_state.get("profile")

# Если вдруг профиля нет — делаем один запрос
if not profile:
    try:
        resp = get_profile()
        if resp.ok:
            profile = resp.json()
            st.session_state["profile"] = profile
        else:
            st.error(get_error_message(resp))
            st.stop()
    except requests.RequestException:
        st.error("Нет связи с backend")
        st.stop()
    except ValueError:
        st.error("Некорректный ответ сервера")
        st.stop()

if not isinstance(profile, dict):
    st.error("Некорректный формат данных профиля.")
    st.stop()


st.write(f"**Почта:** {profile.get('email', 'Не указано')}")
st.write(f"**Роль:** {profile.get('role', 'user')}")

if st.button("Выйти", type="primary"):
    clear_auth()
    st.success("Вы вышли из аккаунта.")
    st.switch_page("pages/login.py")
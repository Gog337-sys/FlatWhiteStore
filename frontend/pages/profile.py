import requests
import streamlit as st

from frontend.api.client import get_error_message, get_profile
from frontend.auth.state import clear_auth, require_login, save_auth


require_login()
st.header("Профиль")

try:
    response = get_profile()
except requests.RequestException:
    st.error("Не удалось выполнить запрос к  backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

profile = response.json()
save_auth(st.session_state["access_token"], profile)

st.write(f"**ФИО:** {profile.get('full_name', 'Не указано')}")
st.write(f"**Почта:** {profile.get('email', 'Не указано')}")
st.write(f"**Роль:** {profile.get('role', 'user')}")

if st.button("Выйти", type="primary"):
    clear_auth()
    st.switch_page("pages/login.py")
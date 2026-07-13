import streamlit as st

def save_auth(access_token: str, profile: dict) -> None:
    st.session_state["access_token"] = access_token
    st.session_state["profile"] = profile

def clear_auth() -> None:
    st.session_state.pop("access_token", None)
    st.session_state.pop("profile", None)

def is_authenticated() -> bool:
    return bool(st.session_state.get("access_token"))

def current_profile() -> dict | None:
    return st.session_state.get("profile")

def is_admin() -> bool:
    profile = current_profile()
    return bool(profile and profile.get("role") == "admin")

def require_login() -> None:

    if not is_authenticated():
        st.warning("Пожалуйста, войдите в аккаунт")
        st.switch_page("pages/login.py")
        st.stop()

def require_admin() -> None:

    if not is_authenticated():
        st.warning("Пожалуйста, войдите в аккаунт")
        st.switch_page("pages/login.py")
        st.stop()
    if not is_admin():
        st.error("У вас недостаточно прав для доступа к этой странице.")
        st.stop()
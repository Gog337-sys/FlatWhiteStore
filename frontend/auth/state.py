import streamlit as st
from frontend.cookie_manager import get_auth_cookie, remove_auth_cookie
from frontend.api.client import get_profile

def save_auth(access_token: str, profile: dict) -> None:

    get_auth_cookie(access_token)


    st.session_state["access_token"] = access_token
    st.session_state["profile"] = profile
    st.session_state["authenticated"] = True
    st.session_state.pop("_auth_failed", None)


    if not st.session_state.get("_cookie_rerun_done"):
        st.session_state["_cookie_rerun_done"] = True
        st.rerun()

def clear_auth() -> None:
    remove_auth_cookie()
    st.session_state.pop("access_token", None)
    st.session_state.pop("profile", None)
    st.session_state.pop("authenticated", None)
    st.session_state.pop("_auth_failed", None)
    st.session_state.pop("_cookie_rerun_done", None)

def is_authenticated() -> bool:
    if st.session_state.get("authenticated", False):
        return True
    if st.session_state.get("_auth_failed", False):
        return False


    token = st.session_state.get("access_token")
    if not token:
        token = get_auth_cookie()   # чтение куки (без аргументов)
        if token:
            st.session_state["access_token"] = token

    if not token:
        st.session_state["_auth_failed"] = True
        return False

    try:
        response = get_profile()
        if response.ok:
            profile = response.json()
            st.session_state["profile"] = profile
            st.session_state["authenticated"] = True
            st.session_state.pop("_auth_failed", None)
            return True
        else:
            clear_auth()
            return False
    except Exception:
        clear_auth()
        return False

def current_profile() -> dict | None:
    return st.session_state.get("profile")

def is_admin() -> bool:
    profile = current_profile()
    return bool(profile and profile.get("is_admin") is True)

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
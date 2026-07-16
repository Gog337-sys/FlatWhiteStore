import streamlit as st
from streamlit_cookies_controller import CookieController

controller = CookieController()

def get_cookie_controller():
    if "cookie_controller" not in st.session_state:
        st.session_state.cookie_controller = CookieController()
    return st.session_state.cookie_controller

def set_auth_cookie(access_token: str):
    controller = get_cookie_controller()
    controller.set(
        "access_token",
        access_token,
        max_age=604800,
        path="/",
        secure=False,
        same_site="Lax"
    )

def get_auth_cookie(access_token=None):

    if access_token is not None:
        # Режим записи
        controller.set(
            "access_token",
            access_token,
            max_age=604800,
            path="/",
            secure=False,
            same_site="Lax"
        )
        return access_token
    else:
        return controller.get("access_token")

def remove_auth_cookie():
    try:
        controller.remove("access_token", path="/")
    except KeyError:
        pass
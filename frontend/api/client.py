from starlette.status import HTTP_401_UNAUTHORIZED
import streamlit as st
import json
import requests

BACKEND_URL = "http://127.0.0.1:8000"

LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login/"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register/"
PRODUCT_ENDPOINT = f"{BACKEND_URL}/products/"
CATEGORY_ENDPOINT = f"{BACKEND_URL}/category/"
FAVORITES_ENDPOINT = f"{BACKEND_URL}/favorites/"
PROFILE_ENDPOINT = f"{BACKEND_URL}/profile/"


def register(name: str, email: str, password: str) -> requests.Response:
    data = {"name": name, "email": email, "password": password}
    return requests.post(REGISTER_ENDPOINT, json=data)


def login(email, password):
    data = {"email": email, "password": password}
    return requests.post(LOGIN_ENDPOINT, json=data)


def request_with_authorization_header(
        request_type: str,
        endpoint: str,
        params: dict | None = None,
        payload: dict | None = None,
) -> requests.Response:

    token = st.session_state.get("access_token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    if request_type == "GET":
        response = requests.get(endpoint, headers=headers, params=params)
    elif request_type == "POST":
        response = requests.post(endpoint, headers=headers, json=payload)
    elif request_type == "PATCH":
        response = requests.patch(endpoint, headers=headers, json=payload)
    elif request_type == "DELETE":
        response = requests.delete(endpoint, headers=headers, params=params)
    else:
        raise ValueError("Неизвестный тип запроса")

    if response.status_code == HTTP_401_UNAUTHORIZED:
        # При 401 очищаем авторизацию (сессию и URL)
        st.session_state.pop("access_token", None)
        st.session_state.pop("profile", None)
        st.session_state.pop("authenticated", None)
        st.query_params.clear()

    return response


def get_error_message(response: requests.Response) -> str:
    try:
        detail = response.json().get("detail")
        return str(detail or f"Ошибка backend: HTTP {response.status_code}")
    except ValueError:
        return f"Ошибка backend: HTTP {response.status_code}"


def get_profile(token: str | None = None) -> requests.Response:

    if token:
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(PROFILE_ENDPOINT, headers=headers)
    return request_with_authorization_header("GET", PROFILE_ENDPOINT)


def get_products() -> requests.Response:
    return request_with_authorization_header("GET", PRODUCT_ENDPOINT)


def get_product(product_id: int) -> requests.Response:
    endpoint = f"{PRODUCT_ENDPOINT}{product_id}/"
    return request_with_authorization_header("GET", endpoint)


def get_favorites() -> requests.Response:
    return request_with_authorization_header("GET", FAVORITES_ENDPOINT)


def add_favorite(product_id: int) -> requests.Response:
    return request_with_authorization_header(
        "POST",
        FAVORITES_ENDPOINT,
        payload={"product_id": product_id}
    )


def remove_favorite(product_id: int) -> requests.Response:
    endpoint = f"{FAVORITES_ENDPOINT}{product_id}/"
    return request_with_authorization_header("DELETE", endpoint)


def create_product(payload: dict) -> requests.Response:
    return request_with_authorization_header(
        "POST",
        PRODUCT_ENDPOINT,
        payload=payload,
    )


def update_product(product_id: int, payload: dict) -> requests.Response:
    endpoint = f"{PRODUCT_ENDPOINT}{product_id}/"
    return request_with_authorization_header(
        "PUT",
        endpoint,
        payload=payload,
    )


def delete_product(product_id: int) -> requests.Response:
    endpoint = f"{PRODUCT_ENDPOINT}{product_id}/"
    return request_with_authorization_header("DELETE", endpoint)


def get_categories() -> requests.Response:
    return request_with_authorization_header("GET", CATEGORY_ENDPOINT)


def add_category(product_id: int) -> requests.Response:
    endpoint = f"{CATEGORY_ENDPOINT}{product_id}/"
    return request_with_authorization_header("POST", endpoint)


def remove_category(product_id: int) -> requests.Response:
    endpoint = f"{CATEGORY_ENDPOINT}{product_id}/"
    return request_with_authorization_header("DELETE", endpoint)
from starlette.status import HTTP_401_UNAUTHORIZED
from streamlit import session_state
import json

import requests

BACKEND_URL = "http://127.0.0.1:8000"

LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login/"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register/"
PRODUCT_ENDPOINT = f"{BACKEND_URL}/product/"
CATEGORY_ENDPOINT = f"{BACKEND_URL}/category/"
FAVORITES_ENDPOINT = f"{BACKEND_URL}/favorites/"
PROFILE_ENDPOINT = f"{BACKEND_URL}/profile/"


def register(email, password, fio):
    data = {"email": email, "password": password, "full_name": fio}
    with requests.Session() as s:
        response = s.post(REGISTER_ENDPOINT, json=data) # , headers={"Authorization": f"Bearer {token}"}

    return response


def login(email, password):
    data = {"email": email, "password": password}

    with requests.Session() as s:
        response = s.post(LOGIN_ENDPOINT, json=data) # , headers={"Authorization": f"Bearer {token}"}

    return response


# Функция для получения ответа с бэкенда с указанием header'a, который поможет понять что пользователь авторизован
def request_with_authorization_header(
        request_type: str,
        endpoint: str,
        params: dict | None = None,
        payload: dict | None = None,
) -> requests.Response:
    headers = {
        "Authorization": f"Bearer {session_state['access_token']}"
    }

    if request_type == "GET":
        response = requests.get(endpoint, headers=headers, params=params)
    elif request_type == "POST":
        response = requests.post(endpoint, headers=headers, params=params, json=payload)
    elif request_type == "PATCH":
        response = requests.patch(endpoint, headers=headers, params=params, json=payload)
    elif request_type == "DELETE":
        response = requests.delete(endpoint, headers=headers, params=params)
    else:
        raise  ValueError("Неизвестный тип запроса")

    if response.status_code == 401:
        session_state.pop("access_token", None)
        session_state.pop("profile", None)

    return response

def get_error_message(response: requests.Response) -> str:
    try:
        detail = response.json().get("detail")
        return str(detail or f"Ошибка backend: HTTP {response.status_code}")
    except ValueError:
        return f"Ошибка backend: HTTP {response.status_code}"

def get_profile() -> requests.Response:
    return request_with_authorization_header("GET", PROFILE_ENDPOINT)

def get_products() -> requests.Response:
    if session_state.get("access_token"):
        return request_with_authorization_header("GET", PRODUCT_ENDPOINT)
    return requests.get(PRODUCT_ENDPOINT)

def get_product(product_id: int) -> requests.Response:
    endpoint = f"{PRODUCT_ENDPOINT}{product_id}/"

    if session_state.get("access_token"):
        return request_with_authorization_header("GET", endpoint)
    return requests.get(endpoint)

def get_favorites() -> requests.Response:
    return request_with_authorization_header("GET", FAVORITES_ENDPOINT)

def add_favorite(product_id: int) -> requests.Response:
    endpoint = f"{FAVORITES_ENDPOINT}{product_id}/"
    return request_with_authorization_header("POST", endpoint)

def remove_favorite(product_id: int) -> requests.Response:
    endpoint = f"{FAVORITES_ENDPOINT}{product_id}/"
    return  request_with_authorization_header("DELETE", endpoint)

def create_product(payload: dict) -> requests.Response:
    return request_with_authorization_header(
        "POST",
        PRODUCT_ENDPOINT,
        payload=payload,
    )

def update_product(product_id: int, payload: dict) -> requests.Response:
    endpoint = f"{PRODUCT_ENDPOINT}{product_id}/"
    return  request_with_authorization_header(
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

if __name__ == '__main__':
    register_response = register()

    print(register_response)
    print(json.dumps(register_response, indent=4))

    login_response = login()
    print(login_response)
    print(json.dumps(login_response, indent=4))
from starlette.status import HTTP_401_UNAUTHORIZED
from streamlit import session_state
import json

import requests

BACKEND_URL = "http://127.0.0.1:8000"

LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login/"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register/"


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
def request_with_authorization_header(request_type: str, endpoint: str, params: dict = None, payload: dict = None):
    if not session_state.get('access_token'):
        return HTTP_401_UNAUTHORIZED
    with requests.Session() as s:
        s.headers.update({"Authorization": f"Bearer {session_state.get('access_token')}"})
        if request_type == "POST":
            response = s.post(endpoint, json=payload, params=params)
        elif request_type == "GET":
            response = s.get(endpoint, params=params)
        elif request_type == "PUT":
            response = s.put(endpoint, json=payload, params=params)
        elif request_type == "DELETE":
            response = s.delete(endpoint, params=params)
    return response


# request_with_authorization_headerith_authorization_header(
#     "POST",
#     "/tanks/{id}",
#     params={"id": 1},
#     payload={"name": "blablabla"},
# )


if __name__ == '__main__':
    register_response = register()

    print(register_response)
    print(json.dumps(register_response, indent=4))

    login_response = login()
    print(login_response)
    print(json.dumps(login_response, indent=4))
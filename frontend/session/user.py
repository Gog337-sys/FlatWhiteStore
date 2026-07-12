from streamlit import session_state


# Функция, которая сохраняет в памяти приложение информацию о пользователе: access_token
def save_access_token(data: dict):
    print(data)
    session_state["access_token"] = data.get("access_token")
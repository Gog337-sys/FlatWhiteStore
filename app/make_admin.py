import sqlite3

# Подставьте имя вашей БД (обычно products.db)
conn = sqlite3.connect("products.db")
cursor = conn.cursor()

# Замените email на свой
email = "admin@example.com"

cursor.execute("UPDATE users SET is_admin = 1 WHERE email = ?", (email,))
conn.commit()

if cursor.rowcount > 0:
    print(f"Пользователь {email} теперь администратор.")
else:
    print(f"Пользователь с email {email} не найден.")

conn.close()
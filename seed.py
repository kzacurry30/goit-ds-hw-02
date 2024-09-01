import sqlite3
from faker import Faker


def connect_db(db_name='task_management.db'):
    """Підключення до бази даних і створення курсора."""
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()


def insert_statuses(cursor):
    """Вставка унікальних статусів у таблицю статусів."""
    statuses = [('new',), ('in progress',), ('completed',)]
    cursor.executemany("INSERT OR IGNORE INTO status (name) VALUES (?)", statuses)


def insert_users_and_tasks(cursor, num_users=10, tasks_per_user=5):
    """Вставка користувачів та їх завдань до бази даних."""
    fake = Faker()

    for _ in range(num_users):
        fullname = fake.name()
        email = fake.unique.email()

        # Вставка користувача
        cursor.execute("INSERT INTO users (fullname, email) VALUES (?, ?)", (fullname, email))
        user_id = cursor.lastrowid

        for _ in range(tasks_per_user):
            title = fake.sentence(nb_words=4)
            description = fake.text(max_nb_chars=200)
            status_id = fake.random_int(min=1, max=3)  # Випадковий статус (1-3)

            # Вставка завдання
            cursor.execute(
                "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
                (title, description, status_id, user_id)
            )


def main():
    """Основна функція для виконання скрипта."""
    conn, cursor = connect_db()

    try:
        insert_statuses(cursor)
        insert_users_and_tasks(cursor)

        # Фіксація змін у базі даних
        conn.commit()
    except Exception as e:
        print(f"Виникла помилка: {e}")
        conn.rollback()
    finally:
        # Закриття з'єднання
        conn.close()


if __name__ == '__main__':
    main()


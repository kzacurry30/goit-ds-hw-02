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


# Запити:

def get_tasks_by_user(cursor, user_id):
    """Отримати всі завдання певного користувача за його user_id."""
    cursor.execute('''
        SELECT tasks.id, tasks.title, tasks.description, status.name AS status
        FROM tasks
        JOIN status ON tasks.status_id = status.id
        WHERE tasks.user_id = ?;
    ''', (user_id,))
    return cursor.fetchall()


def get_tasks_by_status(cursor, status_name):
    """Вибрати завдання за певним статусом."""
    cursor.execute('''
        SELECT tasks.id, tasks.title, tasks.description, users.fullname
        FROM tasks
        JOIN status ON tasks.status_id = status.id
        JOIN users ON tasks.user_id = users.id
        WHERE status.name = ?;
    ''', (status_name,))
    return cursor.fetchall()


def update_task_status(cursor, task_id, new_status):
    """Оновити статус конкретного завдання."""
    cursor.execute('''
        UPDATE tasks
        SET status_id = (SELECT id FROM status WHERE name = ?)
        WHERE id = ?;
    ''', (new_status, task_id))


def get_users_without_tasks(cursor):
    """Отримати список користувачів, які не мають жодного завдання."""
    cursor.execute('''
        SELECT fullname, email
        FROM users
        WHERE id NOT IN (
            SELECT user_id FROM tasks
        );
    ''')
    return cursor.fetchall()


def add_new_task(cursor, user_id, title, description, status_name='new'):
    """Додати нове завдання для конкретного користувача."""
    cursor.execute('''
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (?, ?, (SELECT id FROM status WHERE name = ?), ?);
    ''', (title, description, status_name, user_id))


def get_uncompleted_tasks(cursor):
    """Отримати всі завдання, які ще не завершено."""
    cursor.execute('''
        SELECT tasks.id, tasks.title, tasks.description, users.fullname
        FROM tasks
        JOIN status ON tasks.status_id = status.id
        JOIN users ON tasks.user_id = users.id
        WHERE status.name != 'completed';
    ''')
    return cursor.fetchall()


def delete_task(cursor, task_id):
    """Видалити конкретне завдання."""
    cursor.execute('''
        DELETE FROM tasks
        WHERE id = ?;
    ''', (task_id,))


def find_users_by_email(cursor, email_pattern):
    """Знайти користувачів з певною електронною поштою."""
    cursor.execute('''
        SELECT id, fullname, email
        FROM users
        WHERE email LIKE ?;
    ''', (email_pattern,))
    return cursor.fetchall()


def update_user_name(cursor, user_id, new_name):
    """Оновити ім'я користувача."""
    cursor.execute('''
        UPDATE users
        SET fullname = ?
        WHERE id = ?;
    ''', (new_name, user_id))


def get_task_count_by_status(cursor):
    """Отримати кількість завдань для кожного статусу."""
    cursor.execute('''
        SELECT status.name, COUNT(tasks.id) AS task_count
        FROM tasks
        JOIN status ON tasks.status_id = status.id
        GROUP BY status.name;
    ''')
    return cursor.fetchall()


def get_tasks_by_email_domain(cursor, domain):
    """Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти."""
    cursor.execute('''
        SELECT tasks.id, tasks.title, tasks.description, users.fullname, users.email
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        WHERE users.email LIKE ?;
    ''', (f'%{domain}',))
    return cursor.fetchall()


def get_tasks_without_description(cursor):
    """Отримати список завдань, що не мають опису."""
    cursor.execute('''
        SELECT id, title
        FROM tasks
        WHERE description IS NULL OR description = '';
    ''')
    return cursor.fetchall()


def get_users_and_tasks_in_progress(cursor):
    """Вибрати користувачів та їхні завдання, які є у статусі 'in progress'."""
    cursor.execute('''
        SELECT users.fullname, tasks.title, tasks.description
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        JOIN status ON tasks.status_id = status.id
        WHERE status.name = 'in progress';
    ''')
    return cursor.fetchall()


def get_users_and_task_count(cursor):
    """Отримати користувачів та кількість їхніх завдань."""
    cursor.execute('''
        SELECT users.fullname, COUNT(tasks.id) AS task_count
        FROM users
        LEFT JOIN tasks ON users.id = tasks.user_id
        GROUP BY users.fullname;
    ''')
    return cursor.fetchall()


def main():
    """Основна функція для виконання скрипта."""
    conn, cursor = connect_db()

    try:
        insert_statuses(cursor)
        insert_users_and_tasks(cursor)

        # Деякі приклади використання функцій:
        print(get_tasks_by_user(cursor, 1))
        print(get_tasks_by_status(cursor, 'new'))
        update_task_status(cursor, 1, 'in progress')
        print(get_users_without_tasks(cursor))
        add_new_task(cursor, 1, "New Task", "This is a new task")
        print(get_uncompleted_tasks(cursor))
        delete_task(cursor, 1)
        print(find_users_by_email(cursor, '%@gmail.com'))
        update_user_name(cursor, 1, "Updated User Name")
        print(get_task_count_by_status(cursor))
        print(get_tasks_by_email_domain(cursor, 'example.com'))
        print(get_tasks_without_description(cursor))
        print(get_users_and_tasks_in_progress(cursor))
        print(get_users_and_task_count(cursor))

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

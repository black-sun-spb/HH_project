# HH_project

Приложение для сбора и анализа вакансий с сайта [hh.ru](https://hh.ru) через публичный API. Данные сохраняются в базу данных PostgreSQL, после чего можно выполнять запросы по компаниям, зарплате, ключевым словам и т.д.

---

## ⚙️ Функциональность

- Получение информации о компаниях (работодателях)
- Получение информации о вакансиях этих компаний
- Сохранение данных в PostgreSQL
- Отображение:
  - Всех компаний и количества вакансий у каждой
  - Всех вакансий с указанием зарплаты и ссылки
  - Средней зарплаты по всем вакансиям
  - Вакансий с зарплатой выше средней
  - Вакансий, содержащих ключевое слово в названии

---

## 🧰 Технологии

- Python 3.10+
- PostgreSQL
- [psycopg2](https://pypi.org/project/psycopg2/)
- [requests](https://pypi.org/project/requests/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📁 Структура проекта

```
HH_project/
│
├── main_clean.py # Главный исполняемый файл
├── .env # Переменные окружения для подключения к БД
├── db/
│ ├── db_config.py # Подключение к БД
│ ├── db_init.py # Создание базы данных
│ └── db_manager.py # Класс DBManager с SQL-запросами
├── hh/
│ └── hh_api.py # Работа с API hh.ru
├── requirements.txt # Зависимости проекта
└── README.md
```


---

## ⚡ Установка

1. Клонируй репозиторий:


```
git clone https://github.com/your_username/HH_project.git
cd HH_project
```

2. Установи зависимости:

```
pip install -r requirements.txt
```

3. Настрой файл .env в корне проекта:

```
DB_NAME=hh_db
DB_USER=postgres
DB_PASSWORD=ваш_пароль
DB_HOST=localhost
DB_PORT=5432
```

4. Создай базу данных (опционально):

```
python db/db_init.py
```

5. Запусти приложение:

```
python main_clean.py
```

## 📌 Примечание
API HH ограничивает количество запросов — между запросами есть пауза (time.sleep(0.2)).

По умолчанию используются ID 10 компаний, но ты можешь изменить список в hh_api.py.

## 📝 Автор

👤 black-sun-spb

📧 Telegram (@black_sun_rkd)

# Лицензия
Проект лицензирован под [MIT License](LICENSE).
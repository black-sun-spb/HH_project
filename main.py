from api.hh_api import HHApi
from db.db_manager import DBManager
from db.db_config import get_connection

def main():
    # Получение данных
    api = HHApi()
    employers = api.get_employers()
    vacancies = api.get_vacancies_for_employers(employers)

    # Работа с базой
    conn = get_connection()
    db = DBManager(conn)

    db.create_tables()
    db.insert_companies(employers)
    db.insert_vacancies(vacancies)

    # Пример использования
    print(db.get_companies_and_vacancies_count())

if __name__ == '__main__':
    main()

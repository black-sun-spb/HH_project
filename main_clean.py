from api.hh_api import HHApi
from db.db_config import get_connection
from db.db_manager import DBManager


def main():
    print("Подключение к базе данных...")
    conn = get_connection()
    db = DBManager(conn)
    hh_api = HHApi()

    print("Создаём таблицы (если ещё не созданы)...")
    db.create_tables()

    print("Получаем компании с hh.ru...")
    employers = hh_api.get_employers()

    print("Сохраняем компании в базу...")
    for company in employers:
        db.insert_company(company)

    print("Получаем вакансии для компаний...")
    vacancies = hh_api.get_vacancies_for_employers(employers)

    print("Сохраняем вакансии в базу...")
    for vacancy in vacancies:
        db.insert_vacancy(vacancy)

    print("\nДобро пожаловать в приложение для просмотра вакансий и компаний!\n")

    print("Список компаний и количество вакансий в каждой из них:\n")
    companies = db.get_companies_and_vacancies_count()
    for name, count in companies:
        print(f"{name}: {count}")

    print("\nВсе вакансии с указанием компании, зарплаты и ссылки:\n")
    all_vacancies = db.get_all_vacancies()
    for comp_name, vac_name, salary, url in all_vacancies:
        print(f"{comp_name} — {vac_name} — {salary} — {url}")

    avg_salary = db.get_avg_salary()
    print(f"\nСредняя зарплата по вакансиям: {avg_salary:.2f}\n")

    print("Вакансии с зарплатой выше средней:\n")
    higher_vacancies = db.get_vacancies_with_higher_salary()
    for comp_name, vac_name, salary in higher_vacancies:
        print(f"{comp_name} — {vac_name} — {salary}")

    keyword = input(
        "\nВведите ключевое слово для поиска вакансий (например, python): "
    ).strip()
    matching_vacancies = db.get_vacancies_with_keyword(keyword)
    print(f"\nВакансии с ключевым словом '{keyword}':\n")
    for comp_name, vac_name, salary in matching_vacancies:
        print(f"{comp_name} — {vac_name} — {salary}")

    conn.close()


if __name__ == "__main__":
    main()

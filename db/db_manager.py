from typing import Dict, List, Tuple


class DBManager:
    def __init__(self, conn):
        self.conn = conn

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS companies (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    area TEXT,
                    site_url TEXT
                );
            """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS vacancies (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    key_skills TEXT[],
                    salary_from INTEGER,
                    salary_to INTEGER,
                    currency TEXT,
                    published_at TIMESTAMP,
                    company_id INTEGER REFERENCES companies(id),
                    url TEXT
                );
            """
            )
            self.conn.commit()

    def insert_company(self, company: Dict):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO companies (id, name, description, area, site_url)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """,
                (
                    company["id"],
                    company["name"],
                    company.get("description"),
                    company.get("area", {}).get("name"),
                    company.get("site_url"),
                ),
            )
            self.conn.commit()

    def insert_vacancy(self, vacancy: Dict):
        key_skills = (
            [skill["name"] for skill in vacancy.get("key_skills", [])]
            if vacancy.get("key_skills")
            else []
        )
        salary = vacancy.get("salary")
        salary_from = salary.get("from") if salary else None
        salary_to = salary.get("to") if salary else None
        currency = salary.get("currency") if salary else None

        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO vacancies (
                    id, name, description, key_skills, salary_from,
                    salary_to, currency, published_at, company_id, url
                 )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """,
                (
                    vacancy["id"],
                    vacancy["name"],
                    vacancy.get("description"),
                    key_skills,
                    salary_from,
                    salary_to,
                    currency,
                    vacancy.get("published_at"),
                    vacancy["employer"]["id"],
                    vacancy.get("alternate_url"),
                ),
            )
            self.conn.commit()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Возвращает список компаний и количество вакансий у каждой компании
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.name, COUNT(v.id) AS vacancies_count
                FROM companies c
                LEFT JOIN vacancies v ON c.id = v.company_id
                GROUP BY c.name
                ORDER BY vacancies_count DESC;
            """
            )
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, str, str]]:
        """
        Возвращает список всех вакансий с названием компании, названием вакансии,
        зарплатой и ссылкой на вакансию
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.name, v.name,
                    CASE
                        WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN
                            CONCAT(v.salary_from, ' - ', v.salary_to, ' ', v.currency)
                        WHEN v.salary_from IS NOT NULL THEN
                            CONCAT('от ', v.salary_from, ' ', v.currency)
                        WHEN v.salary_to IS NOT NULL THEN
                            CONCAT('до ', v.salary_to, ' ', v.currency)
                        ELSE 'Не указана'
                    END AS salary,
                    v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                ORDER BY c.name;
            """
            )
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Возвращает среднюю зарплату по вакансиям, усредняя по среднему значению salary_from и salary_to.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2.0) AS avg_salary
                FROM vacancies
                WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL;
            """
            )
            result = cur.fetchone()
            avg_salary = result[0]
            return avg_salary if avg_salary is not None else 0.0

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, str]]:
        """
        Возвращает вакансии, у которых зарплата выше средней по всем вакансиям
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                WITH avg_salary AS (
                    SELECT AVG((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2.0) AS avg_sal
                    FROM vacancies
                    WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
                )
                SELECT c.name, v.name,
                    CASE
                        WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN
                            CONCAT(v.salary_from, ' - ', v.salary_to, ' ', v.currency)
                        WHEN v.salary_from IS NOT NULL THEN
                            CONCAT('от ', v.salary_from, ' ', v.currency)
                        WHEN v.salary_to IS NOT NULL THEN
                            CONCAT('до ', v.salary_to, ' ', v.currency)
                        ELSE 'Не указана'
                    END AS salary
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id,
                avg_salary
                WHERE ((COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2.0) > avg_salary.avg_sal
                ORDER BY salary DESC;
            """
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, str]]:
        """
        Возвращает вакансии, в названии которых содержится ключевое слово (поиск case-insensitive)
        """
        like_pattern = f"%{keyword.lower()}%"
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.name, v.name,
                    CASE
                        WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN
                            CONCAT(v.salary_from, ' - ', v.salary_to, ' ', v.currency)
                        WHEN v.salary_from IS NOT NULL THEN
                            CONCAT('от ', v.salary_from, ' ', v.currency)
                        WHEN v.salary_to IS NOT NULL THEN
                            CONCAT('до ', v.salary_to, ' ', v.currency)
                        ELSE 'Не указана'
                    END AS salary
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE LOWER(v.name) LIKE %s
                ORDER BY c.name;
            """,
                (like_pattern,),
            )
            return cur.fetchall()

from typing import List, Dict
import psycopg2

class DBManager:
    def __init__(self, conn):
        self.conn = conn

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute(open('create_tables.sql', 'r').read())
        self.conn.commit()

    def insert_companies(self, companies: List[Dict]):
        with self.conn.cursor() as cur:
            for company in companies:
                cur.execute("""
                    INSERT INTO companies (id, name, description, area, site_url)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (
                    company['id'], company['name'], company.get('description'),
                    company.get('area', {}).get('name'), company.get('site_url')
                ))
        self.conn.commit()

    def insert_vacancies(self, vacancies: List[Dict]):
        with self.conn.cursor() as cur:
            for v in vacancies:
                salary = v.get('salary') or {}
                cur.execute("""
                    INSERT INTO vacancies (id, name, description, key_skills,
                        salary_from, salary_to, currency, published_at, company_id, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (
                    v['id'], v['name'], v.get('description'), [],
                    salary.get('from'), salary.get('to'), salary.get('currency'),
                    v.get('published_at'), v['employer']['id'], v.get('alternate_url')
                ))
        self.conn.commit()

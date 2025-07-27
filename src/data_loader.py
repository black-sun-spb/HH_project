import requests
import psycopg2
import time

EMPLOYER_IDS = [1740, 3529, 78638, 15478, 2180, 10671, 227, 80, 64174, 1122462]

conn = psycopg2.connect(
    dbname='hh_db',
    user='your_user',
    password='your_pass',
    host='localhost'
)
cursor = conn.cursor()

def get_employer_data(employer_id):
    url = f'https://api.hh.ru/employers/{employer_id}'
    return requests.get(url).json()

def get_vacancies(employer_id):
    url = f'https://api.hh.ru/vacancies'
    params = {'employer_id': employer_id, 'per_page': 100}
    return requests.get(url, params=params).json().get('items', [])

def insert_data():
    for employer_id in EMPLOYER_IDS:
        company = get_employer_data(employer_id)
        cursor.execute("""
            INSERT INTO companies (id, name, description, area, site_url)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            int(company['id']),
            company['name'],
            company.get('description'),
            company['area']['name'] if company.get('area') else None,
            company.get('site_url')
        ))

        for vacancy in get_vacancies(employer_id):
            salary = vacancy.get('salary') or {}
            skills = [s['name'] for s in vacancy.get('key_skills', [])]
            cursor.execute("""
                INSERT INTO vacancies (id, name, description, key_skills, salary_from, salary_to, currency, published_at, company_id, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                int(vacancy['id']),
                vacancy['name'],
                vacancy['snippet']['requirement'] if vacancy.get('snippet') else None,
                skills,
                salary.get('from'),
                salary.get('to'),
                salary.get('currency'),
                vacancy['published_at'],
                int(employer_id),
                vacancy.get('alternate_url')
            ))

        time.sleep(1)

    conn.commit()
    cursor.close()
    conn.close()

insert_data()
git add .
git commit -m "Initial commit: project setup, structure and base code"

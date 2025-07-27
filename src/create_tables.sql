CREATE TABLE companies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    area TEXT,
    site_url TEXT
);

CREATE TABLE vacancies (
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

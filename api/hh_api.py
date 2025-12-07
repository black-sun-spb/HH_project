import time
from typing import Dict, List
import requests


class HHApi:
    def __init__(self):
        self.base_url = "https://api.hh.ru"
        # ID 10 компаний для примера
        self.employer_ids = [
            "9498120",
            "60377",
            "3529",
            "11041754",
            "8643040",
            "12025479",
            "32918",
            "2368",
            "2381",
            "1122462",
        ]

    def get_employers(self) -> List[Dict]:
        employers = []
        for eid in self.employer_ids:
            resp = requests.get(f"{self.base_url}/employers/{eid}")
            if resp.status_code == 200:
                employers.append(resp.json())
            time.sleep(0.2)
        return employers

    def get_vacancies_for_employers(self, employers: List[Dict]) -> List[Dict]:
        vacancies = []
        for emp in employers:
            eid = emp["id"]
            page = 0
            while True:
                resp = requests.get(
                    f"{self.base_url}/vacancies",
                    params={"employer_id": eid, "page": page, "per_page": 100},
                )
                if resp.status_code != 200:
                    break
                data = resp.json()
                vacancies.extend(data.get("items", []))
                if page >= data["pages"] - 1:
                    break
                page += 1
                time.sleep(0.3)
        return vacancies

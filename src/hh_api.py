import requests
from typing import List, Dict

class HHApi:
    def __init__(self):
        self.base_url = "https://api.hh.ru"
        self.employer_ids = ['1740', '3529', '78638', '15478', '1122462', '3776', '9498115', '2748', '64174', '2180']

    def get_employers(self) -> List[Dict]:
        return [requests.get(f"{self.base_url}/employers/{eid}").json() for eid in self.employer_ids]

    def get_vacancies_for_employers(self, employers: List[Dict]) -> List[Dict]:
        vacancies = []
        for emp in employers:
            eid = emp['id']
            response = requests.get(f"{self.base_url}/vacancies?employer_id={eid}&per_page=100")
            vacancies.extend(response.json().get('items', []))
        return vacancies

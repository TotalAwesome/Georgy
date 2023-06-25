###############################################
#
#           Модуль с ИТ вакансиями в регионе
#
###############################################


import requests
import json
from time import time, ctime
import traceback

# from db import GeorgyDB
from telegram.config import HH_FILTERS
from jobs.models import Jobs, JobsSource

class JobDb:
    
    def _check_new(self, vacancy: dict):
        joblist = Jobs.objects.filter(
            job_id=vacancy['id'], 
            published_at=vacancy['published_at']
        )
        if not joblist:
            return True
    
    def _add_vacancy(self, vacancy: dict):
        Jobs.objects.create(
            source=JobsSource.objects.get(name='HeadHunter'),
            job_id=vacancy['id'],
            name=vacancy['name'],
            salary_from=vacancy['salary'].get('from') if vacancy['salary'] is not None else None,
            salary_to=vacancy['salary'].get('to') if vacancy['salary'] is not None else None,
            currency=vacancy['salary'].get('currency') if vacancy['salary'] is not None else 'RUR',
            schedule=vacancy['schedule'].get('name'),
            employer_name=vacancy['employer'].get('name'),
            published_at=vacancy['published_at'],
            url=vacancy['alternate_url']
        )
        

class JobHhunter:

    url = 'https://api.hh.ru/'
    db = JobDb()

    def _prepare_link(self):
        payload_str = f'?text=&area={HH_FILTERS["area"]}&period={HH_FILTERS["period"]}'
        payload_str += ''.join(
            [f'&professional_role={spec}' for spec in HH_FILTERS['roles']]
            )
        return self.url + 'vacancies/'+payload_str + '&per_page=100'

    def get_vacancies_list(self):
        """
        Получение списка вакансий 
        """
        full_url = self._prepare_link()
        print(full_url)
        response = requests.get(full_url)
        vacancies = {}
        if response.status_code == 200:
            # json.dump(response.json(), open('response.json', 'w'))

            for i in response.json()['items']:
                tmp_json = requests.get(self.url + f'vacancies/{i["id"]}').json()
                # specs = [tmp_json['specializations'][item[0]]['id'] for item in enumerate(tmp_json['specializations'])]
                # if len(set(specs) - set(HH_FILTERS['specializations'])) == 0 and tmp_json['employer']['id'] not in HH_FILTERS['exclude_employer_id']:
                vacancies[i['id']] = tmp_json

        return vacancies

    def get_new_vacancies(self):
        """
        Получение только новых вакансий
        """
        vacancies = {}
        while not vacancies:
            try:
                vacancies = self.get_vacancies_list()
            except Exception:
                func_name = traceback.extract_stack()[-1].name
                print(ctime(time()), func_name, Exception)
        return list(filter(self.db._check_new, vacancies.values()))

    def _save_vacancy(self, vac):
        self.db._add_vacancy(vac)

    def short(self, string):
        '''
        Возращает укороченное описание вакансии
        '''
        if len(string) > 25:
            return string[:25] + ('...' if string[24] != ' ' else '')
        else:
            return string

    def check_new_vacancies(self):
        vac_list = self.get_new_vacancies()
        for vac in vac_list:
            self._save_vacancy(vac)

    def new_vacancies_msg(self, new_vacancies=None):
        if not new_vacancies:
            new_vacancies = self.get_new_vacancies()
        msg = ''
        for vac in new_vacancies:
            self._save_vacancy(vac)
            name = vac['name']
            employer = vac['employer']['name']
            salary = vac.get('salary')
            if salary:
                salary_from = salary.get('from', None)
                salary_to = salary.get('to', None)
            else:
                salary_from = salary_to = None
            url = vac['alternate_url']
            if salary_from != salary_to:
                if salary_from:
                    special = '👀 ' if salary_from > 100_000 else ''
                salary = f'{special}от {salary_from}' if salary_from != None else ''
                salary += f' до {salary_to}' if salary_to != None else ''
            else:
                salary = str(salary_from) if salary_from != None else ''
            if not salary:
                salary = 'З/П не указана'
            else:
                salary += ' ' + (vac['salary']['currency']
                                if vac['salary'] != None else 'RUR')
            msg += f'\n[{name}]({url})\n_{self.short(employer)} ({vac["area"]["name"]})\n{vac["schedule"]["name"]}_\n*{salary}*\n{"-  "*5}'
        return '*Кому работу?*\n'+msg if msg else None


if __name__ == "__main__":
    jh = JobHhunter()
    print(jh.new_vacancies_msg())

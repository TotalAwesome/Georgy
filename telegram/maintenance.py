###############################################
#
#           Модуль техработ
#
###############################################

import requests
from bs4 import BeautifulSoup
from re import match, search
from datetime import datetime
from georgy_v2 import settings

from techworks.models import TechWork, TechWorkSource

def parse_datetime(time_string):
    """
    Парсим русскую дату
    """
    def _date(string):
        return datetime(tzinfo=settings.TIME_ZONE).strptime(string, '%d %m %Y %H:%M')

    time_string = time_string.replace('\xa00', ' ')
    time_string = time_string.replace('\xa0', ' ')
    MONTHS = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12',
    }
    year = datetime.today().year
    for month in MONTHS:
        time_string = time_string.replace(month, f'{MONTHS[month]} {year}')
    if '-' not in time_string:
        time_string = time_string.replace('С ', '')
        splited = time_string.split('До')
        date_start = _date(splited[0].strip()) 
        date_end = _date(splited[1].strip())
    else:
        splited = time_string.split(' -')
        date_start = _date(splited[0].strip())
        splited[1] = f"{date_start.strftime('%d %m %Y')} {splited[1]}"
        date_end = _date(splited[1].strip())
    
    return date_start, date_end


class TechDB:

    def _check_new(self, work_item):
        techworks_list = TechWork.objects.filter(
            time_string=work_item['time'],
            description=work_item['content']
        )
        if not techworks_list:
            return True
    
    def _new_techwork(self, techwork):
        start, end = parse_datetime(techwork['time'])
        TechWork.objects.create(
            source=TechWorkSource.objects.get(name='IKS'),
            time_string=techwork['time'],
            title=techwork['title'],
            description=techwork['content'],
            start_time=start,
            end_time=end
        )

class TechWorks:

    db = TechDB()

    def _get_list(self):
        try:
            raw = requests.get('https://iks.ru/works').text
            soup = BeautifulSoup(raw, 'lxml')
            works_list = soup.find_all('li', {'class': 'WorksPage__workItem'})
            return works_list
        except Exception as e:
            print('Не получены работы IKS')
            print(e)

    def _prepare_list(self, raw_list):
        tw_list = []
        for item in raw_list:
            soup = BeautifulSoup(str(item), 'lxml')
            timestring = soup.find('div', {'class': 'TechWork__dateInfo'}).text
            timestring = timestring[1:len(timestring)]
            title = soup.find('h2', {'class': 'TechWork__title'}).text
            content = soup.find('div', {'class': 'fr-view'}).text
            if match('(.+)Служба', content):
                content = search('(.+)Служба', content).group(1)
            else:
                content = content.replace('<p>', '')
                content = content.replace('</p>', '')
            tw_list.append(
                {
                    'source': 'IKS',
                    'time': timestring,
                    'title': title.replace('"', ' '),
                    'content': content.replace('"', ' ')
                }
            )
        return tw_list

    def iks_maintenance(self):
        works_list_iks = self._get_list()

        if not works_list_iks:
            return

        prepared_list = self._prepare_list(works_list_iks)
        for i in prepared_list:
            result = self.db._check_new(i)
            if result:
                self.db._new_techwork(i)

    def new_msg(self):
        tw_list = TechWork.objects.filter(new=True)
        msg = ''
        for i in tw_list:
            msg += f'*{i.title}*\n{"- " * 10}\n{i.time_string}\n_{i.description}_\n{"- " * 10}\n'
            i.new = False
            i.save()
        return msg


if __name__ == '__main__':
    tw = TechWorks()
    print(tw.iks_maintenance())
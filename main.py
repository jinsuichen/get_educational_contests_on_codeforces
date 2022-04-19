from bs4.element import Tag
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


# Get page count of contests
html = requests.get("https://codeforces.com/contests/")
soap = BeautifulSoup(html.content, 'lxml')
pages = soap.select('.page-index > a')
max_page_num = int(pages[-1].get_text())


# Get a list of all contests
base_url = "https://codeforces.com/contests/page/"
contests_list = []

for page_num in range(1, max_page_num + 1):
    time.sleep(0.2)
    url = base_url + str(page_num)
    print('running... ' + str(page_num) + '/' + str(max_page_num))
    html = requests.get(url)
    soap = BeautifulSoup(html.content, 'lxml')
    contests = soap.select('#pageContent > div.contestList > div.contests-table > div.datatable > div:nth-child(6) > '
                           'table > tr[data-contestid]')
    for contest in contests:  # type: Tag
        cells = contest.select('td')
        name_cell = cells[0]  # type: Tag
        time_cell = cells[2]  # type: Tag
        contest_name = name_cell.contents[0].strip()  # type: str
        link = 'https://codeforces.com' + name_cell.a['href']  # type: str
        start_time = time_cell.span.get_text().strip()  # type: str
        if 'Educational' in contest_name:
            contests_list.append({
                'contest_name': contest_name,
                'link': link,
                'start_time': start_time
            })


# Process result
pf = pd.DataFrame(list(contests_list))
order = ['contest_name', 'link', 'start_time']
pf = pf[order]
file_path = pd.ExcelWriter('results.xlsx')
pf.to_excel(file_path, encoding='utf-8', index=False)
file_path.save()

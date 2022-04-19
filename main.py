import requests
import time
import pandas as pd


# Get data by Codeforces api
contests = requests.get("https://codeforces.com/api/contest.list?gym=false").json()['result']


# Deal with contests list.
# Erase non-educational round.
contests = list(filter(lambda x: 'Educational' in x['name'], contests))
# Reverse contests list to sort by time in ascending order.
contests.reverse()


# Format contests. (Add attributes about link and format time)
for contest in contests:
    contest['link'] = 'https://codeforces.com/contest/' + str(contest['id'])
    contest['formatTime'] = time.strftime("%Y-%m-%d %H:%M", time.localtime(contest['startTimeSeconds']))


# Process result.
result = pd.DataFrame(list(contests))
order = ['name', 'link', 'formatTime']
result = result[order]
result.to_excel('results.xlsx', encoding='utf-8', index=False)
